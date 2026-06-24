# Text Comparison Metrics

Methods and metrics for comparing two natural language texts: a **True Answer** (reference/ground truth) and a **Test Answer** (candidate/generated text).

## 1. Lexical Similarity Metrics

### 1.1 Exact Match (EM)
- **Description**: Binary metric indicating if test answer exactly matches true answer (case-insensitive, whitespace-normalized)
- **Range**: 0 (no match) to 1 (exact match)
- **Use Case**: Strict comparison, factual QA systems
- **Library**: `sklearn.metrics.accuracy_score` or custom implementation
- **Language Independent**: ✅ Yes

### 1.2 Levenshtein Distance (Edit Distance)
- **Description**: Minimum number of single-character edits (insertions, deletions, substitutions) needed to transform one text into another
- **Range**: 0 (identical) to max(len(text1), len(text2))
- **Use Case**: Typo detection, spell checking
- **Library**: `python-Levenshtein`, `nltk.edit_distance()`
- **Language Independent**: ✅ Yes (character-level, works with any Unicode text)

### 1.3 Jaccard Similarity
- **Description**: Size of intersection divided by size of union of word sets
- **Formula**: J(A,B) = |A ∩ B| / |A ∪ B|
- **Range**: 0 (no overlap) to 1 (identical sets)
- **Use Case**: Quick word overlap assessment
- **Library**: `sklearn.metrics.jaccard_score` or custom implementation
- **Language Independent**: ✅ Yes (token-based, no linguistic knowledge required)

### 1.4 Token Overlap (F1)
- **Description**: Harmonic mean of precision and recall at token level
- **Range**: 0 to 1
- **Use Case**: QA systems, extractive summarization
- **Library**: Custom implementation or `sklearn.metrics.f1_score`
- **Language Independent**: ✅ Yes (requires tokenization but no language-specific features)

## 2. N-gram Based Metrics

### 2.1 BLEU (Bilingual Evaluation Understudy)
- **Description**: Precision-based metric comparing n-gram overlap with brevity penalty
- **Range**: 0 to 1 (or 0 to 100)
- **Use Case**: Machine translation, text generation
- **Library**: `nltk.translate.bleu_score`, `sacrebleu`
- **Language Independent**: ✅ Yes (n-gram matching, no linguistic features)

### 2.2 ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
- **Variants**:
  - **ROUGE-N**: N-gram recall
  - **ROUGE-L**: Longest common subsequence
  - **ROUGE-W**: Weighted longest common subsequence
  - **ROUGE-S**: Skip-bigram co-occurrence
- **Range**: 0 to 1
- **Use Case**: Summarization, text generation
- **Library**: `rouge-score`, `py-rouge`
- **Language Independent**: ⚠️ Partially (ROUGE-N and ROUGE-L are language-independent; stemming option is English-specific)

### 2.3 METEOR (Metric for Evaluation of Translation with Explicit ORdering)
- **Description**: Harmonic mean of precision and recall with stemming, synonyms, and word order alignment
- **Range**: 0 to 1
- **Use Case**: Machine translation, more nuanced than BLEU
- **Library**: `nltk.translate.meteor_score`
- **Language Independent**: ❌ No (requires language-specific stemmers and synonym databases)

## 3. Semantic Similarity Metrics

### 3.1 Cosine Similarity with Word Embeddings
- **Description**: Cosine of angle between vector representations of texts
- **Range**: -1 to 1 (typically 0 to 1 for text)
- **Embeddings**: Word2Vec, GloVe, FastText
- **Library**: `gensim`, `sklearn.metrics.pairwise.cosine_similarity`
- **Language Independent**: ⚠️ Depends on embeddings (multilingual models like XLM, mBERT available; monolingual models are language-specific)

### 3.2 Sentence Embeddings Similarity
- **Models**:
  - **Sentence-BERT (SBERT)**: Fine-tuned BERT for sentence embeddings
  - **Universal Sentence Encoder**: Google's pre-trained model
  - **InferSent**: Facebook's sentence embeddings
