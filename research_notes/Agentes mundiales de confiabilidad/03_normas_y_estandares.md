# Normas y estándares internacionales: confiabilidad, mantenimiento, análisis de falla, CBM, gestión de activos e IA gobernada

**Limitación de acceso (leer primero).** Todo egreso a dominios oficiales fue bloqueado: `iso.org`, `committee.iso.org`, `webstore.iec.ch`, `nist.gov`, `nvlpubs.nist.gov`, `airc.nist.gov`, `sae.org`, `webstore.ansi.org`, `api.org`, `standard.no`, `apps.dtic.mil`, `evs.ee`, `iteh.es`, `en.wikipedia.org`. WebFetch devolvió `ENOTFOUND` y curl con proxy devolvió `CONNECT tunnel failed, response 403`. Solo funcionó WebSearch. Por eso NINGUNA fila alcanza "VERIFICADO (página abierta)". Todo lo de abajo es **SOLO-SNIPPET** (resumen de buscador sobre catálogos oficiales o de terceros) o **NO-VERIFICADO**. Las URLs son las que devolvió el buscador; no las abrí. Antes de citar en un entregable, abrir la URL oficial.

Fecha de referencia: 2026-10-27. Leyenda: SS = SOLO-SNIPPET; NV = NO-VERIFICADO.

## 1. Datos y taxonomía de falla (ISO 14224, OREDA, EN 13306, IEC 60050-192)

### Takeaway
ISO 14224:2016 (3.ª ed.) es la edición vigente según el listado de ISO (confirmada en 2022); un listado de terceros la muestra en revisión (stage 90.60) pero no hallé confirmación de una 4.ª edición. OREDA es un handbook de datos (6.ª ed., 2015), no una norma ISO. EN 13306:2017 está confirmada; IEC 60050-192 no pude confirmarla.

### Cited Findings
| Norma | Título exacto | Organismo | Edición/año | Estado | Alcance (parafraseado) | URL | Verif. |
|---|---|---|---|---|---|---|---|
| ISO 14224 | Petroleum, petrochemical and natural gas industries — Collection and exchange of reliability and maintenance data for equipment | ISO (TC 67) | 3.ª ed., sept. 2016; revisada y confirmada 2022 | Vigente. La ed. 2006 está retirada. Posible revisión en curso: Wikipedia (solo pista) cita stage 90.60 desde 2022; no hallé 4.ª ed. | Formato común para recolectar datos de confiabilidad y mantenimiento de equipos a lo largo de su vida; define modos de falla como "tesauro". Cubre equipo de proceso, seguridad, submarino, ductos, perforación, etc. Ed. 3 añadió definiciones, clases de equipo (Anexo A) y KPIs (Anexo E) | https://www.iso.org/standard/64076.html | SS |
| OREDA Handbook | OREDA: Offshore and Onshore Reliability Data Handbook (vol. Topside y Subsea) | OREDA / SINTEF-NTNU, distribuye DNV | 6.ª ed., 2015 (última pública) | Vigente como última edición pública hallada; no es norma | Tablas genéricas de tasas de falla y estimación a partir de datos de campo del sector petrolero | https://oreda.com/standards-and-publications/ | SS |
| EN 13306 | Maintenance — Maintenance terminology | CEN | EN 13306:2017 (DIN EN 13306: 2018-02) | Vigente (según listado DIN) | Terminología trilingüe de mantenimiento | https://www.din.de (listado DIN) | SS |
| IEC 60050-192 | International Electrotechnical Vocabulary — Part 192: Dependability | IEC | Edición 2015 (mencionada en mi consulta) | NV: la búsqueda no devolvió la entrada | Vocabulario de dependabilidad | https://webstore.iec.ch | NV |

Fuente de la fila ISO 14224 (resumen de búsqueda sobre iso.org y ANSI): https://blog.ansi.org/ansi/iso-14224-2016-collection-maintenance-data/

