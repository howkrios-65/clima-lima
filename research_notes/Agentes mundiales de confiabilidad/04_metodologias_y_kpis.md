# Metodologías de ingeniería de confiabilidad y KPIs de mantenimiento (fichas comparables)

## 0. Estado de acceso y regla de evidencia (LEER PRIMERO)

- WebFetch devolvió `getaddrinfo ENOTFOUND` para: apps.dtic.mil, qualitysafety.bmj.com, reliamag.com, en.wikipedia.org, weibull.com, reliasoft.com, smrp.org.
- curl desde Bash con el proxy: `CONNECT tunnel failed, response 403` para apps.dtic.mil, qualitysafety.bmj.com, pmc.ncbi.nlm.nih.gov, reliamag.com, wikipedia. El proxy opera con lista de dominios permitidos. No hubo URL alternativa que abriera.
- Consecuencia: NINGUNA fuente fue abierta en texto completo. Todo lo "citado" viene de resúmenes de WebSearch, por eso el estado máximo es SOLO-SNIPPET. Nada es VERIFICADO.
- Lo marcado NO-VERIFICADO / "síntesis propia" viene de conocimiento previo del investigador, sin fuente abierta. El redactor debe tratarlo como hipótesis a confirmar, no como cita.
- No se registra ninguna cifra de efectividad ("reduce X%") como evidencia: ninguna fuente primaria fue abierta.
- Varias fuentes de snippets son blogs de proveedores (reliamag.com, oxmaint, fabrico, tractian, metricgate). Son secundarias y de baja autoridad.
- Fuera de alcance de esta pasada: ningún estándar (IEC 60812, SAE JA1011, EN 15341, ISO 22400, ISO 14224, API 580/581) se leyó en su texto; solo resúmenes de catálogo.

---

## 1. RCA / ACR (PROACT, TapRooT, Apollo, 8D, RCFA, 5 Porqués, Ishikawa, FTA)

### Takeaway
IEC 62740 es el estándar marco de RCA: define principios, pasos mínimos y atributos para elegir técnica, solo para eventos ya ocurridos y sin asignar culpa. La crítica publicada más sólida y localizada sobre el 5 Porqués es Card 2017 (BMJ Qual Saf); la comparación PROACT/TapRooT/Apollo solo se halló en material de proveedor.

