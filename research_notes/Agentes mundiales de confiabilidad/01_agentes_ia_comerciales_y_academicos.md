# Agentes, copilotos y plataformas de IA para mantenimiento y confiabilidad (comerciales y académicos)

**Nota de método y de acceso (leer primero).** Fecha de acceso de todo: 2026-10-27. En esta sesión NO se pudo abrir ninguna página primaria: WebFetch devolvió `getaddrinfo ENOTFOUND` (ibm.com, aspentech.com, gevernova.com, arxiv.org, papers.phmsociety.org) y curl por el proxy devolvió `CONNECT tunnel failed, response 403` (arxiv.org y otros). Elicit (`mcp__Elicit__search_papers`) devolvió `api_access_denied` (el plan no incluye API). Por tanto TODO lo de abajo es **SOLO-SNIPPET** (visto únicamente en resultados de WebSearch, que a su vez resumen la página) salvo indicación. Ningún ítem es VERIFICADO (página/paper abierto). Las cifras son "reportado por el proveedor" salvo que se diga otra cosa. Lo no encontrado se marca NO-VERIFICADO/Gap.

## 1. Soluciones comerciales: qué hacen realmente, tipo de IA, datos, resultados

### Takeaway
El mercado se divide en (a) ML sobre series de tiempo/vibración/señal eléctrica para detección de anomalías y alerta temprana (Mtell, Senseye, Augury, Samotics), (b) capas LLM/genAI sobre CMMS/EAM para limpieza de datos, búsqueda en manuales y generación de órdenes (Maximo 9, MaintainX, Fiix, SAP Joule, Siemens), y (c) plataformas de datos con constructores de agentes (Cognite Atlas AI, C3 AI). Casi toda la evidencia de resultados es de proveedor; no hallé validación independiente ni tasas de falsa alarma agregadas.

### Cited Findings
Columnas: ítem · qué es · fuente · acceso 2026-10-27 · verificación · relevancia para agente de confiabilidad