### Inferences
- Un agente debe citar "ISO 14224:2016" y no "2006". Si el taxonomía de modos de falla es de otra fuente, no atribuirla a ISO 14224.
- OREDA es fuente de datos de tasas de falla (petróleo y gas); no usarlo como norma ni extrapolarlo sin ajustar a minería.

### Gaps
- Estado exacto de la revisión de ISO 14224 (¿4.ª ed. en desarrollo?) no confirmado.
- IEC 60050-192: edición y estado NV. Se puede consultar gratis en electropedia.org (no accesible).

## 2. Gestión de activos (ISO 55000/55001/55002, GFMAM/IAM)

### Takeaway
La familia fue revisada: ISO 55000:2024 y ISO 55001:2024 (2.ª ed., julio 2024) reemplazan a las de 2014. ISO 55002 sigue en edición 2018, marcada "to be revised". Un agente que cite "ISO 55001:2014" cita una versión retirada.

### Cited Findings
| Norma | Título | Organismo | Edición | Estado | Alcance | URL | Verif. |
|---|---|---|---|---|---|---|---|
| ISO 55000 | Asset management — Vocabulary, overview and principles (título abreviado en listados; título completo exacto NV) | ISO (TC 251) | 2024 (vigente desde 2024-07-03) | Vigente; reemplaza ed. 2014 | Define términos, principios y resultados de la gestión de activos; aplica a todo tipo de activo y tamaño de organización; sin guía técnica específica por tipo de activo | https://www.sis.se/en/produkter/standardization/vocabularies/services/iso-550002024/ | SS |
| ISO 55001 | Asset management — Asset management system — Requirements | ISO (TC 251) | 2.ª ed., 2024-07 (ISO 88433) | Vigente; la ed. 2014 está retirada | Requisitos certificables del sistema de gestión de activos. Fuentes secundarias (no la norma) indican más peso a sostenibilidad/clima (vía estructura armonizada), decisiones justificadas por objetivos estratégicos y uso de datos en tiempo real; transición típica 3 años | https://www.iso.org/standard/88433.html | SS |
| ISO 55002 | Asset management — Management systems — Guidelines for the application of ISO 55001 | ISO | 2018 | Vigente pero stage 90.92 "to be revised"; sin ed. 2024 según fuentes | Guía de aplicación de ISO 55001 | (catálogo ISO; no abierto) | SS |
| ISO 55011, 55012, 55013 | NV (títulos no confirmados) | ISO/TC 251 | NV | Mencionadas por un medio comercial como nuevas guías | NV | NV | NV |
| GFMAM Landscape / IAM Landscape / Competences | NV | GFMAM, IAM | NV | NV | Marco de 39 sujetos (dato de memoria, no verificado) | https://gfmam.org | NV |

Fuentes: https://reliamag.com/guides/iso-55000-asset-management-explained/ (trade); https://www.glocertinternational.com/resources/guides/iso-55001-2024-changes-and-transition-guide/ (certificadora). Aclaración: la "enmienda de acción climática" encontrada es del ISO/IEC 19770-1 (gestión de activos TI), no de ISO 55001.

### Inferences
- Para auditorías 55001, exigir "ISO 55001:2024" y verificar el plazo de transición con el organismo certificador.

### Gaps
- Título completo exacto de ISO 55000:2024, y existencia/títulos de ISO 55011-13, no verificados. GFMAM Landscape no verificado.

## 3. Monitoreo de condición y diagnóstico

### Takeaway
ISO 17359:2018 (confirmada 2023) es la guía marco. ISO 20816 sustituye a ISO 10816/7919. ISO 20816-1:2016 vigente con 2.ª ed. en etapa FDIS; ISO 20816-3:2022 vigente. ISO 18436-2:2014 está en revisión (FDIS ISO/FDIS 18436-2, título pasa a "training and certification"). Para ISO 13374-1/-2, 13379-1, 13381-1 y 13372 solo tengo evidencia parcial.

