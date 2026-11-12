#set page(paper: "a4", margin: 2cm)
#set text(font: "New Computer Modern", size: 10pt, lang: "es")
#set par(justify: true)

= Prueba de citas estadísticas

Este documento compila las 19 entradas de `citas_estadisticas.bib` y sirve para
verificar que el archivo BibTeX es sintácticamente válido y que Typst puede
resolver todas las claves.

#cite(<mccullagh1980>) #cite(<agresti2010>) #cite(<laird1982>) #cite(<wilks1938>)
#cite(<akaike1974>) #cite(<friedman1937>) #cite(<kendall1939>) #cite(<wilcoxon1945>)
#cite(<cureton1956>) #cite(<efron1979>) #cite(<field2007>) #cite(<searle1980>)
#cite(<holm1979>) #cite(<christensen2026ordinal>) #cite(<lenth2026emmeans>)
#cite(<venables2002>) #cite(<virtanen2020scipy>) #cite(<seabold2010statsmodels>)
#cite(<rcore2026>)

#bibliography("citas_estadisticas.bib", title: [Referencias], style: "apa")
