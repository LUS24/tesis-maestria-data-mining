= Fundamentos e Historia del procesamiento de lenguaje natural (PLN) <cap:fundamentos-pln>

#import "@preview/mmdr:0.2.2": mermaid
#import "@preview/tablem:0.3.0": three-line-table
#import "@preview/zeitline:0.1.1": timeline

#quote(block: true)[
  *Nota:* El campo de los grandes modelos de lenguaje evoluciona a un ritmo sin precedentes. Este capítulo presenta los fundamentos teóricos vigentes al momento del diseño del sistema (segundo semestre de 2025). Los desarrollos posteriores al período experimental se discuten en el capítulo de trabajos relacionados.
]

== Introducción al procesamiento de lenguaje natural

El procesamiento de lenguaje natural (PLN o NLP, por sus siglas en inglés) es un área de la inteligencia artificial centrada en desarrollar modelos computacionales que permitan a las máquinas comprender, generar y razonar sobre lenguaje humano. En el corazón de muchas aplicaciones de PLN se encuentran los modelos de lenguaje, que asignan probabilidades a secuencias de palabras y permiten estimar la probabilidad de la siguiente palabra dado un contexto @jurafsky_martin_2026.

La historia del desarrollo de los modelos del lenguaje se remota hace más de 100 años a los inicios del siglo XX, comenzando desde modelos estadísticos relativamente simples, basados en distribuciones de frecuencias de palabras, hasta redes neuronales, basados en la arquitectura del Transformer. En este capítulo se realiza una breve reseña de las diferentes estrategias para el desarrollo de los modelos del lenguaje.

#let eventos_evolucion_llm_1 = (
  (date: "1913", desc: [Markov publica _An example of statistical investigation of the text Eugene Onegin_, primer modelo probabilístico de cadenas de dependencia entre muestras textuales @markov1913anexampleof @markov2006anexampleof.]),
  (date: "1948", desc: [Shannon publica _A Mathematical Theory of Communication_, que funda la teoría de la información y de los modelos de lenguaje estadísticos @shannon1948.]),
  (date: "1950", desc: [Turing plantea el _imitation game_ como criterio de inteligencia de máquina @turing1950computing.]),
  (date: "1954", desc: [Primer experimento de traducción automática basada en reglas (Georgetown--IBM) @garvin1967georgetown @hutchins2004georgetown.]),
  (date: "1966", desc: [Weizenbaum presenta ELIZA, uno de los primeros *chatbots*, basado en coincidencia de patrones @weizenbaum1966.]),
  (date: "1969", desc: [Minsky y Papert demuestran las limitaciones del perceptrón de una capa (problema XOR), provocando el primer _invierno de las redes neuronales_ @minsky2017perceptrons.]),
  (date: "1986", desc: [Rumelhart, Hinton y Williams popularizan el algoritmo de *backpropagation* @rumelhart1986learning.]),
  (date: "1990s", desc: [Métodos estadísticos y _corpus-based_ dominan el PLN: modelos de n-gramas, _Hidden Markov Models_, _Maximum Entropy_ @jurafsky_martin_2026.]),
)

#let eventos_evolucion_llm_2 = (
  (date: "2003", desc: [Bengio y colaboradores proponen el primer modelo de lenguaje neuronal @bengio2003aneural.]),
  (date: "2013", desc: [Word2Vec @mikolov2013word2vec y GloVe @pennington2014glove popularizan los _word embeddings_ como representación distribuida del lenguaje.]),
  (date: "2014", desc: [Sutskever y colaboradores introducen la arquitectura secuencia-a-secuencia (_seq2seq_) @sutskever2014seq2seq; GRU @cho2014 como alternativa a la LSTM.]),
  (date: "2017", desc: [Aparece la arquitectura *Transformer* @vaswani2017, basada enteramente en atención, desplazando a las arquitecturas recurrentes.]),
  (date: "2018", desc: [BERT @devlin2018bert demuestra la potencia de los modelos bidireccionales basados en _encoder_; GPT-1 @radford2018improving funda la familia *decoder-only*.]),
  (date: "2019", desc: [GPT-2 @radford2019language_models muestra habilidades _zero-shot_ sorprendentes a 1.5 mil millones de parámetros.]),
  (date: "2020", desc: [GPT-3 @brown2020gpt3 introduce el _in-context learning_ a 175 mil millones de parámetros, popularizando el paradigma _few-shot_ prompting.]),
  (date: "2021", desc: [Codex, CLIP y DALL-E extienden los LLMs a código y a modalidades visuales.]),
)

#figure(
  timeline(
    eventos_evolucion_llm_1,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 11pt,
        body: 9pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.4em,
        arm:  2.6em,
      ),
    ),
  ),
  caption: [Cronología de los hitos principales en la evolución de los modelos del lenguaje (1913--1990s). Primera parte.],
) <fig_evolucion_llms_1>

#figure(
  timeline(
    eventos_evolucion_llm_2,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 11pt,
        body: 9pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.4em,
        arm:  2.6em,
      ),
    ),
  ),
  caption: [Cronología de los hitos principales en la evolución de los modelos del lenguaje (2003--2021). Segunda parte.],
) <fig_evolucion_llms_2>

== Evolución de los modelos del lenguaje

