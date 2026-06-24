# Filosofía y Mejores Prácticas para la Redacción de Artículos de ML

Esta referencia recopila consejos de redacción de destacados investigadores de ML, incluyendo a Neel Nanda, Andrej Karpathy, Sebastian Farquhar, Zachary Lipton y Jacob Steinhardt.

---

## Contenido

- [El Principio Narrativo](#el-principio-narrativo)
- [Distribución del Tiempo](#distribución-del-tiempo)
- [Fórmula para el Resumen](#fórmula-para-el-resumen)
- [Estructura de la Introducción](#estructura-de-la-introducción)
- [Claridad a Nivel de Oración](#claridad-a-nivel-de-oración)
- [Elección de Palabras y Precisión](#elección-de-palabras-y-precisión)
- [Redacción Matemática](#redacción-matemática)
- [Diseño de Figuras](#diseño-de-figuras)
- [Errores Comunes a Evitar](#errores-comunes-a-evitar)

---

## El Principio Narrativo

### De Neel Nanda

"Un artículo es una historia técnica corta, rigurosa y basada en evidencia, con una conclusión que importe a los lectores."

La narrativa se sustenta en tres pilares que deben estar clarísimos al final de tu introducción:

**El "Qué"**: De una a tres afirmaciones novedosas específicas que encajen en un tema cohesivo. Contribuciones vagas como "estudiamos X" fracasan de inmediato — los revisores necesitan afirmaciones precisas y falseables.

**El "Por qué"**: Evidencia empírica rigurosa que respalde convincentemente esas afirmaciones, incluyendo líneas de base sólidas ajustadas honestamente y experimentos que distingan entre hipótesis competidoras, en lugar de meramente mostrar "resultados decentes".

**El "Y qué"**: Por qué los lectores deberían importarse, conectando tu contribución con problemas que la comunidad reconoce como importantes.

---

## Distribución del Tiempo

### De Neel Nanda

Dedica aproximadamente **la misma cantidad de tiempo** a cada uno de:
1. El resumen
2. La introducción
3. Las figuras
4. Todo lo demás combinado

Esto no es una hipérbole — la mayoría de los revisores forman juicios preliminares antes de llegar a la sección de métodos. Los lectores encuentran tu artículo en un patrón predecible: **título → resumen → introducción → figuras → quizás el resto.**

### Patrones de Lectura de los Revisores

Estudios sobre el comportamiento de los revisores muestran:
- El resumen se lee el 100% de las veces
- La introducción es hojeada por más del 90% de los revisores
- Las figuras se examinan antes que los métodos en la mayoría de los casos
- Los métodos completos se leen solo si se ha establecido interés

**Implicación**: Pon el valor de tu artículo al frente. No entierres la contribución.

---

## Fórmula para el Resumen

### Fórmula de 5 Oraciones de Sebastian Farquhar

1. **Lo que lograste**: "Presentamos...", "Demostramos...", "Probamos..."
2. **Por qué es difícil e importante**
3. **Cómo lo haces** (con palabras clave especializadas para facilitar el descubrimiento)
4. **Qué evidencia tienes**
5. **Tu número/resultado más notable**

### Ejemplo (Buen Resumen)

```
Demostramos que el descenso de gradiente en redes neuronales
sobreparametrizadas converge a mínimos globales a una tasa lineal. [Qué]
Esto resuelve una pregunta fundamental sobre por qué el aprendizaje
profundo funciona a pesar de paisajes de optimización no convexos. [Por qué difícil/importante]
Nuestra demostración se basa en mostrar que el Neural Tangent Kernel
se mantiene aproximadamente constante durante el entrenamiento,
reduciendo el problema a regresión con kernels. [Cómo con palabras clave]
Validamos nuestra teoría en CIFAR-10 e ImageNet, mostrando que las
tasas de convergencia predichas coinciden con los experimentos dentro
del 5%. [Evidencia]
Esta es la primera garantía de convergencia en tiempo polinomial para
redes con profundidad y anchura prácticas. [Resultado notable]
```

### Qué Evitar

De Zachary Lipton: "Si la primera oración se puede anteponer a cualquier artículo de ML, elimínala."

**Elimina estas aperturas**:
- "Los modelos de lenguaje grandes han logrado un éxito notable..."
- "El aprendizaje profundo ha revolucionado..."
- "En los últimos años, las redes neuronales han..."

**Comienza con tu contribución específica en su lugar.**

---

## Sobre la Introducción

### Viñetas de Contribución: Buenas vs Malas

**Buenas:**
- Demostramos que X converge en tiempo O(n log n) bajo el supuesto Y
- Presentamos Z, una arquitectura de 3 capas que reduce la memoria en un 40%
- Demostramos que A supera a B en un 15% en el punto de referencia C

**Malas:**
- Estudiamos el problema de X (no es una contribución)
- Proporcionamos experimentos extensos (demasiado vago)
- Hacemos varias contribuciones al campo (no dice nada)

---

## Claridad a Nivel de Oración

### De Gopen & Swan: "The Science of Scientific Writing"

El artículo seminal de 1990 de George Gopen y Judith Swan establece que **los lectores tienen expectativas estructurales** sobre dónde aparece la información en la prosa. Violar estas expectativas obliga a los lectores a gastar energía en la estructura en lugar del contenido.

> "Si el lector ha de captar lo que el escritor quiere decir, el escritor debe entender lo que el lector necesita."

#### Los 7 Principios de las Expectativas del Lector

**Principio 1: Proximidad Sujeto-Verbo**

Mantén el sujeto gramatical y el verbo cerca. Cualquier cosa que intervenga se lee como una interrupción de menor importancia.

**Débil**: "El modelo, que fue entrenado con 100M de tokens y ajustado con datos de dominio específico usando LoRA con rango 16, logra resultados de vanguardia"

**Fuerte**: "El modelo logra resultados de vanguardia tras entrenarse con 100M de tokens y ajustarse con LoRA (rango 16)"

**Principio 2: Posición de Énfasis (Guarda lo Mejor para el Final)**

Los lectores enfatizan naturalmente las **últimas palabras de una oración**. Coloca allí tu información más importante.

**Débil**: "La precisión mejora un 15% al usar atención"
**Fuerte**: "Al usar atención, la precisión mejora un **15%**"

**Principio 3: Posición Temática (Lo Primero es lo Primero)**

El comienzo de una oración establece la perspectiva. Pon el elemento de "cuya historia se cuenta" primero — los lectores esperan que la oración trate sobre quien aparece primero.

**Débil**: "Se introduce un novedoso mecanismo de atención que calcula puntuaciones de alineación"
**Fuerte**: "Para abordar el problema de alineación, introducimos un novedoso mecanismo de atención"

**Principio 4: Información Vieja Antes que Nueva**

Coloca la información familiar (vieja) en la posición temática para enlace hacia atrás; coloca la información nueva en la posición de énfasis.

**Débil**: "La atención dispersa fue introducida por Child et al. La complejidad cuadrática de la atención estándar motiva este trabajo."
**Fuerte**: "La atención estándar tiene complejidad cuadrática. Para abordar esto, Child et al. introdujeron la atención dispersa."

**Principio 5: Una Unidad, Una Función**

Cada unidad de discurso (oración, párrafo, sección) debe cumplir una única función. Si tienes dos puntos, usa dos unidades.

**Principio 6: Articular la Acción en el Verbo**

Expresa la acción de cada oración en su verbo, no en sustantivos nominalizados.

**Débil**: "Realizamos un análisis de los resultados" (nominalización)
**Fuerte**: "Analizamos los resultados" (acción en el verbo)

**Principio 7: Contexto Antes que Información Nueva**

Proporciona contexto antes de pedirle al lector que considere algo nuevo. Esto aplica a todos los niveles — oración, párrafo, sección.

**Débil**: "La Ecuación 3 muestra que la convergencia está garantizada cuando la tasa de aprendizaje satisface..."
**Fuerte**: "Para que la convergencia esté garantizada, la tasa de aprendizaje debe satisfacer la condición de la Ecuación 3..."

#### Tabla Resumen

| Principio                | Regla                            | Mnemotecnia                               |
| ------------------------ | -------------------------------- | ----------------------------------------- |
| Proximidad Sujeto-Verbo  | Mantén sujeto y verbo cerca      | "No te interrumpas"                       |
| Posición de Énfasis      | Énfasis al final de la oración   | "Guarda lo mejor para el final"           |
| Posición Temática        | Contexto al inicio de la oración | "Lo primero es lo primero"                |
| Viejo Antes que Nuevo    | Familiar → no familiar           | "Construye sobre terreno conocido"        |
| Una Unidad, Una Función  | Cada párrafo = un punto          | "Una idea por contenedor"                 |
| Acción en el Verbo       | Usa verbos, no nominalizaciones  | "Los verbos hacen, los sustantivos están" |
| Contexto Antes que Nuevo | Explica antes de presentar       | "Prepara el escenario primero"            |

---

## Consejos de Micro-Redacción

### De Ethan Perez (Anthropic)

Estos consejos prácticos de micro-nivel mejoran la claridad a nivel de oración y palabra.

#### Manejo de Pronombres

**Minimiza los pronombres** ("esto," "ello," "estos," "aquello"). Cuando los pronombres sean necesarios, úsalos como adjetivos con un sustantivo:

**Débil**: "Esto muestra que el modelo converge."
**Fuerte**: "Este resultado muestra que el modelo converge."

**Débil**: "Ello mejora el rendimiento."
**Fuerte**: "Esta modificación mejora el rendimiento."

#### Posición del Verbo

**Coloca los verbos temprano** en las oraciones para facilitar el análisis:

**Débil**: "El gradiente, después de ser calculado y normalizado, actualiza los pesos."
**Fuerte**: "El gradiente actualiza los pesos después de ser calculado y normalizado."

#### Expansión del Posesivo

Transforma las construcciones posesivas para mayor claridad:

**Original**: "El Y de X" → **Expandido**: "El Y de X" (se mantiene igual en español)

**Antes**: "La precisión del modelo en el conjunto de prueba"
**Después**: "La precisión del modelo en el conjunto de prueba"

En español el posesivo ya se expresa naturalmente con "de", por lo que esta regla aplica de forma nativa.

#### Palabras a Eliminar

Elimina estas palabras de relleno en casi todos los casos:
- "actualmente"
- "un poco"
- "afortunadamente" / "desafortunadamente"
- "muy" / "realmente"
- "bastante"
- "básicamente"
- "esencialmente"
- Conectivos excesivos ("sin embargo," "además," "asimismo" cuando no sean necesarios)

#### Reglas de Construcción de Oraciones

1. **Una idea por oración** — Si te cuesta expresar una idea en una oración, necesita dos
2. **Sin sonidos repetidos** — Evita palabras que suenen similar en la misma oración
3. **Cada oración añade información** — Elimina oraciones que meramente reiteran
4. **Voz activa siempre** — Especifica el actor ("Encontramos..." no "Se encuentra...")
5. **Sin contracciones** — Para formalidad académica

#### Arquitectura del Párrafo

- **Primera oración**: Expresa el punto claramente
- **Oraciones intermedias**: Respaldan con evidencia
- **Última oración**: Refuerza o hace transición

No entierres información clave en medio de los párrafos.

---

## Elección de Palabras y Precisión

### De Zachary Lipton

**Elimina las ambigüedades** a menos que exista incertidumbre genuina:
- Elimina "puede" y "podría" a menos que sea necesario
- "proporciona una aproximación *muy* ajustada" transpira inseguridad
- "proporciona una aproximación ajustada" es seguro

**Evita los intensificadores vacíos**:
- Elimina: muy, extremadamente, altamente, significativamente (a menos que sea estadístico)
- Estas palabras señalan inseguridad, no fortaleza

### De Jacob Steinhardt

**Precisión sobre brevedad**: Reemplaza términos vagos por específicos.

| Vago              | Específico                                          |
| ----------------- | --------------------------------------------------- |
| rendimiento       | precisión, latencia, rendimiento                    |
| mejora            | aumenta la precisión en X%, reduce la latencia en Y |
| grande            | 1B parámetros, 100M tokens                          |
| rápido            | 3x más rápido, 50ms de latencia                     |
| buenos resultados | 92% de precisión, 0.85 F1                           |

**Terminología consistente**: Referirse al mismo concepto con términos diferentes crea confusión.

**Elige uno y mantente con él**:
- "modelo" vs "red" vs "arquitectura"
- "entrenamiento" vs "aprendizaje" vs "optimización"
- "muestra" vs "ejemplo" vs "instancia"

### Señalización de Vocabulario

**Evita palabras que señalen trabajo incremental**:
- Nunca: "combinar," "modificar," "expandir," "extender"
- En su lugar: "desarrollar," "proponer," "introducir"

**Por qué**: "Combinamos X e Y" suena como si hubieras juntado dos ideas existentes con grapas. "Desarrollamos un método que aprovecha X para Y" suena como una contribución genuina.

---

## Redacción Matemática

### De Ethan Perez

**Expande los posesivos** para mayor claridad:
- Débil: "El Y de X"
- Fuerte: "El Y de X" (en español se usa naturalmente)

Ejemplo: "la precisión del modelo" → "la precisión del modelo" (en español es la misma construcción)

### Principios Generales

1. **Enuncia todos los supuestos formalmente** antes de los teoremas
2. **Proporciona explicaciones intuitivas** junto con las demostraciones
3. **Usa notación consistente** en todo el artículo
4. **Define los símbolos en su primer uso**

### Convenciones de Notación

```typst
// Escalares: cursiva minúscula
$x$, $y$, $alpha$, $beta$

// Vectores: negrita minúscula
$bold(x)$, $bold(v)$

// Matrices: negrita mayúscula
$bold(W)$, $bold(X)$

// Conjuntos: caligráfica mayúscula (requiere paquete)
$cal(X)$, $cal(D)$

// Funciones: romana para funciones nombradas
$op("softmax")$, $op("ReLU")$
```

---

## Diseño de Figuras

### De Neel Nanda

Las figuras deben contar una historia coherente incluso si el lector se salta el texto. Muchos lectores SE saltan el texto inicialmente.

### Principios de Diseño

1. **La Figura 1 es crucial**: A menudo es lo primero que los lectores examinan después del resumen
2. **Leyendas autocontenidas**: El lector debe entender la figura sin el texto principal
3. **Sin título dentro de la figura**: La leyenda cumple esa función (regla de ICML/NeurIPS)
4. **Gráficos vectoriales**: PDF/EPS para gráficos, PNG (600 DPI) solo para fotografías

### Requisitos de Accesibilidad

El 8% de los hombres tienen deficiencia en la visión del color. Tus figuras deben funcionar para ellos.

**Soluciones**:
- Usa paletas seguras para daltonismo: Okabe-Ito o Paul Tol
- Evita combinaciones rojo-verde
- Verifica que las figuras funcionen en escala de grises
- Usa diferentes estilos de línea (sólida, discontinua, punteada) además de colores

### Herramientas

```python
# SciencePlots: Estilos listos para publicación
import matplotlib.pyplot as plt
plt.style.use(['science', 'ieee'])

# O para estilo Nature
plt.style.use(['science', 'nature'])
```

---

## Errores Comunes a Evitar

### Errores de Estructura

| Error                                    | Solución                                    |
| ---------------------------------------- | ------------------------------------------- |
| Viñetas de contribución faltantes        | Añade afirmaciones específicas y falseables |
| Experimentos sin afirmaciones explícitas | Indica qué prueba cada experimento          |

### Errores de Redacción

| Error                         | Solución                                         |
| ----------------------------- | ------------------------------------------------ |
| Apertura genérica del resumen | Comienza con tu contribución específica          |
| Terminología inconsistente    | Elige un término por concepto                    |
| Uso excesivo de voz pasiva    | Usa voz activa: "Mostramos" no "Se muestra"      |
| Ambigüedad en todas partes    | Sé seguro a menos que haya incertidumbre genuina |

### Errores en Figuras

| Error                                     | Solución                          |
| ----------------------------------------- | --------------------------------- |
| Gráficos rasterizados para diagramas      | Usa vectoriales (PDF/EPS)         |
| Esquema de color rojo-verde               | Usa paleta segura para daltonismo |
| Título dentro de la figura                | Pon el título en la leyenda       |
| Leyendas que requieren el texto principal | Haz las leyendas autocontenidas   |

### Errores de Citación

| Error                                     | Solución                                                    |
| ----------------------------------------- | ----------------------------------------------------------- |
| Trabajo Relacionado artículo por artículo | Organiza metodológicamente                                  |
| Citas relevantes faltantes                | Los revisores son autores de artículos — cita generosamente |
| Citas generadas por IA                    | Verifica siempre mediante APIs                              |
| Formato de citación inconsistente         | Usa BibLaTeX con claves consistentes                        |

---

## Lista de Verificación Pre-Presentación

Antes de presentar, verifica:

**Narrativa**:
- [ ] Puedo expresar la contribución en una oración
- [ ] Los tres pilares (Qué/Por qué/Y qué) están claros en la introducción
- [ ] Cada experimento respalda una afirmación específica

**Estructura**:
- [ ] El resumen sigue la fórmula de 5 oraciones
- [ ] Se incluyen viñetas de contribución
- [ ] Sección de limitaciones presente

**Redacción**:
- [ ] Terminología consistente en todo el documento
- [ ] Sin oraciones de apertura genéricas
- [ ] Ambigüedades eliminadas a menos que sean necesarias
- [ ] Todas las figuras tienen leyendas autocontenidas

**Técnico**:
- [ ] Todas las citas verificadas mediante API
- [ ] Barras de error incluidas con la metodología
- [ ] Recursos computacionales documentados
- [ ] Disponibilidad de código/datos indicada