| Ítem | Qué es / qué hace (según snippet) | Fuente | Estado | Relevancia |
|---|---|---|---|---|
| IBM Maximo Application Suite 9.0 (GenAI) | Asistentes GenAI para "work order intelligence": revisa/corrige/sugiere códigos de falla en órdenes; asistente de onboarding entrenado en documentación. Reseller describe Monitor (datos de sensores), Predict (orden de trabajo con partes/procedimientos), Health, Assist (guía a técnicos). | [Verdantix](https://marketing.verdantix.com/blog/ibm-maximo-application-suite-9-0-provides-users-new-genai-fsm-and-emissions-functionality); [reseller](https://platform.softwareone.com/product/ibm-maximo-application-suite/PCP-1654-4934) (tercero, no IBM) | SOLO-SNIPPET; capacidades agénticas de Maximo: NO-VERIFICADO (no hallado) | Alta: calidad de códigos de falla es base de cualquier análisis de confiabilidad |
| Aspen Mtell (AspenTech) | ML "agents": un agente de falla por evento de falla registrado + agentes de anomalía; aprende de historian + registros de fallas. Casos: caldera/horno pulpa y papel con aviso de 9 días; compresor de refinería con aviso de 8 semanas; piloto Saras (4 equipos). | [IoT ONE caso](https://iotone.com/case-study/leading-pulp-amp-paper-manufacturer-detects-and-avoids-major-fire-using-aspen-mtell/c15718); [Mining.com patrocinado](https://www.mining.com/sponsored-content/aspentech-reduces-downtime-mining-equipment/); [OGN Saras](https://ognnews.com/Article/45085/AspenTech_uses_app_to_help_Saras_improve_business_performance) | SOLO-SNIPPET; resultados = reportado por el proveedor (contenido patrocinado) | Alta: modelo de "firma de falla" por modo de falla |
| Siemens Senseye Predictive Maintenance | genAI conversacional añadida a inicios de 2024; agrupa casos, multi-idioma, busca casos pasados similares y soluciones; BlueScope citado (cita cualitativa). Sin cifras de resultado en lo hallado. | [Enlit](https://www.enlit.world/library/siemens-brings-generative-ai-to-predictive-maintenance); [NAFEMS](https://www.nafems.org/about-us/media/news/industrynews1003/generative-artificial-intelligence-takes-siemens-predictive-maintenance-solution-to-the-next-level/) | SOLO-SNIPPET; cifras: no hay | Media-alta: patrón "predictivo a prescriptivo" con casos similares |
| GE Vernova APM | Sin anuncio de genAI de 2025 confirmado. Un snippet 2026 (LinkedIn, secundario): MoU con Cosmo Oil (sep. 2026) para acceso temprano a capacidades GenAI del roadmap APM; Inspenet: "AI assistants" en APM (API Summit 2026). | [Inspenet](https://inspenet.com/en/inspenet-tv/ge-vernova-failures-industrial-assets/); [blog GE Vernova](https://gevernova.com/software/blog/center-of-excellence-asset-performance-management) | SOLO-SNIPPET (fuentes secundarias); detalle técnico: NO-VERIFICADO | Media: roadmap, sin evidencia de producto |
| Augury (Halo) | Diagnóstico continuo con vibración/ultrasonido/otros; "malfunction dictionary" de >40.000 máquinas (dato de volumen, no de precisión); sensor edge-AI Halo R4000 (nov. 2024) con "hybrid-AI prescriptive diagnostics". | [BusinessWire 2024](https://www.businesswire.com/news/home/20241112051493/en/Augury-Introduces-the-First-Industrial-Grade-Edge-AI-Native-Machine-Health-Sensing-Platform); [Facility Executive 2017 (anterior a 2023)](https://facilityexecutive.com/2017/11/augury-unveils-halo-diagnostics-platform/) | SOLO-SNIPPET; sin métricas de exactitud | Media: ejemplo de diccionario de fallas + diagnóstico |
| Samotics SAM4 | ML sobre firma eléctrica (formas de onda desde el centro de control de motores) para motores AC/tren de potencia, sin sensores de vibración. | [Capterra](https://www.capterra.com/p/188010/SAM4/); [GetApp](https://www.getapp.com/all-software/a/sam4/) | SOLO-SNIPPET (listados de terceros); sin resultados | Media: fuente de datos alternativa |
| Fiix (Rockwell) | Asset Risk Predictor (ML, "predice fallas con días de anticipación", setup en 2 semanas según Rockwell) + GenAI "Prescriptive Work Orders" (mayo 2024) que convierte predicciones en órdenes editables enviables a cualquier CMMS/EAM. Un roundup secundario (Overview.ai) dice que Plex+Fiix tiene capa agéntica; fuente única. | [ITWire](https://itwire.com/business-it-news/enterprise-solutions/flix-by-rockwell-automation-announces-gen-ai-prescriptive-work-orders.html); [Overview.ai](https://www.overview.ai/blog/top-10-agentic-ai-tools-manufacturing-2026/) | SOLO-SNIPPET; "agéntico" = NO-VERIFICADO | Alta: ciclo predicción -> orden de trabajo |
| MaintainX CoPilot | Add-on: busca en manuales/archivos adjuntos al activo, responde en lenguaje natural, convierte respuestas en órdenes/plantillas, sugiere al completar OT según OT pasadas y manuales; la revisión humana es obligatoria. | [Help MaintainX](https://help.getmaintainx.com/ask-your-asset); [Complete a WO](https://help.getmaintainx.com/complete-a-work-order-with-maintainx-copilot) | SOLO-SNIPPET (documentación oficial vista vía resumen) | Alta: RAG sobre manuales con human-in-the-loop |
| SAP APM + Joule | Joule responde preguntas desde documentación SAP Help Portal; SAP afirma 30% menos tiempo para obtener insights (proveedor). Es Q&A de documentación, no diagnóstico predictivo según lo hallado. | [SAP](https://www.sap.com/products/scm/joule-with-sap-asset-performance-management.html) | SOLO-SNIPPET | Baja-media |
| Seeq AI Assistant | Lanzado 29-feb-2024; asistente genAI para construir analítica y código sobre datos de proceso; multi-LLM; Ascend Performance Materials espera ~50% menos curva de aprendizaje (cita de cliente). | [Automation World](https://www.automationworld.com/analytics/article/33039380/seeq-adds-generative-ai-capabilities); [ReliabilityWeb](https://reliabilityweb.com/seeq-announces-generative-ai-capabilities-with-seeq-ai-assistant) | SOLO-SNIPPET | Media: copiloto de analítica sobre historian |
| Cognite Atlas AI | Constructor low-code de agentes sobre Cognite Data Fusion (grafo de conocimiento); Document QA sobre logs/manuales; permisos y confirmación explícita para herramientas (Python, REST); límites 30 agentes/proyecto, 10 herramientas/agente. Aker BP: agentes RCA, >70% menos tiempo de análisis (reportado por la empresa). | [Cognite blog](https://www.cognite.com/en/resources/blog/cognite-atlas-ai-september-product-release-accelerating-agentic-ai-at-scale); [Offshore Technology](https://www.offshore-technology.com/newsletters/aker-bp-leverages-cognite-atlas-ai) | SOLO-SNIPPET | Alta: ejemplo de gobernanza y RCA agéntico |
| C3 AI Reliability | Listado como oferta; 2023 genAI suite con clientes citados (Georgia-Pacific, Nucor, Con Edison). Estudio Forrester patrocinado por Baker Hughes/C3 (oct. 2024, n=96): confiabilidad operativa 24% usa genAI, 22% piloto. | [Forrester/Baker Hughes](https://thoughtleadership.forrester.com/go/bakerhughes/genai_in_heavy_industries) | SOLO-SNIPPET; producto en detalle: NO-VERIFICADO | Baja (contexto de adopción) |
| Otros hallados en roundups | Infinite Uptime ("reliability as a service"), Arch Systems (genAI para RCA de downtime; 60-80% OEE es cifra del CEO sin verificar). | [IIoT World](https://www.iiot-world.com/predictive-analytics/predictive-maintenance/10-predictive-maintenance-platforms-for-manufacturing-2026/); [Overview.ai](https://www.overview.ai/blog/top-10-agentic-ai-tools-manufacturing-2026/) | SOLO-SNIPPET (listicles/marketing) | Baja |

Aviso: blogs de OxMaint con cifras como 43% menos downtime son marketing sin cita verificable; no usar.

### Inferences
- (Inferencia) Existen dos arquitecturas distintas: ML de detección de anomalías específico por activo (Mtell, Senseye, Augury, Samotics) y capas LLM sobre texto/OT (Maximo, MaintainX, Fiix, Cognite). Un agente de confiabilidad completo necesita ambas.
- (Inferencia) Ningún proveedor mostró en lo visto un FMEA/RCM asistido con trazabilidad; la genAI comercial se concentra en OT, manuales y códigos de falla.

### Gaps
- NO-VERIFICADO / sin evidencia en esta sesión: Uptake, AVEVA (PI, Predictive Analytics), Honeywell Forge, SKF Enlight/Insight, Emerson, Bentley, Hexagon, UpKeep, C3 AI Reliability en detalle (las búsquedas no devolvieron páginas de estos). Tampoco se verificó ninguna página primaria de IBM, AspenTech, GE Vernova por ENOTFOUND.
- Sin tasas de falsa alarma, precisión ni lead time agregados e independientes para ninguna plataforma.

## 2. Literatura académica 2023-2026

### Takeaway
La literatura es mayormente preprints; muestra que los LLM ayudan en clasificación de modos de falla (con fine-tuning), ideación de FMEA y análisis de bitácoras, pero requieren revisión experta. No pude abrir ningún paper (arxiv bloqueado, Elicit sin acceso); los datos vienen de snippets.

### Cited Findings
| Ítem (título · autores · año · venue) | Qué demuestra / límites | Fuente | Estado |
|---|---|---|---|
| Large Language Models for Failure Mode Classification: An Investigation · Stewart, Hodkiewicz, Li · sep. 2023 · arXiv | GPT-3.5 fine-tuned F1 0.80 vs 0.60 clasificador de texto convencional vs 0.46 GPT-3.5 sin ajuste; clave es la calidad de datos de ajuste | [arXiv 2309.08181](https://arxiv.org/abs/2309.08181v1) | SOLO-SNIPPET |
| Exploratory Semantic Reliability Analysis of Wind Turbine Maintenance Logs using LLMs · Malyi y coautores · sep. 2025 · arXiv | 1.065 logs de convertidor: 15 modos de falla distintos; modos, cadenas causales, auditoría de calidad de datos; "reliability co-pilots" | [arXiv 2509.22366](https://arxiv.org/pdf/2509.22366) | SOLO-SNIPPET |
| AssetOpsBench: Benchmarking AI Agents for Task Automation in Industrial Asset Operations and Maintenance · IBM Research · arXiv 2506.03828 (v2 mar. 2026) | 4 agentes (IoT, FMSR, TSFM, WO), 140+ consultas; compara Tool-As-Agent vs Plan-Executor; tabla de resultados no vista | [arXiv](https://arxiv.org/html/2506.03828v1); [IBM blog](https://researchweb.draco.res.ibm.com/blog/asset-ops-benchmark) | SOLO-SNIPPET |
| Chat-of-Thought: Collaborative Multi-Agent System for Generating Domain Specific Information · IBM Research · 2025 · arXiv | Multiagente con roles para generar y validar tablas FMEA de activos industriales, con rondas de discusión multi-persona; resultados no vistos | [arXiv 2506.10086](https://arxiv.org/html/2506.10086v1) | SOLO-SNIPPET |
| Large Language Model Agents as Prognostics and Health Management Copilots · PHM Society conf. | Existe; contenido no visto | [PHM Society](https://papers.phmsociety.org/index.php/phmconf/article/view/3906) | SOLO-SNIPPET (solo título) |
| Multi-agent robotics fault diagnosis with expert knowledge (DOI 10.1007/s10015-026-01136-3) · 2026 | Conocimiento experto recuperado (FMEA) mejora diagnóstico LLM; razonador determinista sobre grafo supera en preguntas por umbral de telemetría | [FAU](https://cris.fau.de/publications/366862216?lang=de_DE) (URL tal cual del resultado: https://cris.fau.de/publications/366862216) | SOLO-SNIPPET |
| AI-driven FMEA: integration of LLMs for faster and more accurate risk analysis · Design Science (Cambridge) · 2025 | GPT-3.5 prueba de concepto; compara GPT-4, GPT-4o, Gemini; reportan mejora en velocidad/exactitud; cifras no vistas | [Cambridge](https://resolve-he.cambridge.org/core/journals/design-science/article/aidriven-fmea-integration-of-large-language-models-for-faster-and-more-accurate-risk-analysis/22F110A2BF0DB4D01A69472CF17A0B43) | SOLO-SNIPPET |
| How good are LLMs at product risk assessment? · Virginia Tech | ChatGPT bueno en lluvia de ideas de modos de falla/mitigaciones, pero con errores, inconsistencias y guía genérica | [VTechWorks](https://vtechworks.lib.vt.edu/items/01506cca-0075-4ffe-8553-49ede6fb6d90) | SOLO-SNIPPET |
| AI Powered FMEA in Safety Critical Industry · SAE 2026-01-0106 | Extracción de señales/categorización 92%; puntuación S/O/D 70-90% vs verdad de experto; LLM no crea medidas de detección fiables | [SAE](https://saemobilus.sae.org/papers/ai-powered-failure-mode-effect-analysis-safety-critical-industry-2026-01-0106) | SOLO-SNIPPET |
| Exploring LLM-based Agents for Root Cause Analysis · Roy et al. · FSE 2024 (Microsoft) | Agente ReAct con recuperación; mayor exactitud factual; dominio incidentes de nube, no mantenimiento | [Microsoft Research](https://www.microsoft.com/en-us/research/publication/exploring-llm-based-agents-for-root-cause-analysis/) | SOLO-SNIPPET |
| Agentic AI in Smart Manufacturing: Human-Centric Predictive Maintenance Ecosystems · Comillas · 2025 | Piloto en planta cerámica con 43% menos paros no planificados (dato de un solo piloto, vía snippet) | [Comillas](https://repositorio.comillas.edu/xmlui/handle/11531/106744) | SOLO-SNIPPET |

### Inferences
- (Inferencia) Patrón repetido: LLM bueno en generación/ideación y clasificación con ajuste; débil en puntuación fiable, medidas de detección y cálculo numérico, por lo que conviene combinar LLM con razonadores deterministas (ver robótica FAU).

### Gaps
- Elicit no disponible; cobertura incompleta de IEEE/Elsevier/MDPI (no se localizó ningún artículo MDPI/Elsevier de minería de OT con LLM). Sin autores completos, DOI ni resultados numéricos verificados de AssetOpsBench ni de Chat-of-Thought.

## 3. Benchmarks, evaluaciones y riesgos

### Takeaway
AssetOpsBench es el único benchmark específico de agentes de mantenimiento hallado; los riesgos documentados son alucinación, respuestas genéricas, falta de trazabilidad y necesidad de supervisión humana.

### Cited Findings
- AssetOpsBench: 140+ consultas, simulación IoT, evaluación automática de respuesta final y pasos intermedios; v2 describe 141 escenarios centrados en chillers HVAC (resumen secundario hyper.ai); plataforma pública con 250+ usuarios y 500+ agentes — [IBM blog](https://researchweb.draco.res.ibm.com/blog/asset-ops-benchmark); [arXiv](https://arxiv.org/html/2506.03828v1); [hyper.ai](https://hyper.ai/en/papers/2606.19704) (SOLO-SNIPPET). Un agregador lista 11 modelos con mejor puntaje normalizado 67,6 (no verificado contra el paper) — [theresanaiforthat](https://theresanaiforthat.com/benchmark/assetopsbench/).
- Revisión humana siempre requerida en MaintainX CoPilot — [Help MaintainX](https://help.getmaintainx.com/complete-a-work-order-with-maintainx-copilot).
- Cognite exige confirmación explícita y permisos para herramientas de ejecución — [Cognite](https://www.cognite.com/en/resources/blog/cognite-atlas-ai-september-product-release-accelerating-agentic-ai-at-scale).
- Errores/inconsistencias y guía genérica en LLM para riesgo de producto — [VTechWorks](https://vtechworks.lib.vt.edu/items/01506cca-0075-4ffe-8553-49ede6fb6d90).

### Inferences
- (Inferencia) Seguridad OT: no hallé fuente específica de ciberseguridad OT para agentes; solo el control de permisos de Cognite apunta a ello.

### Gaps
- No se vio la tabla de resultados de AssetOpsBench. Sin evaluación independiente de ningún agente comercial. Sin fuente sobre seguridad OT.

## 4. Checklist de capacidades de los mejores sistemas (INFERENCIA, no hecho)

### Takeaway
Síntesis propia, marcada como inferencia, a partir de las fuentes de las secciones 1-3.

### Cited Findings
- Ver secciones previas; este apartado no añade hechos nuevos.

### Inferences
1. Limpieza y normalización de códigos de falla/OT con LLM (Maximo 9.0, Verdantix; Stewart et al. 2023).
2. Detección de anomalías/firmas de falla por modo de falla desde historian (Mtell; Senseye).
3. Recuperación de casos similares y RAG sobre manuales con citación al activo (Senseye, MaintainX).
4. Conversión de alerta a orden de trabajo prescriptiva editable, enviable a cualquier CMMS (Fiix).
5. Grafo de conocimiento/contexto de activos para RCA agéntico (Cognite; Aker BP; robótica FAU).
6. Combinación de LLM con razonadores deterministas y herramientas de series de tiempo (FAU; AssetOpsBench).
7. Humano en el bucle, permisos por herramienta y confirmación explícita (MaintainX, Cognite).
8. Evaluación con benchmark propio de escenarios (AssetOpsBench) y revisión experta para FMEA (Virginia Tech, SAE).

### Gaps
- Estas capacidades no están validadas como "las de los mejores" por ranking independiente; es una síntesis sobre evidencia parcial y de proveedor.