De acuerdo a la taxonomía mencionada por #cite(<raeini2025evolution>, form: "prose"), los modelos del lenguaje pueden clasificarse de la siguiente manera:

+ Estadísticos
+ Basados en reglas
+ Basados en recuperación de información
+ Basados en espacio de vectores
+ Redes Neuronales
+ Redes Neuronales basadas en la arquitectura Transformer
+ Estado de espacios

=== Modelos estadísticos

La primera aproximación para tratar de predecir secuencias de texto fueron los trabajos de #cite(<markov1913anexampleof>, form: "prose") #cite(<markov2006anexampleof>, form: "prose") y #cite(<shannon1948>, form: "prose") que derivaron en la creación de modelos estadísticos permitiendo caracterizar la probabilidad de secuencias de letras (palabras y frases). Esta estrategia se basa en el uso de n-gramas, los cuales consisten en secuencias de caracteres de longitud $n$. Por ejemplo, para la frase "Pablito clavó un clavito qué clavito clavó Pablito" se pueden obtener los siguientes n-gramas:

*Unigramas — n = 1:*

#align(center, three-line-table(
  columns: (auto, auto),
  [
    | *N.* | *Palabra* |
    | :--- | :-------- |
    | 1    | Pablito   |
    | 2    | clavó     |
    | 3    | un        |
    | 4    | clavito   |
    | 5    | qué       |
    | 6    | clavito   |
    | 7    | clavó     |
    | 8    | Pablito   |
  ],
))

*Bigramas — n = 2:*

#align(center, three-line-table(
  columns: (auto, auto, auto),
  [
    | *N.* | *Palabra 1* | *Palabra 2* |
    | :--- | :---------- | :---------- |
    | 1    | Pablito     | clavó       |
    | 2    | clavó       | un          |
    | 3    | un          | clavito     |
    | 4    | clavito     | qué         |
    | 5    | qué         | clavito     |
    | 6    | clavito     | clavó       |
    | 7    | clavó       | Pablito     |
  ],
))

*Trigramas — n = 3:*

#align(center, three-line-table(
  columns: (auto, auto, auto, auto),
  [
    | *N.* | *Palabra 1* | *Palabra 2* | *Palabra 3* |
    | :--- | :---------- | :---------- | :---------- |
    | 1    | Pablito     | clavó       | un          |
    | 2    | clavó       | un          | clavito     |
    | 3    | un          | clavito     | qué         |
    | 4    | clavito     | qué         | clavito     |
    | 5    | qué         | clavito     | clavó       |
    | 6    | clavito     | clavó       | Pablito     |
  ],
))

A partir de los cuales es posible construir un modelo estadístico siguiendo la ecuación:

$ P(w | h) = ("count"(h, w)) / ("count"(h)) $

Donde $"count"(h, w)$ es el número de veces que la secuencia $h$ seguida de $w$ aparece en el texto, y $"count"(h)$ es el número total de veces que aparece el contexto $h$. Para el caso de la palabra "clavó" empleando bigramas se obtiene:

$ P("clavó" | "Pablito") = ("count"("Pablito", "clavó")) / ("count"("Pablito")) $

#figure(
  [#align(center)[
    #block(width: 9cm, height: auto)[
      #mermaid(
      "graph TD
       A[Palabra inicial: Pablito] --> B[Buscar bigramas que comienzan con Pablito]
       B --> C[Obtener distribución de probabilidad]
       C --> D[Muestrear siguiente palabra según P]
       D --> E{¿Se alcanzó longitud deseada?}
       E -->|No| F[Nueva palabra como contexto]
       E -->|Sí| G[Texto generado]
       B <-- F
       
       linkStyle 0 stroke:#0066cc,stroke-width:2px;
       linkStyle 3 stroke:#ffaa00,stroke-width:2px;
       linkStyle 6 stroke:#0066cc,stroke-width:2px;
       
       style A fill:#e6f3ff,stroke:#0066cc,stroke-width:2px;
       style C fill:#fff3e6,stroke:#cc6600,stroke-width:2px;
       style D fill:#ffe6f0,stroke:#cc0066,stroke-width:2px;
       style G fill:#e6ffe6,stroke:#00aa00,stroke-width:2px;",
      )
    ]
  ]],
  caption: [Diagrama de flujo de generación de texto basado en n-gramas, siguiendo el método de #cite(<shannon1948>, form: "prose").],
) <fig_flujo_ngramas>

A pesar de su utilidad, los modelos de n-gramas presentan limitaciones sustanciales que restringen severamente su aplicabilidad a vocabularios y corpus de gran escala @jurafsky_martin_2026 @chengoodman1999smoothing:

+ *Explosión combinatoria y dispersión.* El número de n-gramas únicos crece de manera aproximadamente exponencial con el tamaño del vocabulario y con el orden $n$. Esto vuelve a los modelos de orden superior ($n >= 4$) rápidamente intratables, tanto en memoria como en tiempo de cómputo, aún para corpus de tamaño modesto.
+ *Gestión de palabras fuera de vocabulario (OOV).* Toda palabra que no haya sido observada en el corpus de entrenamiento recibe probabilidad cero. Análogamente, los n-gramas que contienen palabras raras o no vistas obtienen estimaciones de probabilidad poco fiables, fenómeno conocido como _data sparsity_. En la práctica se aplican técnicas de suavizado (_smoothing_) como Laplace, Good--Turing, Kneser--Ney o interpolated Kneser--Ney para mitigar este problema @chengoodman1999smoothing.
+ *Falta de generalización semántica.* Los modelos de n-gramas tratan a cada palabra como un índice discreto y no capturan ningún tipo de relación semántica, sintáctica o morfológica entre ellas. Palabras semánticamente próximas como _perro_ y _can_ son igualmente "distantes" en el espacio del modelo, lo que impide transferir conocimiento entre términos relacionados.
+ *Dependencia rígida del orden de las palabras.* La probabilidad se calcula sobre secuencias literales de tokens; variantes como _El perro ladra_ y _Ladra el perro_ producen distribuciones completamente diferentes. Esta rigidez torna al modelo muy sensible a la longitud del contexto y al estilo de los textos observados.
+ *Ventana de contexto limitada.* La historia que condiciona la predicción está restringida a los $n - 1$ tokens previos. Para modelar dependencias de mayor alcance (por ejemplo, la concordancia entre sujeto y verbo en oraciones largas, o las correferencias entre párrafos distantes) hacen falta arquitecturas que operen sobre representaciones más ricas, como las que veremos a partir de las redes neuronales recurrentes y, más adelante, los mecanismos de atención y la arquitectura Transformer.

Estas limitaciones motivaron la búsqueda de representaciones distribuidas (como los _word embeddings_) y, posteriormente, de arquitecturas neuronales capaces de capturar dependencias de largo plazo.

=== Sistemas basados en reglas y en recuperación de información

Ya por los años 60, el desarrollo inicial de los asistentes virtuales como los *chatbots* se centró en sistemas estructurados que operaban bajo directrices preprogramadas, es decir, sistemas de reglas escritas a mano por humanos. #cite(<weizenbaum1966>, form: "prose")  presentó a ELIZA, un *chatbot* que emulaba a un psicoterapeuta rogeriano#footnote[
  La terapia rogeriana, también llamada terapia centrada en el cliente, fue desarrollada por el psicólogo estadounidense Carl Rogers en la década de 1940 @rogers1951clientcentered. Se caracteriza por la escucha activa, la empatía incondicional y la reformulación no directiva de los planteos del paciente, condiciones que la vuelven especialmente fácil de simular mediante reglas de coincidencia de patrones.
] mediante técnicas de coincidencia de patrones @mnasri2019 @weizenbaum1966. El programa analiza la consulta del usuario, identifica las palabras clave con mayor jerarquía dentro de su base de conocimientos y ejecuta reglas de transformación contenidas en scripts específicos. El éxito de ELIZA impulsó el desarrollo de arquitecturas similares como PARRY, ALICE, CLEVER y SHRDLU @mnasri2019 @shum2018 @winograd1972. Su principal desventaja radica en que eran sistemas muy básicos, limitados estrictamente a las reglas manuales y bases de datos integradas en sus scripts.

#figure(
  [#align(center)[
    #block(width: 7cm, height: auto)[
      #mermaid(
      "graph TD
       A[Entrada del usuario] --> B[Escaneo izquierda derecha]
       B --> C[Detección y búsqueda de palabras clave]
       C --> D{¿Palabra clave encontrada?}
       D -->|No| E[Responder con frase genérica]
       D -->|Sí| F[Aplicar regla de descomposición y reensamblaje]
       
       linkStyle 3 stroke:#ff0000,stroke-width:2px,color:#ff0000;
       linkStyle 4 stroke:#00aa00,stroke-width:2px,color:#00aa00;
       
       style E fill:#ffe6e6,stroke:#ff0000,stroke-width:2px;
       style F fill:#e6ffe6,stroke:#00aa00,stroke-width:2px;",
      )
    ]
  ]],
  caption: [Flujo de procesamiento de ELIZA. Basado en el mecanismo de descomposición y reensamblaje descrito por @weizenbaum1966.],
) <fig_flujo_eliza>

Otro tipo de *chatbots* son aquellos basados en recuperación de información (Information Retrieval, IR), donde los sistemas formulan respuestas al contrastar los patrones de entrada con pares de solicitud-respuesta ya estructurados en una base de datos de diálogos @jurafsky_martin_2026. Para seleccionar la respuesta óptima, se apoyan en metodologías de recuperación de datos a nivel de palabra tales como TF-IDF, similitud del coseno y modelos de espacio de estados. CleverBot es un referente de esta categoría; fue diseñado a finales de la década de 1980 y difundido formalmente a finales de los años 1990 @mnasri2019.

=== Modelos basados en espacio de vectores y espacio de estados

Los espacios vectoriales constituyen otro pilar fundamental en el desarrollo de los modelos de lenguaje.

Los modelos de espacio de vectores (VSM, por sus siglas en inglés) son enfoques algebraicos que transforman los elementos del lenguaje en vectores dentro de un espacio determinado. La incrustación de palabras (*word embedding*) es el nombre que recibe la técnica de representar palabras mediante vectores. Esta es una estrategia que surgió en la década de 1980 @rumelhart1985 aunque su verdadero auge llegó con investigaciones clave como la de #cite(<bengio2003aneural>, form: "prose"), seguidas por Word2Vec @mikolov2013word2vec y GloVe @pennington2014glove en los años 2010.