- **Range**: -1 to 1 (cosine similarity)
- **Use Case**: Semantic textual similarity
- **Library**: `sentence-transformers`, `tensorflow-hub`
- **Language Independent**: ⚠️ Depends on model (multilingual models like `paraphrase-multilingual-MiniLM` available; default models often English-only)

### 3.3 BERTScore
- **Description**: Computes precision, recall, and F1 using contextual embeddings from BERT
- **Range**: 0 to 1
- **Use Case**: Text generation evaluation with semantic understanding
- **Library**: `bert-score`
- **Language Independent**: ⚠️ Depends on model (supports multilingual BERT models like mBERT, XLM-RoBERTa)

### 3.4 Word Mover's Distance (WMD)
- **Description**: Minimum cumulative distance word embeddings need to "travel" to transform one text into another
- **Range**: 0 (identical meaning) to ∞
- **Use Case**: Semantic similarity with word-level granularity
- **Library**: `gensim.models.Word2Vec.wmdistance()`
- **Language Independent**: ⚠️ Depends on embeddings (multilingual embeddings available but require training)

## 4. Advanced Neural Metrics

### 4.1 MoverScore
- **Description**: Soft alignment between contextualized embeddings using Earth Mover's Distance
- **Range**: 0 to 1
- **Use Case**: Text generation evaluation
- **Library**: `moverscore`
- **Language Independent**: ⚠️ Depends on model (supports multilingual transformers)

### 4.2 BARTScore
- **Description**: Uses BART model to compute generation probability
- **Range**: Log probability scores
- **Use Case**: Text generation, summarization
- **Library**: `bart-score` or custom implementation
- **Language Independent**: ⚠️ Depends on model (BART is primarily English; mBART available for multilingual)

### 4.3 BLEURT
- **Description**: BERT-based learned metric trained on human judgments
- **Range**: Approximately -1 to 1 (not bounded)
- **Use Case**: High correlation with human judgments
- **Library**: `bleurt` (Google Research)
- **Language Independent**: ❌ No (trained primarily on English data)

## 5. Task-Specific Metrics

### 5.1 Semantic Answer Similarity (SAS)
- **Description**: Cross-encoder models that directly compare question-answer pairs
- **Range**: 0 to 1
- **Use Case**: Question answering systems
- **Library**: `sentence-transformers` with cross-encoders
- **Language Independent**: ⚠️ Depends on model (multilingual cross-encoders available)

### 5.2 Answer Equivalence
- **Description**: Binary classification if answers are semantically equivalent
- **Models**: Fine-tuned transformers (RoBERTa, DeBERTa)
- **Range**: 0 (different) to 1 (equivalent)
- **Use Case**: QA evaluation, exam grading
- **Language Independent**: ⚠️ Depends on model (requires multilingual models for non-English)

## 6. Character-Level Metrics

### 6.1 Character Error Rate (CER)
- **Description**: Edit distance normalized by true answer length
- **Formula**: CER = (insertions + deletions + substitutions) / length(true_answer)
- **Range**: 0 to ∞
- **Use Case**: OCR, speech recognition
- **Library**: `jiwer`, custom implementation
- **Language Independent**: ✅ Yes (operates on character sequences)

### 6.2 Longest Common Substring (LCS)
- **Description**: Length of longest contiguous matching substring
- **Range**: 0 to min(len(text1), len(text2))
- **Use Case**: Plagiarism detection, diff tools
- **Library**: Custom implementation, `difflib`
- **Language Independent**: ✅ Yes (sequence matching algorithm)

## 7. Statistical Metrics

### 7.1 Perplexity
- **Description**: Measure of how well a probability model predicts the test answer given the true answer
- **Range**: 1 to ∞ (lower is better)
- **Use Case**: Language model evaluation
- **Library**: `transformers` library with language models
- **Language Independent**: ⚠️ Depends on language model used

### 7.2 Cross-Entropy Loss
- **Description**: Measures dissimilarity between predicted and true distributions
- **Range**: 0 to ∞ (lower is better)
- **Use Case**: Classification, generation tasks
- **Library**: `torch.nn.CrossEntropyLoss`, `tensorflow.keras.losses`
- **Language Independent**: ✅ Yes (mathematical operation on probability distributions)

## 8. Implementation Example

