import json
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Lexical metrics
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# N-gram metrics
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# Edit distance
try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    print("Warning: python-Levenshtein not installed. Using NLTK's edit_distance instead.")
    from nltk.metrics.distance import edit_distance

# Semantic similarity (multilingual models)
from sentence_transformers import SentenceTransformer, util

# Optional: BERTScore
try:
    from bert_score import score as bert_score
    BERTSCORE_AVAILABLE = True
except ImportError:
    BERTSCORE_AVAILABLE = False
    print("Warning: bert-score not installed. BERTScore will be skipped.")


def compare_texts(ground_truth: str, generated_text: str, 
                  include_semantic: bool = True,
                  include_bertscore: bool = False,
                  bertscore_scorer = None,
                  semantic_similarity_model_multilingual = None,
                  semantic_similarity_model_spanish = None) -> Dict[str, Any]:
    """
    Compare two Spanish texts using multiple metrics suitable for legal content.
    
    Args:
        ground_truth: The reference/true answer text
        generated_text: The candidate/test answer text
        include_semantic: Whether to include semantic similarity metrics (requires model loading)
        include_bertscore: Whether to include BERTScore (computationally expensive)
        bertscore_scorer: Pre-initialized BERTScore scorer object (optional)
        semantic_similarity_model_multilingual: Pre-initialized multilingual sentence transformer model (optional)
        semantic_similarity_model_spanish: Pre-initialized Spanish sentence transformer model (optional)
    
    Returns:
        Dictionary with metric results in the specified JSON format
    """
    
    results = {}
    
    # ==================== LEXICAL METRICS ====================
    
    # 1. Exact Match
    results["exact_match"] = {
        "value": float(ground_truth.strip().lower() == generated_text.strip().lower()),
        "hyperparameters": {
            "case_sensitive": False,
            "normalized_whitespace": True
        }
    }
    
    # 2. Token Overlap (F1)
    gt_tokens = set(ground_truth.lower().split())
    gen_tokens = set(generated_text.lower().split())
    
    if len(gen_tokens) == 0:
        token_f1 = 0.0
        precision = 0.0
        recall = 0.0
    else:
        common = gt_tokens.intersection(gen_tokens)
        precision = len(common) / len(gen_tokens) if len(gen_tokens) > 0 else 0.0
        recall = len(common) / len(gt_tokens) if len(gt_tokens) > 0 else 0.0
        token_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    results["token_f1"] = {
        "value": float(token_f1),
        "hyperparameters": {
            "precision": float(precision),
            "recall": float(recall),
            "case_sensitive": False
        }
    }
    
    # 3. Jaccard Similarity
    union = gt_tokens.union(gen_tokens)
    intersection = gt_tokens.intersection(gen_tokens)
    jaccard = len(intersection) / len(union) if len(union) > 0 else 0.0
    
    results["jaccard_similarity"] = {
        "value": float(jaccard),
        "hyperparameters": {
            "tokenization": "whitespace",
            "case_sensitive": False
        }
    }
    
    # 4. Levenshtein Distance (normalized)
    if LEVENSHTEIN_AVAILABLE:
        lev_distance = Levenshtein.distance(ground_truth, generated_text)
    else:
        lev_distance = edit_distance(ground_truth, generated_text)
    
    max_len = max(len(ground_truth), len(generated_text))
    normalized_lev = 1 - (lev_distance / max_len) if max_len > 0 else 1.0
    
    results["levenshtein_similarity"] = {
        "value": float(normalized_lev),
        "hyperparameters": {
            "raw_distance": int(lev_distance),
            "normalized": True,
            "max_length": int(max_len)
        }
    }
    
    # 5. Character Error Rate (CER)
    cer = lev_distance / len(ground_truth) if len(ground_truth) > 0 else 0.0
    
    results["character_error_rate"] = {
        "value": float(cer),
        "hyperparameters": {
            "edit_distance": int(lev_distance),
            "reference_length": len(ground_truth)
        }
    }
    
    # ==================== N-GRAM METRICS ====================
    
    # 6. BLEU Score
    reference = [ground_truth.lower().split()]
    candidate = generated_text.lower().split()
    
    smoothie = SmoothingFunction().method4
    
    # BLEU-1 through BLEU-4
    bleu_scores = {}
    for n in range(1, 5):
        weights = tuple([1/n] * n + [0] * (4-n))
        try:
            bleu_n = sentence_bleu(reference, candidate, weights=weights, smoothing_function=smoothie)
            bleu_scores[f"bleu_{n}"] = float(bleu_n)
        except:
            bleu_scores[f"bleu_{n}"] = 0.0
    
    # Overall BLEU (geometric mean of 1-4 grams)
    try:
        bleu_overall = sentence_bleu(reference, candidate, smoothing_function=smoothie)
    except:
        bleu_overall = 0.0
    
    results["bleu"] = {
        "value": float(bleu_overall),
        "hyperparameters": {
            "smoothing": "method4",
            "case_sensitive": False,
            **bleu_scores
        }
    }
    
    # 7. ROUGE Scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
    rouge_scores = scorer.score(ground_truth, generated_text)
    
    results["rouge_1"] = {
        "value": float(rouge_scores['rouge1'].fmeasure),
        "hyperparameters": {
            "precision": float(rouge_scores['rouge1'].precision),
            "recall": float(rouge_scores['rouge1'].recall),
            "stemming": False
        }
    }
    
    results["rouge_2"] = {
        "value": float(rouge_scores['rouge2'].fmeasure),
        "hyperparameters": {
            "precision": float(rouge_scores['rouge2'].precision),
            "recall": float(rouge_scores['rouge2'].recall),
            "stemming": False
        }
    }
    
    results["rouge_l"] = {
        "value": float(rouge_scores['rougeL'].fmeasure),
        "hyperparameters": {
            "precision": float(rouge_scores['rougeL'].precision),
            "recall": float(rouge_scores['rougeL'].recall),
            "stemming": False,
            "metric_type": "longest_common_subsequence"
        }
    }
    
    # ==================== SEMANTIC METRICS ====================
    
    if include_semantic:
        try:
            # 8.A Sentence-BERT Similarity (Multilingual)
            if semantic_similarity_model_multilingual is not None:
                model = semantic_similarity_model_multilingual
            else:
                model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            
            embeddings = model.encode([ground_truth, generated_text], convert_to_tensor=True)
            cosine_sim = util.cos_sim(embeddings[0], embeddings[1]).item()
            
            results["sbert_similarity_multilingual"] = {
                "value": float(cosine_sim),
                "hyperparameters": {
                    "model": "paraphrase-multilingual-MiniLM-L12-v2",
                    "similarity_metric": "cosine",
                    "multilingual": True,
                    "languages_supported": "50+"
                }
            }
            
        except Exception as e:
            print(f"Warning: Could not compute multilingual semantic similarity: {e}")
        
        # 8.B Sentence-BERT Similarity (Spanish-specific)
        try:
            if semantic_similarity_model_spanish is not None:
                spanish_model = semantic_similarity_model_spanish
            else:
                spanish_model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
            
            spanish_embeddings = spanish_model.encode([ground_truth, generated_text], convert_to_tensor=True)
            spanish_sim = util.cos_sim(spanish_embeddings[0], spanish_embeddings[1]).item()
            
            results["sbert_similarity_spanish"] = {
                "value": float(spanish_sim),
                "hyperparameters": {
                    "model": "hiiamsid/sentence_similarity_spanish_es",
                    "similarity_metric": "cosine",
                    "language_specific": "Spanish"
                }
            }
        except Exception as e:
            print(f"Warning: Could not compute Spanish semantic similarity: {e}")
    
    # 9. BERTScore (optional, computationally expensive)
    if include_bertscore and BERTSCORE_AVAILABLE:
        try:
            if bertscore_scorer is not None:
                # Use pre-initialized scorer
                P, R, F1 = bertscore_scorer.score([generated_text], [ground_truth])
            else:
                # Using multilingual BERT for Spanish
                P, R, F1 = bert_score(
                    [generated_text], 
                    [ground_truth], 
                    lang='es',
                    model_type='bert-base-multilingual-cased',
                    verbose=False
                )
            
            results["bertscore"] = {
                "value": float(F1.mean().item()),
                "hyperparameters": {
                    "precision": float(P.mean().item()),
                    "recall": float(R.mean().item()),
                    "model": "bert-base-multilingual-cased",
                    "language": "es",
                    "multilingual": True
                }
            }
        except Exception as e:
            print(f"Warning: Could not compute BERTScore: {e}")
    
    # ==================== ADDITIONAL METRICS ====================
    
    # 10. Length Ratio
    length_ratio = len(generated_text) / len(ground_truth) if len(ground_truth) > 0 else 0.0
    
    results["length_ratio"] = {
        "value": float(length_ratio),
        "hyperparameters": {
            "ground_truth_length": len(ground_truth),
            "generated_length": len(generated_text),
            "length_difference": abs(len(generated_text) - len(ground_truth))
        }
    }
    
    # 11. Word Count Ratio
    word_ratio = len(generated_text.split()) / len(ground_truth.split()) if len(ground_truth.split()) > 0 else 0.0
    
    results["word_count_ratio"] = {
        "value": float(word_ratio),
        "hyperparameters": {
            "ground_truth_words": len(ground_truth.split()),
            "generated_words": len(generated_text.split())
        }
    }
    
    # Wrap in final format
    output = {
        "result": results,
        "metadata": {
            "ground_truth_preview": ground_truth[:100] + "..." if len(ground_truth) > 100 else ground_truth,
            "generated_text_preview": generated_text[:100] + "..." if len(generated_text) > 100 else generated_text,
            "language": "Spanish",
            "domain": "Legal (Argentinian Law)",
            "metrics_computed": len(results)
        }
    }
    
    return output