### Cited Findings
- IEC 62740:2015 describe los principios básicos del RCA y especifica los pasos que un proceso de RCA debe incluir. Identifica atributos de técnicas RCA para ayudar a elegir y describe fortalezas y debilidades de cada una. No busca asignar responsabilidad. Se centra en análisis de eventos ocurridos. Adoptada como EN 62740:2015. Estado: SOLO-SNIPPET — [VDE preview](https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec62740{ed1.0}b.pdf), [GSO](https://www.gso.org.sa/store/standards/GSO:746299/GSO%20IEC%2062740:2017), [Genorma](https://genorma.com/en/standards/en-62740-2015)
- Card (2017), "The problem with '5 whys'", BMJ Qual Saf 26(8):671-677, doi:10.1136/bmjqs-2016-005849. Según resúmenes: su popularidad no proviene de evidencia de eficacia; simplifica problemas complejos; depende de deducción "off-the-cuff" en vez de observación; el punto de parada es arbitrario (la respuesta correcta puede estar en el 2.º o 7.º porqué); se valora como herramienta pedagógica. Estado: SOLO-SNIPPET — [BMJ](https://qualitysafety.bmj.com/content/26/8/671), [PSNet](https://psnet.ahrq.gov/issue/problem-5-whys), [ECRI](https://www.ecri.org/search-results/member-preview/ccrm/pages/iiccrm081117_should/). Un directorio de skills atribuye a Card la prescripción de árboles causales ramificados; no confirmado.
- TapRooT: proceso de 7 pasos; pasos 1-2 reúnen y organizan hechos, 3-5 identifican causas raíz y mejores prácticas faltantes, paso 6 acciones correctivas. Autodescripción del proveedor. Estado: SOLO-SNIPPET — [TapRooT PDCA](https://taproot.com/how-does-taproot-process-fit-into-pdca-cycle/)
- PROACT: descrito solo en texto promocional como proceso robusto contrastado con 5-whys/fishbone (que "pueden aplicarse mal bajo presión de tiempo"). Fases no obtenidas. Estado: SOLO-SNIPPET — [reliability.com](https://reliability.com/?p=1951)
- Apollo RCA: ningún resultado cubrió sus pasos.
- Existe un hilo comparativo PROACT/TapRooT/Apollo (foro de proveedor), no leído en detalle — [oxmaint](https://community.oxmaint.com/discussion-forum/pros-and-cons-of-proact-taproot-and-apollo-a-comprehensive-review-of-rcfa-software). NO-VERIFICADO.

### Ficha comparativa (columnas "síntesis propia / NO-VERIFICADO" salvo donde se cita arriba)

| Método | Propósito | Pasos típicos | Fortalezas | Debilidades / críticas | Norma/fuente | Estado |
|---|---|---|---|---|---|---|
| 5 Porqués | Cadena causal rápida para problemas simples | Preguntar "por qué" iterativamente hasta causa accionable | Simple, didáctico | Parada arbitraria, deducción sin evidencia, lineal (Card 2017) | IEC 62740 lo cubre entre técnicas (no confirmado cuáles) | Crítica: SOLO-SNIPPET; pasos: NO-VERIFICADO |
| Ishikawa | Organizar causas potenciales por categoría | Definir efecto, categorías (6M), lluvia de ideas | Estructura la lluvia de ideas | Produce hipótesis, no causas verificadas (síntesis propia) | — | NO-VERIFICADO |
| FTA | Lógica booleana de combinaciones de causas | Evento tope, compuertas AND/OR, eventos básicos | Cuantificable, muestra redundancias | Requiere experticia y datos; estático (síntesis propia) | IEC 61025 (conocimiento previo) | NO-VERIFICADO |
| PROACT | Programa RCA completo con evidencia (5P: Preservar, Ordenar, Analizar, Comunicar, Evaluar) | Árbol lógico con hipótesis verificadas | Verificación de hipótesis con evidencia | Consume recursos; fases no confirmadas aquí | Reliability Center | SOLO-SNIPPET (existencia), resto NO-VERIFICADO |
| TapRooT | Investigación estructurada con árbol de causas raíz y tabla de causas | 7 pasos (ver arriba) | Estandarizado, enfoque en factores humanos | Proveedor-céntrico, licencia | taproot.com | SOLO-SNIPPET parcial |
| Apollo RCA | Mapa de causa-efecto con evidencia para cada causa | — | — | — | — | NO-VERIFICADO (sin fuente hallada) |
| 8D | Resolución de problemas de calidad con contención | D0-D8 | Contención + acción permanente | Orientado a no-conformidades | — | NO-VERIFICADO |
| RCFA | Término genérico de análisis causal de fallas | — | — | — | — | NO-VERIFICADO |

### Inferences
- El 5 Porqués es defendible solo como técnica de entrada, con evidencia y ramificación; el intake debe preguntar qué evidencia respalda cada "porqué".
- Un agente no debe afirmar que PROACT "reduce X%" ni similar: no se encontró fuente primaria.

### Gaps
- Pasos oficiales de PROACT y Apollo, métricas de un programa RCA (p. ej., % de acciones cerradas, recurrencia) y la lista de técnicas dentro de IEC 62740: no accesibles.
- Evidencia empírica comparativa entre métodos RCA: no encontrada.

---

## 2. FMEA / FMECA (IEC 60812, MIL-STD-1629A, AIAG-VDA 2019)

### Takeaway
AIAG-VDA 2019 sustituye el RPN por Action Priority (tabla H/M/L que prioriza Severidad, luego Ocurrencia, luego Detección); el motivo citado en fuentes secundarias es que multiplicar escalas ordinales puede ocultar severidades altas. Las fuentes oficiales del handbook no se abrieron.

### Cited Findings
- AIAG-VDA elimina el RPN y usa tabla de Action Priority que lee S, O y D juntos y da prioridad Alta/Media/Baja. Razones según artículos secundarios: la multiplicación permite que una detección baja compense una severidad alta; las escalas son ordinales, por lo que multiplicarlas es estadísticamente inapropiado. Ejemplo: S10/O2/D5, S2/O5/D10 y S4/O5/D5 dan todos RPN=100. AP prioriza severidad, luego ocurrencia, luego detección. Costo: más complejidad y tiempo. Estado: SOLO-SNIPPET — [Pharmaceutical Online](https://www.pharmaceuticalonline.com/doc/is-it-time-to-say-goodbye-to-fmea-risk-priority-number-rpn-scores-0001), [UKLO paper](https://eprints.uklo.edu.mk/id/eprint/6566/)
- Guía "How to Perform FMEA" de reliamag: existe pero no se pudo abrir — [reliamag](https://reliamag.com/guides/how-to-perform-fmea/). NO-VERIFICADO.

### Ficha (síntesis propia, NO-VERIFICADO)
- Propósito: identificar modos de falla, efectos y causas, y priorizar acciones. FMECA añade criticidad (MIL-STD-1629A usa número de criticidad por modo e ítem; IEC 60812 cubre FMEA/FMECA, con RPN o matrices).
- Pasos: alcance/límites; funciones; modos de falla; efectos (local/siguiente/final); causas; controles actuales; S/O/D; priorización; acciones; reevaluación.
- Datos de entrada: diagramas, BOM, historial de fallas, modos conocidos, condiciones operativas, criterios de severidad aprobados.
- Errores comunes: llenar FMEA sin datos de campo; promediar S/O/D; escala sin calibrar; FMEA "de escritorio" hecho una vez; confundir causa con modo.
- Calibración S/O/D (síntesis): anclar cada nivel de la escala a consecuencias y frecuencias observables de la planta; acordar la escala antes de puntuar; revisar con datos históricos.

### Gaps
- Textos de IEC 60812 y MIL-STD-1629A (cambio de edición, fórmula de criticidad Cm), tablas AP oficiales y literatura crítica del RPN (p. ej., Bowles) no abiertos.

---

## 3. RCM (RCM II, SAE JA1011/JA1012, streamlined)

### Takeaway
SAE JA1011 fija los criterios mínimos para que un proceso se llame RCM: siete preguntas y jerarquía de tareas; no prescribe metodología. Nowlan & Heap 1978 (AD-A066579) es la fuente original de los seis patrones de falla.

### Cited Findings
- JA1011 define resultados mínimos y las siete preguntas: funciones, fallas funcionales, modos de falla, efectos, consecuencias, tareas proactivas, acciones por defecto. JA1012 es la guía de aplicación. Consecuencias: ocultas, seguridad/ambiente, operacionales, no operacionales. Tareas: on-condition, restauración programada, descarte programado; por defecto: búsqueda de fallas, rediseño, correr a falla. Un blog indica revisión de noviembre 2024 (no confirmado). Estado: SOLO-SNIPPET — [Tractian](https://tractian.com/en/glossary/sae-ja1011), [reliamag RCM](https://reliamag.com/guides/how-to-perform-rcm/)
- Nowlan & Heap (1978), Reliability-Centered Maintenance, AD-A066579, informe para United Airlines con patrones A-F de probabilidad condicional de falla (Exhibit 2.13). Los porcentajes por patrón varían entre sitios (p. ej., 4% para el patrón A, 89% sin zona de desgaste) y no fueron contrastados con el original. Estado: SOLO-SNIPPET para identidad; porcentajes NO-RASTREABLES aquí — [reliamag patrones](https://reliamag.com/guides/six-failure-patterns-nowlan-heap/)

### Ficha (síntesis propia, NO-VERIFICADO)
- Críticas/condiciones de éxito: alto consumo de tiempo del equipo multidisciplinario; riesgo de análisis genérico sin datos; exige facilitador entrenado, apoyo gerencial y proceso de implementación y auditoría de tareas.
- Streamlined/RCM simplificado: reduce el análisis (p. ej., partir de modos de falla existentes); riesgo de saltarse JA1011.

### Gaps
- Texto de JA1011/JA1012, texto de Moubray, evidencia de costo-beneficio de RCM: no abiertos.

---

## 4. RBI / criticidad / matrices de riesgo / bad actors

### Takeaway
API 580 da principios de RBI; API 581 los métodos cuantitativos. La crítica más citada de matrices de riesgo es Cox (2008, Risk Analysis): baja resolución, compresión de rango y errores de ranking.

### Cited Findings
- API 580 introduce principios y guías mínimas de RBI; API 581 da cálculos cuantitativos de probabilidad y consecuencia para generar plan de inspección por equipo; origen: JIP de API iniciado en 1994 para apoyar el elemento de integridad mecánica de PSM. Ediciones en conflicto entre fuentes (3.ª 2019 vs 4.ª 2025). Estado: SOLO-SNIPPET — [Inspectioneering](https://inspectioneering.com/journal/2012-11-01/2980/risk-based-inspection-program-), [OVISS](https://oviss.jp/view/item/000000001157)
- Cox (2008), "What's Wrong with Risk Matrices?": las matrices comparan correctamente una fracción pequeña de pares (p. ej., menos del 10%), asignan igual rating a riesgos muy distintos (range compression), pueden dar mayor rating a un riesgo cuantitativamente menor; con correlación negativa probabilidad-impacto, el ranking puede ser peor que al azar. Estado: SOLO-SNIPPET (vía resúmenes) — [Wikipedia](https://en.wikipedia.org/wiki/Risk_matrix), [Eight to Late](https://eight2late.com/2009/07/01/cox%e2%80%99s-risk-matrix-theorem-and-its-implications-for-project-risk-management)

### Síntesis propia (NO-VERIFICADO)
- NORSOK Z-008 (criticidad en mantenimiento) y análisis de bad actors (Pareto por frecuencia/costo/horas de parada): no se obtuvieron fuentes. Trampas: Pareto sobre una sola métrica; ignorar que los "malos actores" suelen concentrar fallas repetidas por causa común; Pareto sin normalizar por población de activos.

### Gaps
- NORSOK Z-008, sesgos cognitivos documentados en matrices, estudios de bad actors: sin fuentes.

---

## 5. CBM, P-F, optimización de PM, planificación

### Takeaway
La regla de inspeccionar a menos de la mitad del intervalo P-F se atribuye a RCM II (Moubray) en fuentes secundarias; existen variantes más estrictas. No se confirmó que ISO 17359 prescriba una fracción.

### Cited Findings
- Regla de la mitad (ej. P-F de 12 semanas, ruta cada 6 semanas) atribuida a Moubray RCM II; otra fuente sugiere 1/2 a 1/3, y 1/4 a 1/5 para críticos, buscando al menos dos oportunidades de detección; el P-F varía por tipo de activo, ambiente e incluso entre activos iguales; ISO 17359 se menciona solo para emparejar método de detección con indicadores tempranos. Estado: SOLO-SNIPPET — [reliamag P-F](https://reliamag.com/articles/what-is-a-p-f-curve/), [Ludeca](https://ludeca.com/blog/condition-monitoring-2/6004/how-do-you-set-your-condition-monitoring-intervals/), [ReliaSoft Hotwire 76](https://help.reliasoft.com/articles/content/hotwire/issue76/hottopics76.htm)

### Gaps
- "Fake PM", wrench time, backlog: sin fuentes. Límites de CBM (fallas sin P-F detectable, patrones aleatorios): solo síntesis propia.

---

## 6. Estadística (Weibull, Crow-AMSAA, supervivencia, RAM/Monte Carlo)

### Takeaway
Weibull modela tiempo hasta la primera falla de ítems no reparables; Crow-AMSAA (NHPP, ley de potencia) modela la intensidad de fallas de sistemas reparables. Aplicar Weibull a equipos reparados puede inducir a error.

### Cited Findings
- Crow-AMSAA: NHPP con intensidad ρ(t)=λβt^(β−1); β<1 mejora, β>1 deterioro, β=1 HPP. Weibull para no reparables (bombilla, fusible, sello). Advertencia de conclusiones engañosas al aplicar Weibull a equipo reparado, aunque algunos practicantes lo usan con éxito. Estado: SOLO-SNIPPET — [JMP](https://www.jmp.com/support/help/14/crow-amsaa.shtml), [reliamag recurrence](https://reliamag.com/topics/articles/beyond-weibull-understanding-recurrence-analysis-for-repairable-systems), [Accendo SOR 1183](https://accendoreliability.com/podcast/sor/sor-1183-weibull-and-crow-amssa/)

### Gaps
- Tratamiento de censura (derecha, intervalo, terminado por tiempo vs por falla), Kaplan-Meier, Monte Carlo/RAM: no hallados. Síntesis propia: preguntar siempre cuántas unidades siguen operando (censuradas).

---

## 7. Repuestos y LCC

### Takeaway
Croston está sesgado al alza (Syntetos y Boylan lo demostraron); la corrección SBA multiplica por (1−α/2).

### Cited Findings
- Syntetos-Boylan: probaron matemáticamente el sesgo de Croston y propusieron una adaptación aproximadamente insesgada (SBA); la corrección sobreajusta series no intermitentes y una modificación posterior (Teunter & Sani, 2007) elimina ese sesgo con más varianza; un caso de repuestos en Indonesia halló sesgo en ambos pero menor varianza en SBA. Regla ADI≈1.32 de un proveedor: no verificada. Estado: SOLO-SNIPPET — [REF impact case](https://impact.ref.ac.uk/CaseStudies/CaseStudy.aspx?Id=9144), [MetricGate](https://metricgate.com/docs/croston-method)

### Gaps
- Min/max, bootstrap, LCC (SAE/ISO/IEC 60300-3-3), Barlow-Proschan: sin fuentes.

---

## 8. KPIs (catálogo)

### Takeaway
Las fuentes secundarias atribuyen definiciones de MTBF/MTTR a ISO 14224 o SMRP/EN 15341, y discrepan entre sí; las definiciones exactas están detrás de pago. Tratar toda fórmula como "tal como la publican sitios secundarios", no como texto normativo.

### Cited Findings
- EN 15341:2019 (+A1:2022 añade indicadores de salud-seguridad-ambiente): indicadores económicos, técnicos y organizacionales con metodología de selección; en la edición 2007, tres niveles por categoría. Las listas completas no son públicas. Estado: SOLO-SNIPPET — [BSI/IHS](https://cis.ihs.com//CIS/document/339209), [AFNOR](https://www.boutique.afnor.org/en-gb/standard/nf-en-15341/maintenance-maintenance-key-performance-indicators/fa180914/83912)
- Una guía francesa atribuye MTBF/MTTR a ISO 14224 y cita ISO 22400-2:2014 solo para KPIs de producción; discrepa con otra guía que los refiere a SMRP/EN 15341. Estado: SOLO-SNIPPET (conflicto) — [Teeptrak](https://teeptrak.com/fr/mttr-mtbf-mtta-2026/), [reliamag KPI](https://reliamag.com/guides/maintenance-reliability-kpi-reference/)
- Objetivos típicos (planificado alto, reactivo bajo, backlog en semanas) circulan sin fuente primaria rastreable, según el mismo reference — [planned vs reactive](https://reliamag.com/guides/planned-vs-reactive-maintenance-spend-ratios/).

### Tabla de KPIs

| KPI | Definición/fórmula (según fuente indicada) | Unidad | Fuente | Estado | Normalizado | Trampas de cálculo |
|---|---|---|---|---|---|---|
| MTBF | Tiempo total operativo / número de fallas (reparables) | h | [reliamag KPI](https://reliamag.com/guides/maintenance-reliability-kpi-reference/); atribución norma en conflicto | SOLO-SNIPPET | Sí (ISO 14224 / EN 15341 según fuente; sin confirmar) | Censura (ítems sin falla), mezclar unidades, contar paradas planificadas como fallas, usar MTBF para no reparables (usar MTTF) |
| MTTF | Para no reparables (distinción citada) | h | ídem | SOLO-SNIPPET | Sí | Confundir con MTBF |
| MTTR | Tiempo total de reparación / número de reparaciones; puede incluir diagnóstico, movilización de repuestos y pruebas | h | [Teeptrak](https://teeptrak.com/fr/mttr-mtbf-mtta-2026/) | SOLO-SNIPPET | Definiciones varían de empresa a empresa en qué tramos incluye | Incluir o no espera logística |
| Disponibilidad | Uptime/(uptime+downtime) o MTBF/(MTBF+MTTR) | % | [reliamag KPI](https://reliamag.com/guides/maintenance-reliability-kpi-reference/) | SOLO-SNIPPET | Tipos (inherente, alcanzada, operacional) existen; no verificados aquí | Mezclar tipos; definir tiempo calendario vs programado |
| OEE | Disponibilidad × rendimiento × calidad | % | ídem | SOLO-SNIPPET | ISO 22400 relacionada (sin confirmar) | La "disponibilidad" de OEE (tiempo de marcha/tiempo planificado) ≠ disponibilidad de confiabilidad |
| % trabajo planificado | Horas de mano de obra en trabajos planificados / horas totales de mantenimiento (SMRP 5.3.1 según un sitio); metas 80-90% = convención | % | [reliamag](https://reliamag.com/topics/guides/planned-vs-reactive-maintenance-spend-ratios) | SOLO-SNIPPET | SMRP (numeración no confirmada) | Definición de "planificado"; meta sin fuente |
| % trabajo reactivo | Trabajo que interrumpe el programa semanal / horas totales (numerado 5.4.1 o 5.6.1 según fuente) | % | ídem | SOLO-SNIPPET | SMRP (conflicto de numeración) | Distinguir emergencia vs interrupción del programa |
| R(t), TEEP, cumplimiento PM/programa, backlog (semanas), costo mant./valor de reposición, ratio PM/correctivo, tasa de repetición de fallas | Sin fuente abierta | — | — | NO-VERIFICADO | Backlog y costo/RAV conocidos en SMRP (conocimiento previo, sin confirmar); repetición de fallas varía por empresa | Backlog: usar horas planificadas / capacidad semanal; RAV: fuente única y actualizada |

### Folklore NO-RASTREABLE (no usar como evidencia)
- "89% de los ítems sin zona de desgaste / 4% patrón A": circula en blogs; no contrastado con Exhibit 2.13.
- Metas "80-90% planificado", "<10% (o <5%) reactivo", rango de backlog en semanas: sin fuente primaria rastreable, según [reliamag](https://reliamag.com/guides/maintenance-reliability-kpi-reference/).
- Cualquier "80% de las fallas son aleatorias" o "X% de ahorro con RCM/CBM": no encontrado con fuente primaria.

### Gaps
- Textos de EN 15341, ISO 22400-2, SMRP Best Practices (5.x), ISO 14224: de pago; no abiertos.

---

## 9. Modelos de madurez (GFMAM, ISO 55001, SMRP)

### Takeaway
El Landscape de GFMAM (2.ª ed.) tiene 39 subjetos en 6 grupos; la v3 pasa a 7 áreas y 40 subjetos. Sirve para evaluar madurez y como base de conocimiento de auditores ISO 55000.

### Cited Findings
- Landscape 2.ª ed.: 39 subjetos en 6 grupos (estrategia y planificación, toma de decisiones, entrega del ciclo de vida, información de activos, organización y personas, riesgo y revisión); v3: 7 áreas y 40 subjetos; pensado para informar el conocimiento requerido de auditores ISO 55000 y evaluar madurez; el IAM alinea los 39 subjetos con una escala de seis niveles. Estado: SOLO-SNIPPET — [GFMAM 2nd ed. PDF](https://www.gfmam.org/sites/default/files/2019-05/GFMAMLandscape_SecondEdition_English.pdf), [Assetivity v3](https://www.assetivity.com.au/?p=9800), [SAJIE](https://sajie.journals.ac.za/pub/article/view/1081)

### Gaps
- Pilares SMRP y mapeo de los subjetos a cláusulas ISO 55001: no hallados.

---

## 10. Preguntas de intake por método (SÍNTESIS PROPIA, NO-VERIFICADO; no provienen de una fuente citada)

| Método | Preguntas que un agente debe hacer |
|---|---|
| RCA | ¿Qué evento y cuándo? ¿Impacto (seguridad, producción, costo)? ¿Qué evidencia física/datos se preservó? ¿Quién estuvo presente? ¿Historial de eventos similares? ¿Qué se ha hecho ya? ¿Para qué se usará (aprendizaje o culpa; IEC 62740 excluye responsabilidad)? |
| 5 Porqués | ¿Qué evidencia respalda cada respuesta? ¿Hay más de una cadena causal? |
| FMEA/FMECA | ¿Alcance y límites del sistema? ¿Escala S/O/D vigente y calibrada? ¿Modos de falla históricos? ¿Controles actuales? ¿Estándar (IEC 60812, AIAG-VDA)? |
| RCM | ¿Contexto operativo y estándares de desempeño? ¿Quién facilita y quién participa? ¿Historial CMMS? ¿Consecuencias de seguridad/ambiente? |
| RBI/criticidad | ¿Mecanismos de daño? ¿Inspecciones previas? ¿Consecuencias definidas? ¿Calibración de la matriz? |
| Bad actors | ¿Período, métrica (costo, horas, frecuencia), jerarquía de activos? |
| CBM/P-F | ¿Qué síntoma precede a la falla y con cuánta antelación? ¿Tecnología disponible? ¿Tiempo de reacción necesario? |
| Weibull/Crow-AMSAA | ¿Reparable o no? ¿Cuántas unidades siguen operando (censura)? ¿Edades y fechas de falla? ¿Modos mezclados? |
| Repuestos | ¿Demanda histórica por período? ¿Lead time? ¿Criticidad? ¿Costo de faltante vs inventario? |
| LCC | ¿Horizonte, tasa de descuento, costos de adquisición, operación, mantenimiento y disposición? |
| KPIs | ¿Definición local de cada KPI? ¿Fuente de datos y calidad del CMMS? ¿Unidades y calendario base? |

### Gaps
- Estas preguntas no fueron contrastadas con una fuente publicada.