### Cited Findings
| Norma | Título | Edición/año | Estado | Alcance | URL | Verif. |
|---|---|---|---|---|---|---|
| ISO 17359 | Condition monitoring and diagnostics of machines — General guidelines | 3.ª ed., enero 2018; confirmada 2023 | Vigente; reemplazó 2011 (que sustituyó a ISO 13380 e ISO 17359:2003) | Procedimientos generales para establecer un programa de CM; aplica a todas las máquinas; auditoría de criticidad, selección de medición, criterios de alarma | https://www.iso.org/standard/71194.html | SS |
| ISO 13372 | Condition monitoring and diagnostics of machines — Vocabulary | 2012 (2.ª ed.) | NV vigencia | Vocabulario común de CM&D | (catálogo ISO) | SS parcial |
| ISO 13374-3 | Condition monitoring and diagnostics of machines — Data processing, communication and presentation — Part 3: Communication | 2012 | Aparece en catálogos; vigencia NV | Requisitos de comunicación de datos para arquitectura abierta CM&D (interoperabilidad) | https://scc-ccn.ca/standardsdb/standards/8152733 | SS |
| ISO 13374-4 | Condition monitoring and diagnostics of machine systems — Data processing, communication and presentation — Part 4: Presentation | 2015 | vigencia NV | Requisitos de presentación de información para análisis técnico y decisión | https://scc-ccn.ca/standardsdb/standards/8160078 | SS |
| ISO 13374-1 / -2 | Parte 1: General guidelines; Parte 2: Data processing | 2003 / 2007 (años de mi consulta) | NV | NV | NV | NV |
| ISO 13379-1 | Condition monitoring and diagnostics of machines — Data interpretation and diagnostics techniques — Part 1: General guidelines | 2012; un distribuidor muestra además una edición 2025 | CONFLICTO: posible nueva edición 2025; no confirmado | Guía de interpretación de datos y diagnóstico | (catálogo ISO) | SS conflictivo |
| ISO 13381-1 | Condition monitoring and diagnostics of machines — Prognostics — Part 1: General guidelines | 2015 | Listado como vigente | Guía para construir y aplicar procesos de pronóstico; conceptos comunes. Partes 2-4 anunciadas (no confirmadas publicadas) | https://infostore.saiglobal.com/en-us/standards/ISO-13381-1-2015-588598_SAIG_ISO_ISO_1348231/ | SS |
| ISO 18436-2 | Condition monitoring and diagnostics of machines — Requirements for qualification and assessment of personnel — Part 2: Vibration condition monitoring and diagnostics (título de 2014 de memoria, NV) | 2.ª ed., mayo 2014 (confirmada 2019) | Vigente, en revisión: ISO/FDIS 18436-2 (ISO 88030), nuevo título "training and certification of personnel"; estado de publicación NV | Requisitos de formación, experiencia y examen para analistas de vibración, 4 categorías | https://www.iso.org/standard/88030.html | SS |
| ISO 20816-1 | Mechanical vibration — Measurement and evaluation of machine vibration — Part 1: General guidelines | 2016 | Vigente; 2.ª ed. en FDIS (ISO 89921). ISO 10816-1 y 7919-1 retiradas (según BSI y DIN) | Condiciones generales para medir y evaluar vibración en partes giratorias y no giratorias de máquinas completas; no cubre vibración torsional | https://www.iso.org/standard/89921.html | SS |
| ISO 20816-3 | Mechanical vibration — Measurement and evaluation of machine vibration — Part 3: Industrial machinery with a power rating above 15 kW and operating speeds between 120 r/min and 30 000 r/min (título de memoria; el alcance sí está en el snippet) | 2022 | Vigente | Evaluación in situ de banda ancha para máquinas acopladas >15 kW, 120-30 000 r/min; excluye alternativas (van en ISO 20816-8) | https://www.iso.org/standard/78311.html | SS |
| ISO 20816-2/-4/-5/-8 | NV | NV | NV | NV | NV | NV |
| ISO 4406 | Hydraulic fluid power — Fluids — Method for coding the level of contamination by solid particles | 2021 (2021-01-06); listado indica confirmada 2026 | Vigente | Código de contaminación por partículas sólidas (p. ej. 18/16/13) | https://www.iso.org/standard/79716.html | SS |
| ISO 281 | Rolling bearings — Dynamic load ratings and rating life | 2007; enmienda en elaboración (voto de encuesta cerrado jul-2025, nuevo borrador previsto) | Vigente (2007) | Carga dinámica y vida nominal L10 de rodamientos | (catálogo ISO) | SS |