#figure(
  [#align(center)[
    #image("../media/word_embeddings_vsm.png", width: 90%)
  ]],
  caption: [Visualización t-SNE de _word embeddings_ generados a partir de literatura del siglo XIX. Los puntos próximos en el plano corresponden a palabras con significado o contexto de uso similar, ilustrando cómo los VSM codifican relaciones semánticas como relaciones geométricas entre vectores @grayson2017tsne.],
) <fig_word_embeddings>

Mientras que los VSM se han aplicado masivamente en el modelado del lenguaje, los modelos de espacio de estados (SSM, por sus siglas en inglés) han comenzado a captar el interés en el campo del procesamiento de lenguaje natural recientemente @gu_dao_2023. Se utilizaban tradicionalmente en la teoría de control y el procesamiento de señales para modelar secuencias de datos, por lo que se destacan por su gran capacidad para gestionar y procesar secuencias de texto muy largas. Por este motivo se perfilan como candidatos ideales para diseñar nuevas arquitecturas y optimizar los modelos de lenguaje actuales. Para más información puede consultar las publicaciones de Mamba de #cite(<gu_dao_2023>, form: "prose").

#figure(
  [#align(center)[
    #image("../media/ssm_mamba.png", width: 100%)
  ]],
  caption: [Diagrama de bloques de un bloque Mamba, una arquitectura de espacio de estados selectivo. Se observa la aplicación de proyecciones lineales, convoluciones y el mecanismo de selección que vuelve a los parámetros del SSM función de la entrada. La recurrencia lineal $h_t = A h_{t-1} + B x_t$ permite procesar secuencias largas en tiempo lineal, a diferencia del costo cuadrático de la atención. Fuente: #cite(<emsi2024mamba>, form: "prose")],
) <fig_ssm>

=== Modelos de lenguaje basados en redes neuronales artificiales

En esta sección repasamos la historia de las redes neuronales artificiales (RNA) y las familias de RNA que han servido como base de modelos de lenguaje más avanzados, en particular las redes neuronales recurrentes (RNN), las de memoria de corto-largo plazo (LSTM), las unidades recurrentes con compuertas (GRU), el mecanismo de atención y la arquitectura Transformer.

==== El perceptrón y las primeras redes neuronales artificiales

Las redes neuronales artificiales (RNA) son estructuras conformadas por elementos de procesamiento simples, densamente interconectados y adaptativos (denominados neuronas artificiales o nodos), capaces de realizar cálculos masivamente paralelos sobre los datos, y que son utilizadas como herramientas de modelado computacional en un amplio abanico de disciplinas para resolver problemas reales complejos @basheer_hajmeer_2000_anns.

*El perceptrón de Rosenblatt.* El modelo fundacional de neurona artificial fue propuesto por #cite(<rosenblatt1958>, form: "prose"), en el marco de una teoría conexionista del cerebro y de los sistemas de aprendizaje. Rosenblatt partió de los trabajos de Hebb sobre la plasticidad sináptica#footnote[
  La regla de Hebb @hebb2005organization postula que la conexión entre dos neuronas se fortalece cuando ambas se activan simultáneamente, ofreciendo la primera base biológica plausible para el aprendizaje en redes neuronales.
] y de los modelos previos de McCulloch y Pitts @mcculloch1943logical, y propuso un sistema de unidades de procesamiento con pesos sinápticos ajustables, organizados en una capa de _proyección_ (sensorial) conectada a una capa de _asociación_ donde se efectúa la suma ponderada de las entradas, cuya salida alimenta una capa final de _respuesta_ @rosenblatt1958. La regla de aprendizaje del perceptrón modifica los pesos en proporción al error entre la salida obtenida y la deseada, siempre que los datos sean linealmente separables. Esta restricción resultó crucial: Minsky y Papert demostraron  que un perceptrón de una sola capa no podía resolver problemas no linealmente separables como la función lógica XOR @minsky2017perceptrons, lo que provocó lo que se conoce como el _invierno de las redes neuronales_ y frenó la financiación del campo durante más de una década @russell2020artificial.

