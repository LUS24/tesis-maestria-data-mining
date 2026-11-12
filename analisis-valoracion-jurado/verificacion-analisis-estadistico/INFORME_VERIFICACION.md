# Informe de verificación — acuerdo inter-juez (D-14)

## 1. Objeto

La decisión `D-14` establece que el alpha de Krippendorff no debe usarse sin recalcularlo desde los resultados originales de los jueces, sin editar los archivos fuente, y que la verificación debe quedar en un directorio independiente.

Este informe documenta:

1. la reconstrucción de la matriz jueces × observaciones desde `codigo_experimentos/part_i/final_judge_results.csv`;
2. el cálculo del alpha ordinal con valores originales y con la transformación al valor de rúbrica más cercano;
3. el alpha por sistema y las correlaciones de Spearman entre pares;
4. los conteos que sostienen la base de 711 observaciones;
5. los casos que requieren revisión humana por discrepancia entre jueces o por puntajes positivos sobre salidas no sustantivas.

## 2. Método

- **Fuente:** `final_judge_results.csv`, con 2.133 filas (711 observaciones × 3 jueces).
- **Observación:** combinación de `numero_pregunta`, `numero_subpregunta` normalizada, `sistema` y `modelo_respuesta`.
- **Jueces:** Grok 4.1 Fast, DeepSeek V3.1 y Kimi K2 0905.
- **Alpha:** `krippendorff.alpha` con `level_of_measurement="ordinal"`, matriz de 3 jueces × 711 observaciones.
- **Transformación a rúbrica:** cada valor se reemplaza por el elemento más cercano de `{0; 0,25; 0,50; 0,75; 1}`; los empates se resuelven hacia el valor mayor.
- **No se usó** la tabla derivada `correccion-01.../datos/02_long_2133.csv` como insumo del cálculo; se usó solo para contrastar que sus 2.133 filas y 711 observaciones coinciden.
- **No se modificó** ningún archivo fuente, log, respuesta o evaluación.

## 3. Resultados

### 3.1. Alpha global

| Rúbrica | Valores | Observaciones | Jueces | α ordinal |
| --- | --- | ---: | ---: | ---: |
| Corrección | originales | 711 | 3 | 0,807842 |
| Corrección | transformados a rúbrica | 711 | 3 | 0,799542 |
| Precisión legal | originales | 711 | 3 | 0,784566 |
| Precisión legal | transformados a rúbrica | 711 | 3 | 0,783985 |

La diferencia entre 0,808 y 0,800 proviene de la transformación de 37 valores fuera de rúbrica (por ejemplo, 0,9; 0,95; 0,6; 0,85; 0,375). La conclusión cualitativa no cambia: el acuerdo es bueno, pero no es validación humana.

### 3.2. Alpha por sistema

| Sistema | Observaciones | α corrección original | α corrección rúbrica | α precisión original |
| --- | ---: | ---: | ---: | ---: |
| Sin RAG | 237 | 0,6979 | 0,6922 | 0,6211 |
| RAG básico | 237 | 0,8219 | 0,8140 | 0,6389 |
| Agentic-RAG | 237 | 0,8693 | 0,8623 | 0,7550 |

El acuerdo es mayor en Agentic-RAG y menor en Sin RAG. Esto describe confiabilidad entre jueces, no calidad de las respuestas.

### 3.3. Spearman entre pares

| Par | ρ | p | n |
| --- | ---: | ---: | ---: |
| Grok ↔ DeepSeek | 0,8226 | 4,98 × 10⁻¹⁷⁶ | 711 |
| Grok ↔ Kimi | 0,8438 | 8,58 × 10⁻¹⁹⁴ | 711 |
| DeepSeek ↔ Kimi | 0,7937 | 3,47 × 10⁻¹⁵⁵ | 711 |

### 3.4. Conteos

- 2.133 filas de jueces.
- 711 observaciones (79 unidades × 9 configuraciones).
- 79 unidades únicas en 25 casos.
- 58 salidas no sustantivas; 41 en Agentic-RAG + gpt-5-nano.
- 653 respuestas sustantivas.
- Costo total registrado: USD 22,2939.

## 4. Discrepancias y revisión humana

Se identificaron **23 observaciones** con un rango de puntajes entre jueces ≥ 0,75. Están en `datos/casos_discrepancia_para_revision_humana.csv`. No son errores demostrados: son candidatos para una revisión ciega por profesionales.

También se identificaron **17 evaluaciones positivas** sobre salidas no sustantivas (12 de corrección y 5 de precisión legal, según la base final de la corrección 02). Están en `datos/evaluaciones_positivas_salidas_no_sustantivas.csv`. Estos puntajes no deben promediarse como calidad.

**Advertencia para D-01/D-08:** no existen calificaciones humanas de las 711 respuestas generadas. La revisión humana documentada corresponde al benchmark (preguntas, respuestas esperadas y referencias). Por eso:

- no se puede afirmar que la “corrección humana” prevalezca sobre los jueces en la medición de respuestas;
- la revisión humana del benchmark es la referencia principal del instrumento, no una validación de los jueces;
- el alpha se reporta como confiabilidad, no como validez;
- los 23 casos de discrepancia quedan como insumo para una validación humana futura.

## 5. Contraste con la corrección 01

Los valores calculados coinciden exactamente con los publicados:

| Valor | Corrección 01 | Verificación D-14 | Coincide |
| --- | ---: | ---: | :---: |
| α original | 0,8078424689763564 | 0,8078424689763564 | Sí |
| α rúbrica | 0,7995418703552886 | 0,7995418703552886 | Sí |
| α precisión legal original | 0,7845657645755232 | 0,7845657645755232 | Sí |
| Filas de jueces | 2.133 | 2.133 | Sí |
| Observaciones | 711 | 711 | Sí |

## 6. Límites

- No se reajustó el modelo ordinal mixto; la verificación cubre el acuerdo inter-juez y los insumos descriptivos.
- No hay una muestra humana de calificaciones de respuestas; no se puede estimar acuerdo humano–juez.
- Los 23 casos de discrepancia no son una muestra aleatoria; son casos extremos.
- El alpha alto no prueba ausencia de sesgo compartido: tres jueces pueden coincidir en un mismo sesgo.
- La transformación a rúbrica modifica 37 valores; se reportan ambos resultados para transparencia.

## 7. Reproducción

```bash
cd analisis-valoracion-jurado/verificacion-analisis-estadistico
bash scripts/run_all.sh
```

Salidas: `datos/` y `salidas/resumen_verificacion.json`.