### Inferences
- Las alarmas de vibración de una bomba o ventilador industrial >15 kW deben referenciar ISO 20816-3:2022, no ISO 10816-3.
- Certificación del analista: citar ISO 18436-2:2014 y avisar que hay edición nueva en trámite.

### Gaps
- ISO 13374-1/-2, 13379-1 (¿ed. 2025?), 13372 vigencia, 20816-2/-4/-5/-8 y títulos completos de 20816-3 y 18436-2: NV.

## 4. Análisis de falla y riesgo

### Takeaway
IEC 60812:2018 (3.ª ed.), IEC 62740:2015 y IEC 61025:2006 (ed. 3 en curso) están respaldadas por snippets. AIAG-VDA 2019 reemplazó RPN por Action Priority (AP) en automoción. API RP 580 4.ª ed. (2023, Addendum 1 2025) y API 581 4.ª ed. (2025) en listados de terceros. NORSOK Z-008: última edición hallada 2017 con revisión aprobada en 2023.

### Cited Findings
| Norma | Título | Organismo | Edición | Estado | Alcance | URL | Verif. |
|---|---|---|---|---|---|---|---|
| IEC 60812 | Failure modes and effects analysis (FMEA and FMECA) | IEC | 3.ª ed., agosto 2018; reemplaza 2006 | Vigente; no vi enmiendas | Texto normativo genérico (hardware, software, procesos, acción humana); ejemplos de seguridad/automoción/software/servicio en anexos informativos; incluye variantes de RPN y matriz de criticidad | https://webstore.iec.ch/publication/26359 | SS |
| IEC 61025 | Fault tree analysis (FTA) | IEC | 2.ª ed., diciembre 2006 | Vigente; la página TC56 lista "Ed 3.0 in progress" | Símbolos, construcción del árbol, análisis cualitativo y cuantitativo | https://tc56.iec.ch/risk-assessment-standards/ | SS |
| IEC 62740 | Root cause analysis (RCA) | IEC | 1.ª ed., 2015 | Vigente | Principios y pasos del proceso RCA, atributos para elegir técnica; análisis a posteriori; no asigna culpa | https://webstore.iec.ch (listado en online.standard.no) | SS |
| IEC 31010 | Risk management — Risk assessment techniques | IEC/ISO | 2019 | Vigente (según snippet) | Guía de selección y aplicación de técnicas de evaluación de riesgo | https://tc56.iec.ch/risk-assessment-standards/ | SS |
| ISO 31000 | Risk management — Guidelines | ISO | 2.ª ed., feb. 2018; fuente secundaria dice confirmada oct-2023 | Vigente; un artículo habla de revisión, sin fecha (NV) | Principios, marco y proceso de gestión de riesgo; guía, no certificable | https://www.iso.org/iso-31000-risk-management.html (NV abierta) | SS |
| AIAG-VDA FMEA Handbook | FMEA Handbook (1.ª ed. AIAG-VDA) | AIAG y VDA | 2019 (abril o junio, fuentes en conflicto) | Vigente | Método de 7 pasos; sustituye RPN por Action Priority (alta/media/baja) con peso a Severidad > Ocurrencia > Detección; verificar requisitos del cliente | https://reliamag.com/guides/how-to-perform-fmea/ (secundaria) | SS |
| MIL-STD-1629A | Procedures for Performing a FMECA | DoD EE.UU. | Notice 3 (1984) de memoria | NV: la búsqueda no lo cubrió. De memoria fue cancelada en 1998 sin reemplazo; NO citar como vigente sin verificar en ASSIST | https://quicksearch.dla.mil | NV |
| API RP 580 | Risk-Based Inspection | API | 4.ª ed., agosto 2023; Addendum 1 marzo 2025 (listados de terceros) | Vigente | Marco y requisitos mínimos de un programa RBI | https://eshop.normservis.sk/norma/apirp-580-ed-4-1.8.2023.html | SS |
| API RP 581 | Risk-Based Inspection Methodology | API | 4.ª ed., enero 2025 (692 págs., tercero) | Vigente | Métodos cuantitativos de RBI para equipo fijo presurizado | https://oviss.jp/view/item/000000001157 | SS |
| NORSOK Z-008 | Risk based maintenance and consequence classification | Standards Norway | Dic. 2017 (última listada); revisión aprobada jun-2023; Standards Norway anunció "has been revised" (fecha NV) | Posible edición nueva (la de 2017 puede estar reemplazada) | Clasificación de consecuencia por función y programa de mantenimiento inicial; revisión añade clasificación funcional, herencia, anexo de clima y vínculo con barreras | https://standard.no/en/news/norsok-z-008-has-been-revised | SS |