*Organización en capas y perceptrones multicapa.* La limitación anterior se superó intercalando una o más _capas ocultas_ entre la entrada y la salida, dando lugar a los perceptrones multicapa (MLP) @rumelhart1986parallel. Cada capa oculta aplica una transformación no lineal a la representación de la capa anterior, de modo que la composición de varias no linealidades permite aproximar funciones arbitrariamente complejas (esto es formalizado más tarde por el _teorema de aproximación universal_ de #cite(<cybenko1989approximation>, form: "prose") y #cite(<hornik1989multilayer>, form: "prose")). Sin embargo, durante muchos años no se contó con un algoritmo eficiente para ajustar los pesos de todas las capas de manera conjunta @rumelhart1986learning.

*Backpropagation.* La solución llegó de la mano del algoritmo de _retropropagación_ (_backpropagation_), popularizado por Rumelhart, Hinton y Williams en 1986 @rumelhart1986learning. La idea central es propagar el error cometido en la salida hacia atrás, capa por capa, calculando para cada peso la derivada parcial de la pérdida con respecto a ese peso mediante la regla de la cadena. Combinado con un método de optimización basado en gradiente descendente, backpropagation permite entrenar MLP con varias capas ocultas de manera eficiente, y constituye hasta hoy la columna vertebral del aprendizaje profundo. La popularización de backpropagation se considera el hito que dio inicio, ya entrada la década de 2010, al _deep learning_ moderno @lecun2015deep.

A continuación se describen los mecanismos fundamentales que rigen el funcionamiento de las RNA @basheer_hajmeer_2000_anns, integrando los conceptos introducidos por Rosenblatt y Rumelhart, Hinton y Williams @rosenblatt1958 @rumelhart1986learning:

+ *Neurona artificial (modelo tipo perceptrón).* Recibe $n$ señales de entrada $x_i$ con sus respectivos pesos sinápticos $w_i$. Calcula la entrada neta como el producto interno:

  $ j = sum_(i=1)^n w_i x_i $

  La salida $y$ se obtiene aplicando una función de activación (en el perceptrón clásico, un umbral lineal con sesgo $b$): la neurona se "dispara" (por ejemplo, $y = 1$) solo cuando $j > b$, y permanece inactiva ($y = 0$) en caso contrario.

+ *Pesos excitatorios e inhibitorios.* Pesos positivos ($w_i > 0$) potencian la entrada neta y excitan a la neurona; pesos negativos la reducen e inhiben su actividad.

+ *Arquitectura multicapa (MLP).* Para resolver problemas no linealmente separables se intercalan una o más capas ocultas entre la capa de entrada y la de salida. Las neuronas ocultas procesan la información proveniente de la entrada y la transmiten a la capa de salida.

  #figure(
    [#align(center)[
      #image("../media/red_neuronal_mlp.svg", width: 90%)
    ]],
    caption: [Ejemplo esquemático de una red neuronal artificial multicapa (MLP). Se observan la capa de entrada (a la izquierda), una capas ocultas de neuronas interconectadas y la capa de salida (a la derecha). Cada conexión entre neuronas tiene un peso sináptico asociado, y la información fluye estrictamente hacia adelante (_feed-forward_). Fuente: #cite(<diagrama_rna_2026>, form: "prose")],
  ) <fig_mlp_ejemplo>

+ *Aprendizaje.* Tanto la red biológica como la artificial ajustan incrementalmente la magnitud de los pesos. En el perceptrón simple, los pesos se modifican en proporción al error entre la salida deseada $Y$ y la obtenida $y$. En los MLP, este ajuste se realiza típicamente mediante el algoritmo de *retropropagación* (*backpropagation*) con la regla delta, que busca (mediante una técnica de búsqueda especializada) el conjunto de pesos que minimiza el error.
+ *Objetivo.* Desarrollar algoritmos matemáticos que permitan a las RNA aprender imitando el procesamiento de información y la adquisición de conocimiento del cerebro humano, aunque sin pretender replicar la operación del sistema biológico, sino aprovechar lo que se conoce de su funcionalidad para resolver problemas complejos.

==== Redes neuronales recurrentes (RNN)

Tras los modelos estadísticos y los basados en reglas, cobraron protagonismo los modelos de lenguaje sustentados en redes neuronales artificiales. Dentro de este grupo, las redes neuronales recurrentes (RNN) han tenido un rol central. Surgieron en la década de 1980 @hopfield1982 @rumelhart1985 @jordan1997 @elman1990 y se concibieron como una clase de redes orientadas al procesamiento de datos secuenciales y series temporales. Su aporte al desarrollo de modelos de lenguaje fue considerable, aunque muestran un desempeño limitado cuando las secuencias presentan dependencias de largo alcance @bengio1994. Una de sus restricciones más conocidas es la aparición del gradiente evanescente#footnote[
  El _gradiente evanescente_ (_vanishing gradient_) describe el fenómeno por el cual, durante el entrenamiento de redes profundas mediante retropropagación, los gradientes de la pérdida con respecto a los pesos de las capas iniciales se vuelven extremadamente pequeños a medida que la señal se propaga hacia atrás. Esto hace que esos pesos apenas se actualicen y la red no logre aprender dependencias de largo plazo en secuencias largas. El problema fue analizado formalmente por #cite(<hochreiter1998>, form: "prose").
] y del gradiente explosivo#footnote[
  El _gradiente explosivo_ (_exploding gradient_) es el fenómeno opuesto: durante la retropropagación los gradientes crecen de manera descontrolada a través de las capas, provocando actualizaciones de peso enormes que vuelven el entrenamiento inestable. Suele aparecer cuando la matriz de pesos recurrentes tiene valores propios mayores que uno en valor absoluto. #cite(<pascanu2013>, form: "prose") propusieron una solución práctica, el _gradient clipping_, que limita la norma del gradiente a un umbral máximo cuando se supera.
]. Estas limitaciones impulsaron la búsqueda de arquitecturas alternativas capaces de tratar secuencias extensas con mayor eficacia.