def save_comparison_to_json(comparison_result: Dict[str, Any], output_path: str) -> None:
    """
    Save comparison results to a JSON file.
    
    Args:
        comparison_result: The dictionary returned by compare_texts
        output_path: Path where to save the JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comparison_result, f, indent=2, ensure_ascii=False)
    print(f"Results saved to: {output_path}")


# Example usage
if __name__ == "__main__":
    from pathlib import Path
    # import torch
    # import gc
    
    BASE_PATH = Path.cwd()
    INPUT_FILE = BASE_PATH.joinpath("part_e", "20251012_llm_answers_baseline_from_20250804_101435_llm_base_answers.json")
    OUTPUT_FILE = BASE_PATH.joinpath("part_e", "20251101_compare_ground_truth_vs_llm_no_RAG.json")

    # Load models once before the loop
    print("Loading semantic similarity models...")
    multilingual_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    spanish_model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
    
    # Initialize BERTScore scorer if available
    bertscore_scorer = None
    if BERTSCORE_AVAILABLE:
        print("Initializing BERTScore...")
        from bert_score import BERTScorer
        bertscore_scorer = BERTScorer(lang='es', model_type='bert-base-multilingual-cased')
    
    print("Models loaded. Starting comparison...")

    with open(INPUT_FILE, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    for question in data:
        ground_truth_text = question["respuesta"] 
        for llm_response in question["llm_responses"]:
            print(f"Calculating metrics for question {question['numero_pregunta']} and subquestion {question['numero_subpregunta']}")
            print(f"LLM response timestamp:{llm_response['metadata']['timestamp']}")
            evaluated_text = llm_response["texto"]
            
            # Pass pre-loaded models to avoid reloading
            metrics = compare_texts(
                ground_truth_text, 
                evaluated_text, 
                include_semantic=True, 
                include_bertscore=True,
                bertscore_scorer=bertscore_scorer,
                semantic_similarity_model_multilingual=multilingual_model,
                semantic_similarity_model_spanish=spanish_model
            )
            llm_response["metrics"] = metrics["result"]
            
            # # Clear GPU cache after each iteration
            # if torch.cuda.is_available():
            #     torch.cuda.empty_cache()
            
            # # Force garbage collection
            # gc.collect()

        with open(OUTPUT_FILE, encoding="utf-8", mode="w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