### Inferences
- No usar RPN como único criterio si el cliente exige AIAG-VDA; IEC 60812:2018 sí admite RPN y variantes.
- Para MIL-STD-1629A, tratarla como histórica hasta verificar.

### Gaps
- Estado actual de MIL-STD-1629A (cancelada/obsoleta), fecha de la nueva NORSOK Z-008, años y subpartes de API 580/581 en api.org: NV.

## 5. Estadística y modelado de confiabilidad

### Takeaway
Solo IEC 61078:2016, IEC 60300-3-11:2009 y IEC 61164 (edición 2004) tienen respaldo parcial. IEC 61649, IEC 61703, IEC 60300-3-1/-3-3 con años inciertos. MIL-HDBK-217F Notice 2 (1995) es de guía y discontinuado.

### Cited Findings
| Norma | Título | Edición | Estado | Alcance | Verif. |
|---|---|---|---|---|---|
| IEC 61649 | Weibull analysis | Año NV (2008 de memoria) | NV | Análisis de datos de vida con Weibull | NV |
| IEC 61164 | Reliability growth — Statistical test and estimation methods | 2004 (lista india; no hallé ed. 2008; revisada 2023 en India) | NV vigencia IEC | Pruebas y estimación estadística de crecimiento de confiabilidad | SS |
| IEC 61078 | Reliability block diagrams | 2016 | Vigente (listado) | Modelado de dependabilidad con RBD para calcular confiabilidad y disponibilidad | SS (DIN: 2016-08) |
| IEC 61703 | Mathematical expressions for reliability, availability, maintainability and maintenance support terms | Año NV | Listado DIN como vigente | Fórmulas de métricas RAM | SS |
| IEC 60300-3-1 | Dependability management — Part 3-1: Application guide — Analysis techniques for dependability — Guide on methodology (de memoria) | 2003-01 | NV | Guía de técnicas de análisis de dependabilidad | SS parcial |
| IEC 60300-3-3 | Dependability management — Part 3-3: Application guide — Life cycle costing | 2004/2005 vs 2017 (fuentes en conflicto; EVS lista EN 60300-3-3:2017) | Vigencia NV | Introducción a LCC y elementos de costo | SS conflictivo |
| IEC 60300-3-11 | Dependability management — Part 3-11: Application guide — Reliability centred maintenance | 2.ª ed., 2009 (ed. 3 en desarrollo según un listado) | Vigente | Política de gestión de fallas con RCM, algoritmo revisado, aplicable a todas las industrias | SS | 
| IEC 60300-3-12 | NV | NV | NV | NV | NV |
| MIL-HDBK-189C | Reliability Growth Management | 2011 (de memoria) | NV | NV | NV |
| MIL-HDBK-217F Notice 2 | Reliability Prediction of Electronic Equipment | 28 feb. 1995 (base 2 dic. 1991) | Sin actualización desde 1995 (foro, secundaria); solo guía | Modelos de tasas de falla de componentes electrónicos | SS |