#figure(
  [#align(center)[
    #image("../media/rnn_arquitectura.svg", width: 100%)
  ]],
  caption: [Red neuronal recurrente (RNN) desplegada en el tiempo. La misma red (con pesos compartidos) se aplica en cada paso de la secuencia: el estado oculto $h_t$ depende tanto de la entrada actual $x_t$ como del estado anterior $h_{t-1}$, lo que le da a la red memoria de los pasos previos. Fuente: #cite(<diagrama_rnn_unfold_2026>, form: "prose")],
) <fig_rnn_arquitectura>

==== Memorias de corto y largo plazo (LSTM)

Las redes de memoria a corto y largo plazo (LSTM, por sus siglas en inglés) son un tipo particular de red neuronal recurrente que aborda de manera más satisfactoria el problema de las dependencias de largo plazo. Introducidas por  #cite(<hochreiter_schmidhuber_1997>, form: "prose"), su objetivo principal fue mitigar el problema del gradiente evanescente que afecta a las RNN. Una LSTM se compone de una celda de memoria y tres compuertas: de entrada, de salida y de olvido. La compuerta de olvido es la que determina qué información se conserva a lo largo del tiempo, regulando así la memoria de corto o largo plazo. Aunque las LSTM resuelven limitaciones de las RNN básicas, esta mejora tiene un costo: las LSTM son más complejas, requieren más parámetros, su entrenamiento resulta computacionalmente más caro, demanda más tiempo y necesita una mayor cantidad de datos de entrenamiento.

#figure(
  [#align(center)[
    #image("../media/lstm_celda.svg", width: 100%)
  ]],
  caption: [Estructura interna de una celda LSTM. Se observan las tres compuertas: de olvido ($f_t$), de entrada ($i_t$) y de salida ($o_t$), que controlan respectivamente qué información se descarta, qué nueva información se incorpora y qué parte del estado de la celda $C_t$ se propaga como salida. Fuente: #cite(<diagrama_lstm_2017>, form: "prose")],
) <fig_lstm_celda>


==== Unidades recurrentes con compuertas (GRU)

Las unidades recurrentes con compuertas (GRU, por sus siglas en inglés) fueron presentadas por #cite(<cho2014>, form: "prose") como otro intento por resolver el problema del gradiente evanescente en las RNN. Las GRU comparten con las LSTM la idea de incorporar compuertas para lidiar con esta dificultad; sin embargo, las GRU solo cuentan con dos: una compuerta de actualización y una de reinicio. Además, a diferencia de las LSTM, no disponen de una celda de memoria adicional. Esta arquitectura más simple se traduce en un menor número de parámetros y, en consecuencia, en un entrenamiento más rápido. No obstante, tanto las LSTM como las GRU presentan ventajas y desventajas, por lo que la elección entre una y otra depende de la aplicación y del contexto. En particular, las LSTM tienden a desempeñarse mejor en tareas con dependencias de largo plazo marcadas.

#figure(
  [#align(center)[
    #image("../media/gru_celda.svg", width: 100%)
  ]],
  caption: [Estructura interna de una celda GRU. A diferencia de la LSTM, la GRU combina las compuertas de entrada y olvido en una sola _compuerta de actualización_ $z_t$, y agrega una _compuerta de reinicio_ $r_t$ que controla cuánta información del pasado se descarta. No hay una celda de memoria separada: el estado oculto $h_t$ integra la información directamente. Fuente: #cite(<diagrama_gru_2017>, form: "prose").],
) <fig_gru_celda>

=== La arquitectura Transformer

El Transformer, introducido por #cite(<vaswani2017>, form: "prose"), representa un cambio de paradigma frente a las arquitecturas recurrentes. A diferencia de las RNN y LSTM, que procesan secuencias de manera secuencial, el Transformer se basa enteramente en mecanismos de atención, lo que permite el procesamiento paralelo de todos los tokens de una secuencia simultáneamente. Esta propiedad, sumada a la posibilidad de entrenar a gran escala sobre hardware masivamente paralelo (GPUs y TPUs), es la principal razón por la que el Transformer se convirtió en la arquitectura dominante del PLN desde 2017 @tunstall2022natural.

*Arquitectura encoder--decoder.* El Transformer original se organiza en dos mitades simétricas. El _encoder_ recibe la secuencia de entrada y produce, para cada token, una representación contextual que incorpora información de todos los demás tokens. El _decoder_ genera la secuencia de salida token a token, consumiendo tanto la salida del encoder como los tokens previamente generados. Cada mitad es una pila de bloques que se compone, básicamente, de dos sub-capas: una de atención multi-cabezal seguida de una red _feed-forward_ posición por posición, con conexiones residuales y normalización de capa.

*Mecanismo de atención escalada (scaled dot-product attention).* Para cada posición de la secuencia se proyectan tres vectores a partir de su representación de entrada: una _query_ ($q$), una _key_ ($k$) y un _value_ ($v$). La atención entre una query y todas las keys se calcula como la similitud coseno escalada:

$ "Attention"(Q, K, V) = "softmax"((Q K^T) / sqrt(d_k)) V $

donde $d_k$ es la dimensión de las keys. Intuitivamente, la query representa la pregunta _¿a qué tokens de la entrada debería prestarle atención esta posición?_, las keys representan _identificadores_ contra los que se compara esa pregunta, y los values son la _información_ que efectivamente se agrega a la representación de la posición actual, ponderada por la similitud query-key @vaswani2017.