```python
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk

# Example texts
true_answer = "The capital of France is Paris."
test_answer = "Paris is the capital city of France."

# 1. Token-level F1
def token_f1(true_text, test_text):
    true_tokens = set(true_text.lower().split())
    test_tokens = set(test_text.lower().split())
    
    if len(test_tokens) == 0:
        return 0.0
    
    common = true_tokens.intersection(test_tokens)
    precision = len(common) / len(test_tokens)
    recall = len(common) / len(true_tokens)
    
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

# 2. BLEU Score
def compute_bleu(true_text, test_text):
    reference = [true_text.lower().split()]
    candidate = test_text.lower().split()
    smoothie = SmoothingFunction().method4
    return sentence_bleu(reference, candidate, smoothing_function=smoothie)

# 3. ROUGE Score
def compute_rouge(true_text, test_text):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(true_text, test_answer)
    return scores

# 4. Semantic Similarity (SBERT)
def semantic_similarity(true_text, test_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([true_text, test_text])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return similarity.item()

# Run comparisons
print(f"Token F1: {token_f1(true_answer, test_answer):.4f}")
print(f"BLEU: {compute_bleu(true_answer, test_answer):.4f}")
print(f"ROUGE: {compute_rouge(true_answer, test_answer)}")
print(f"Semantic Similarity: {semantic_similarity(true_answer, test_answer):.4f}")
```

## 9. Choosing the Right Metric

| Use Case | Recommended Metrics |
|----------|-------------------|
| Exact factual answers | Exact Match, Token F1 |
| Text generation quality | BLEU, ROUGE, BERTScore |
| Semantic equivalence | Sentence embeddings similarity, BERTScore |
| Translation quality | BLEU, METEOR, chrF |
| Summarization | ROUGE, BERTScore, MoverScore |
| Question Answering | Token F1, Semantic Answer Similarity, BERTScore |
| Spelling/Typos | Levenshtein Distance, CER |

## 10. Language Independence Summary

### Fully Language-Independent Metrics ✅
These metrics work with any language without modification:
- **Exact Match (EM)**
- **Levenshtein Distance**
- **Jaccard Similarity**
- **Token Overlap (F1)**
- **BLEU**
- **Character Error Rate (CER)**
- **Longest Common Substring (LCS)**
- **Cross-Entropy Loss**

### Language-Dependent with Multilingual Options ⚠️
These metrics require language-specific models but multilingual versions exist:
- **ROUGE** (language-independent core, but stemming is language-specific)
- **Word Embeddings Similarity** (use multilingual embeddings like XLM, fastText multilingual)
- **Sentence Embeddings** (use multilingual SBERT models)
- **BERTScore** (use mBERT, XLM-RoBERTa)
- **MoverScore** (use multilingual transformers)
- **Semantic Answer Similarity** (use multilingual cross-encoders)

### Language-Specific Metrics ❌
These metrics are primarily designed for English or require extensive language resources:
- **METEOR** (requires language-specific stemmers and WordNet)
- **BLEURT** (trained on English data)
- **BARTScore** (BART is English-focused; use mBART for multilingual)

### Recommendation for Multilingual Applications
For truly language-agnostic evaluation:
1. **Primary choice**: BLEU, Character-level metrics (CER, Levenshtein), Token F1
2. **With multilingual models**: BERTScore with mBERT/XLM-RoBERTa, multilingual SBERT
3. **Avoid**: METEOR, BLEURT (unless language-specific versions available)

## 11. Best Practices

1. **Use multiple metrics**: No single metric captures all aspects of text similarity
2. **Consider context**: Task-specific metrics often perform better than generic ones
3. **Normalize texts**: Lowercase, remove punctuation when appropriate
4. **Human evaluation**: Use automated metrics as proxies, validate with human judgment
5. **Semantic over lexical**: For meaning-focused tasks, prefer semantic metrics
6. **Computational cost**: Balance accuracy with inference time for production systems

## References

- BLEU: Papineni et al. (2002)
- ROUGE: Lin (2004)
- BERTScore: Zhang et al. (2020)
- Sentence-BERT: Reimers & Gurevych (2019)
- BLEURT: Sellam et al. (2020)