URLs: https://online.standard.no/en/iec-60300-3-11-2009-ed2 ; https://evs.ee/en/evs-en-60300-3-11-2009 ; https://everyspec.com/MIL-HDBK/MIL-HDBK-0200-0299/MIL-HDBK-217F_NOTICE-2_14590/ ; https://www.boutique.afnor.org/en-gb/standard/iec-610781991/analysis-techniques-for-dependability-reliability-block-diagram-method/xs102592/436071 (nótese: esta es la ed. 1991).

### Gaps
- IEC 61649, 61703, 60300-3-12, MIL-HDBK-189C: año/título/estado NV. Resolver IEC 60300-3-3 (2004/2005 vs 2017).

## 6. RCM

### Takeaway
SAE JA1012 (ed. agosto 2011) figura vigente en SAE Mobilus; la ed. 2002 aparece "Current" en SAE pero retirada en un distribuidor (conflicto). La edición vigente de SAE JA1011 y su fecha NO se confirmó (el año 2009 de mi consulta no tiene respaldo). El informe de Nowlan & Heap es público en DTIC.

### Cited Findings
- SAE JA1012_201108 "A Guide to the Reliability-Centered Maintenance (RCM) Standard": revisión de 2011 por ciclo de 5 años y consistencia con JA1011; amplía y aclara los criterios de JA1011 — [SAE Mobilus](https://saemobilus.sae.org/content/JA1012_201108) (SS)
- SAE JA1011 "Evaluation Criteria for RCM Processes": un glosario de proveedor da 1999; edición vigente NV — [Tractian glosario](https://tractian.com/en/glossary/sae-ja1011) (secundaria)
- IEC 60300-3-11:2009 (ver tabla sec. 5).
- Nowlan & Heap, "Reliability-Centered Maintenance", informe DoD/United Airlines, diciembre 1978, DTIC accesión ADA066579, PDF abierto; también copia en EverySpec AD-A066579 — [DTIC](https://apps.dtic.mil/sti/html/tr/ADA066579/index.html) ; [EverySpec](https://everyspec.com/DoD/DOD-General/AD-A066579_18228/) (SS)
- Moubray, RCM II (libro): NO verificado; no hallé ubicación pública (es libro comercial, Industrial Press).

### Inferences
- Para declarar "proceso RCM" conforme, el criterio es JA1011 (7 preguntas); la guía JA1012 explica cómo.

### Gaps
- Edición vigente de SAE JA1011 y estado de la ed. 2002 de JA1012; datos bibliográficos de Moubray.

## 7. KPIs de mantenimiento

### Takeaway
EN 15341 se debe citar como EN 15341:2019+A1:2022 (la 2019 base figura retirada en EVS desde junio 2022). ISO 22400-2:2014 y SMRP no pude verificarlas.

### Cited Findings
| Norma | Título | Edición | Estado | Alcance | Verif. |
|---|---|---|---|---|---|
| EN 15341 | Maintenance — Maintenance key performance indicators | EN 15341:2019+A1:2022 | Vigente la consolidada; 2019 sola retirada (EVS) | Sistema de KPIs de mantenimiento (económicos, técnicos, organizativos) para activos físicos | SS: https://www.evs.ee/en/evs-en-15341-2019 ; https://online.standard.no/en/ns-en-15341-2019a1-2022 |
| ISO 22400-2 | Automation systems and integration — Key performance indicators (KPIs) for manufacturing operations management — Part 2: Definitions and descriptions | 2014 (de memoria) | NV | NV | NV |
| SMRP Best Practice Metrics | NV | SMRP | NV | (qué es público: NV) | NV |

### Gaps
- Lista de KPIs de EN 15341 no pública; ISO 22400-2 y SMRP NV.

## 8. IA y seguridad

### Takeaway
NIST AI RMF 1.0 (enero 2023, NIST AI 100-1) y AI 600-1 Generative AI Profile (julio 2024) están confirmados por snippets, voluntarios. ISO/IEC 42001:2023 (certificable) e ISO/IEC 23894:2023 (guía) están respaldadas parcialmente. IEC 62443 es serie; ISO 8000-61 ed. 2016.

### Cited Findings
| Norma | Título | Organismo | Edición | Estado | Alcance | URL | Verif. |
|---|---|---|---|---|---|---|---|
| NIST AI 100-1 | Artificial Intelligence Risk Management Framework (AI RMF 1.0) | NIST | enero 2023 | Voluntario | Marco Govern/Map/Measure/Manage | https://www.nist.gov/itl/ai-risk-management-framework | SS |
| NIST AI 600-1 | Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile | NIST | julio 2024 | Voluntario, no reemplaza AI RMF | 12 riesgos propios o agravados por IA generativa y acciones sugeridas con IDs (p. ej. GV-1.1-001) | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | SS |
| ISO/IEC 42001 | Information technology — Artificial intelligence — Management system | ISO/IEC | 2023 | Vigente; certificable | Sistema de gestión de IA (título exacto NV) | https://www.iso.org/standard/81230.html | SS (solo descripción de tercero) |
| ISO/IEC 23894 | Artificial intelligence — Guidance on risk management | ISO/IEC | 2023 | Vigente; guía, no certificable | Cómo integrar gestión de riesgo de IA en actividades de IA | https://www.iso.org/standard/77304.html | SS |
| IEC 62443 | Industrial communication networks / Security for industrial automation and control systems (título de serie exacto NV) | IEC TC 65 WG10 + ISA99 | Serie multi-parte; IEC PAS 62443-1-6:2025 (guía IIoT) | Vigente (por partes); estado por parte NV | Ciberseguridad OT/IACS; texto idéntico ISA/IEC | https://syc-se.iec.ch/?p=4375 | SS |
| ISO 8000-61 | Data quality — Part 61: Data quality management: Process reference model | ISO | 2016 (ed. 2023 solo adopción india idéntica) | Vigencia NV | Modelo de procesos de gestión de calidad de datos | https://iteh.es/catalog/standards/iso/0b5737db-6738-48ff-8c0e-0c083adf7194/iso-8000-61-2016 | SS |
| ISO 8000-1 | NV título | ISO | 2022 | NV | NV | https://iteh.es/catalog/standards/iso/61ae2d14-ae55-4e88-bd36-bca8e0870ef8/iso-8000-1-2022 | SS |

### Inferences
- Un agente IA de mantenimiento puede alinear su gobernanza con 42001 (sistema) + 23894 (riesgo) + NIST AI RMF (práctica); ninguno de los tres exige técnicas específicas de confiabilidad.

### Gaps
- Qué partes de IEC 62443 están vigentes/revisadas; títulos exactos de 42001 y de la serie 62443; NIST: posibles revisiones 2025-2026 no verificadas (nist.gov inaccesible).

## 9. Tabla norma → decisión/entregable del agente

| Norma | Decisión que informa | Entregable |
|---|---|---|
| ISO 14224:2016 | Qué campos y códigos de modo/causa/mecanismo de falla registrar | Esquema de datos de fallas del CMMS |
| OREDA 6.ª ed. | Tasa de falla genérica cuando no hay datos propios | Línea base de λ con advertencia |
| EN 13306:2017 | Definiciones de mantenimiento preventivo/correctivo/condicional | Glosario del agente |
| ISO 55001:2024 / 55000:2024 | Alineación de decisiones con objetivos y riesgo de activos | Plan estratégico de gestión de activos, evidencias de auditoría |
| ISO 17359:2018 | Qué máquinas monitorear y con qué técnica | Programa de CBM con criticidad |
| ISO 20816-1/-3 | Umbrales de vibración (zonas A-D) | Reporte de severidad de vibración |
| ISO 18436-2 | Cualificación del analista | Requisito de certificación en el procedimiento |
| ISO 13381-1 | Cómo estructurar un pronóstico de RUL | Especificación del proceso de pronóstico |
| ISO 4406 | Límite objetivo de limpieza de aceite | Meta de código de limpieza |
| ISO 281 | Vida L10 de rodamiento | Cálculo de vida nominal |
| IEC 60812 / AIAG-VDA | Priorización de modos de falla | FMEA con RPN/AP |
| IEC 61025 | Combinación lógica de causas de un evento | Árbol de fallas |
| IEC 62740 | Pasos y técnica de RCA | Informe RCA |
| IEC 31010 / ISO 31000 | Elección de técnica de riesgo, proceso de riesgo | Matriz y registro de riesgos |
| API RP 580/581, NORSOK Z-008 | Intervalo de inspección por riesgo; clase de consecuencia | Plan RBI; jerarquía de criticidad |
| IEC 61078, 61703 | Disponibilidad de sistemas en serie/paralelo | Modelo RBD |
| IEC 60300-3-11, SAE JA1011/1012, Nowlan & Heap | Si un proceso es RCM; selección de tareas | Análisis RCM y plan de tareas |
| EN 15341:2019+A1:2022 | Definición de KPIs de mantenimiento | Tablero de KPIs |
| ISO/IEC 42001, 23894, NIST AI RMF, AI 600-1 | Controles de gobernanza y riesgo del agente de IA | Registro de riesgos de IA, política de uso |
| IEC 62443 | Seguridad de acceso a datos/redes OT | Requisitos de segmentación y acceso |
| ISO 8000-61 | Calidad de datos de falla | Plan de gestión de calidad de datos |

(Las relaciones norma→decisión son inferencia mía basada en los alcances, no texto de las normas.)

## 10. Cambios recientes 2023-2026 (para no citar mal)
- ISO 55000 e ISO 55001 pasaron a edición 2024; ISO 55002 sigue 2018 en revisión. (SS)
- EN 15341:2019 → citar +A1:2022. (SS)
- ISO 20816-3:2022 vigente; ISO 20816-1 2.ª ed. en FDIS; ISO 10816-1 retirada. (SS)
- ISO 18436-2 en FDIS (nueva ed. con título de "training and certification"). (SS)
- ISO 13379-1: posible edición 2025 (conflicto de distribuidor). (SS)
- API RP 580 4.ª ed. 2023 + Addendum 2025; API 581 4.ª ed. 2025. (SS terceros)
- NORSOK Z-008 revisada (aprobada 2023); fecha de publicación NV. (SS)
- IEC 61025 ed. 3 en curso; IEC 60300-3-11 ed. 3 en desarrollo (un listado). (SS)
- ISO 4406:2021 confirmada 2026 (listado ISO); ISO 281 enmienda en elaboración. (SS)
- NIST AI 600-1 (julio 2024); ISO/IEC 42001:2023 y 23894:2023. (SS)
- IEC PAS 62443-1-6:2025 (IIoT). (SS)

## Lista de normas NO verificadas (o solo con título de memoria)
IEC 60050-192; IEC 61649; IEC 61703 (año); IEC 60300-3-12; IEC 60300-3-1 (vigencia); IEC 60300-3-3 (2004/2005 vs 2017); MIL-STD-1629A (estado); MIL-HDBK-189C; ISO 22400-2; SMRP Best Practice Metrics; GFMAM/IAM Landscape; ISO 55011/55012/55013; ISO 13374-1 y -2; ISO 13372 (vigencia); ISO 20816-2/-4/-5/-8; SAE JA1011 (edición vigente); Moubray RCM II (ubicación pública); títulos completos exactos de ISO 55000:2024, ISO/IEC 42001, IEC 62443 y ISO 18436-2/20816-3; ISO 8000-1/-8; cualquier estado de ISO 14224 revisión 4.ª ed.