*Multi-head attention.* En lugar de aplicar una única atención, el Transformer aprende $h$ proyecciones independientes de $Q$, $K$ y $V$ y aplica la atención escalada en paralelo sobre cada una. Las salidas se concatenan y se proyectan de nuevo. Esta _multi-cabezal_ permite que cada cabeza aprenda a atender a distintos tipos de relaciones: una cabeza puede especializarse en la dependencia sintáctica sujeto--verbo, otra en correferencias, otra en la posición local, etc. Formalmente:

$ "MultiHead"(Q, K, V) = "Concat"("head"_1, ..., "head"_h) W^O $
$ "donde" "head"_i = "Attention"(Q W_i^Q, K W_i^K, V W_i^V) $

*Positional encoding.* Como la atención opera sobre conjuntos y no sobre secuencias, el Transformer no tiene noción intrínseca del orden de los tokens. Para reintroducir esa información se suma a cada embedding de token un _positional encoding_, una señal posicional de la misma dimensión. En el paper original se propuso una combinación de funciones sinusoidales de distintas frecuencias, lo que permite al modelo extrapolar a longitudes de secuencia no vistas durante el entrenamiento. Variantes más modernas como ALiBi @press2022train y RoPE (_Rotary Position Embedding_) @su2024roformer codifican la posición relativa directamente dentro del cómputo de la atención y son habituales en LLMs contemporáneos.

*Máscara causal en el decoder.* Para que el decoder pueda entrenarse de forma paralela sobre toda la secuencia de salida (en lugar de estrictamente token a token), se aplica una _máscara causal_ sobre la matriz de atención que impide a cada posición atender a tokens futuros. El resultado es la _masked multi-head self-attention_, que es la operación central de los modelos generativos tipo GPT @radford2018improving.

=== Modelos fundacionales basados en Transformer

A partir de la arquitectura Transformer surgieron los grandes modelos de lenguaje (LLM, por sus siglas en inglés), entrenados a partir de corpus de texto de escala masiva. Dos familias principales dominaron el panorama inicial:

- *BERT* @devlin2018bert: modelo bidireccional basado exclusivamente en el *encoder* del Transformer, optimizado para tareas de extracción y comprensión de información a partir de texto.
- *GPT* @radford2018improving: modelo unidireccional basado en el *decoder* del Transformer, especializado en la predicción y generación de secuencias de texto.

Estas arquitecturas dieron origen a diversas familias de LLMs como GPT, PaLM, LLaMA, entre otras, que se han convertido en la columna vertebral del PLN moderno. Para una revisión exhaustiva, consultar #cite(<zhao2026surveySpringer>, form: "prose").

// Quita la numeración de los sub-headers de "Innovaciones recientes" (los años)
// Configura el nivel 4 (====) sin numeración, solo con cuerpo en negrita.
#show heading.where(level: 4): it => {
  text(weight: "bold", it.body)
}



=== Innovaciones recientes en modelos de lenguaje

A partir del transformer la investigación en los modelos se aceleró cada vez más, en esta sección se presenta una cronología de hitos relevantes en la evolución de los LLMs, desde 2022 hasta el momento de cierre del marco teórico de este trabajo (segundo semestre de 2025).

#let eventos_evolucion_llm_3 = (
  (date: "2022", desc: [Wei y colaboradores documentan las *capacidades emergentes* @wei2022emergent; *InstructGPT* introduce RLHF @ouyang2022instructgpt; *Constitutional AI* propone retroalimentación generada por IA @bai2022constitutional; *ChatGPT* populariza el acceso masivo a LLMs @openai2022chatgpt.]),
  (date: "2023", desc: [*GPT-4* @openai2023gpt4 introduce arquitectura MoE; *Claude* @anthropic2023claude enfatiza seguridad; *Toolformer* @schick2023toolformer y *Function Calling* incorporan herramientas externas.]),
  (date: "2024", desc: [*OpenAI o1* @openai2024o1 mejora el razonamiento mediante cadenas de pensamiento internas; *DeepSeek-V3* @deepseek2024v3 y *DeepSeek-R1* @deepseek2025r1 demuestran que el RL sin supervisión humana compite con RLHF.]),
  (date: "2025", desc: [*GPT-4.5* @openai2025gpt45, *Claude 4* y *Claude Code* @anthropic2025claude4, *Codex* @openai2025codex y *GPT-5* @openai2025gpt5 consolidan los agentes de programación autónoma y la siguiente generación de modelos fundacionales.]),
)

#figure(
  timeline(
    eventos_evolucion_llm_3,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 11pt,
        body: 9pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.4em,
        arm:  2.6em,
      ),
    ),
  ),
  caption: [Cronología de los hitos principales en la evolución de los modelos del lenguaje (2022--2025). Tercera parte.],
) <fig_evolucion_llms_3>

==== Año 2022

- *Emergent Abilities of Large Language Models* @wei2022emergent: Wei y colaboradores documentaron que ciertas capacidades de los modelos de lenguaje —resolución de problemas aritméticos simples, comprensión lectora de varios pasos, decodificación de instrucciones compuestas, razonamiento por analogías, entre otras— aparecen de manera discontinua y no predecible a partir de cierto umbral de escala (número de parámetros y de datos de entrenamiento). Estas _capacidades emergentes_ no se observan en modelos pequeños ni pueden extrapolarse linealmente desde su comportamiento, lo que sugiere que los LLMs no son simplemente una versión _a mayor escala_ de sus contrapartes pequeñas, sino que en cierto régimen de tamaño exhiben habilidades cualitativamente nuevas. La caracterización rigurosa de este fenómeno abrió una línea de investigación muy activa sobre sus condiciones, límites e implicaciones para la seguridad y la interpretabilidad de los modelos.
- *InstructGPT* @ouyang2022instructgpt: entrenamiento de modelos de lenguaje para seguir instrucciones con retroalimentación humana (RLHF, por sus siglas en inglés).
- *Constitutional AI* @bai2022constitutional: método para entrenar asistentes inofensivos mediante retroalimentación generada por la propia IA.
- *ChatGPT* (noviembre 2022) @openai2022chatgpt: lanzamiento público que popularizó el acceso masivo a los LLMs. Este hito puede entenderse como una manifestación a gran escala de las capacidades emergentes descritas por @wei2022emergent: aunque los modelos GPT-3 de acceso programático ya exhibían buena parte de esas habilidades, fue la interfaz conversacional de ChatGPT la que las volvió evidentes para el público general. En la práctica, ChatGPT demostró que modelos entrenados primariamente para predecir el siguiente token eran capaces de seguir instrucciones matizadas, mantener el contexto a lo largo de un diálogo, rechazar pedidos inapropiados y producir texto de apariencia humana en una amplia variedad de dominios —capacidades para las que no habían sido entrenados de forma explícita. Este comportamiento, interpretado a la luz del trabajo de Wei y colaboradores, reforzó la idea de que las capacidades emergentes no son un artefacto de evaluación, sino una propiedad intrínseca de los modelos suficientemente grandes.

==== Año 2023

- *GPT-4* @openai2023gpt4: modelo multimodal con arquitectura *Mixture of Experts* (MoE), cuyos orígenes se remontan a @jacobs1991moe y @shazeer2017moe.
- *Claude* (marzo 2023) @anthropic2023claude: asistente desarrollado por Anthropic con énfasis en seguridad y alineamiento.
- *Toolformer* @schick2023toolformer y *OpenAI Function Calling*: incorporación de uso de herramientas externas por parte de los LLMs.

==== Años 2024 y 2025

- *OpenAI o1* @openai2024o1: modelo con capacidades de razonamiento mejoradas mediante cadenas de pensamiento internas.
- *DeepSeek-V3* @deepseek2024v3 y *DeepSeek-R1* @deepseek2025r1: modelos que demostraron que el aprendizaje por refuerzo sin supervisión humana —con técnicas como GRPO (*Group Relative Policy Optimization*)— puede alcanzar calidad comparable al estado del arte a un costo significativamente menor.
- *GPT-4.5* (febrero 2025) @openai2025gpt45: iteración avanzada de la familia GPT.
- *Claude 4* y *Claude Code* (mayo 2025) @anthropic2025claude4: agentes de larga ejecución con capacidades de programación autónoma.
- *Codex* (mayo 2025) @openai2025codex: agente de programación de OpenAI.
- *GPT-5* (agosto 2025) @openai2025gpt5: siguiente generación de modelos fundacionales.

==== Desarrollos posteriores al alcance de este trabajo

Desarrollos posteriores a septiembre de 2025 enfatizan el harness engineering para co-diseñar entornos de control y andamiajes de agentes, superando la ingeniería de prompts tradicional @hashimoto2026harness @anthropic2025harness.

Paralelamente, el local-first AI se posiciona como estándar para la soberanía de datos, ejecutando modelos de frontera directamente en el hardware del cliente o infraestructura periférica @cruzes2026sovereignty @ibm2026sovereignty.

== Síntesis del capítulo

A lo largo de este capítulo se ha trazado la evolución del procesamiento de lenguaje natural desde sus orígenes estadísticos hasta los grandes modelos de lenguaje contemporáneos. Se partió de los modelos de n-gramas fundados en los trabajos de Markov y Shannon, se revisaron los sistemas basados en reglas y recuperación de información como ELIZA, y se introdujeron los espacios vectoriales y de estados como representaciones distribuidas del lenguaje. Posteriormente, se describió el desarrollo de las redes neuronales artificiales —desde el perceptrón de Rosenblatt y el algoritmo de _backpropagation_ hasta las redes recurrentes, LSTM y GRU— que culminó en la arquitectura Transformer, basada enteramente en mecanismos de atención. Finalmente, se presentó una cronología de las innovaciones recientes (2022--2025), incluyendo las capacidades emergentes, el alineamiento mediante RLHF, el razonamiento encadenado y los agentes de programación autónoma.

Esta progresión sienta las bases técnicas necesarias para abordar la aplicación del PLN a dominios especializados. En particular, el dominio legal presenta desafíos propios —vocabulario técnico, razonamiento normativo y estructuras documentales extensas— que motivan el desarrollo de sistemas de recuperación aumentada y agentes capaces de operar sobre corpus jurídicos. Estos temas se abordan en el siguiente capítulo, dedicado a la aplicación del PLN al dominio legal.