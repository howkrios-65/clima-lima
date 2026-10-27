# Ecosistema abierto para confiabilidad, análisis de falla y mantenimiento predictivo (fecha de consulta: 2026-10-27)

Nota de método y limitaciones de acceso (leer primero):
- Alcanzables: pypi.org (JSON API), raw.githubusercontent.com, Hugging Face (MCP), WebSearch (snippets), un WebFetch a github.com/nasa/progpy.
- NO alcanzables (proxy 403 / DNS): api.github.com/repos/* ("GitHub access not enabled for this session"), github.com (salvo una página), cran.r-project.org, crandb, archive.ics.uci.edu, www.nasa.gov, kaggle.com, backblaze.com, zenodo.org. Consecuencia: NO hay estrellas ni fecha de último commit para casi ningún repo; la "última actividad" de librerías = fecha de última release en PyPI (VERIFICADO vía pypi.org/pypi/<pkg>/json). Paquetes R (survival, flexsurv, WeibullR) = NO-VERIFICADO. Kaggle = NO-VERIFICADO (sin acceso).
- Estados: VERIFICADO = visto en página/API abierta por mí; SOLO-SNIPPET = visto sólo en resumen de búsqueda; NO-VERIFICADO = no pude abrir.

## 1. Librerías Python/R de confiabilidad, supervivencia, series de tiempo, anomalías y prognostics

### Takeaway
Hay base sólida y activa en Python para supervivencia (lifelines, scikit-survival), series/anomalías (sktime, darts, PyOD, tsfresh, stumpy) y prognostics (ProgPy, release 2026-10-23). Alertas de licencia: scikit-survival es GPL-3.0 y `reliability` es LGPLv3; ProgPy usa NASA-1.3/NOSA (no OSI estándar). Merlion y pycox sin release desde 2024 (riesgo de mantenimiento). Paquetes R no verificados.

### Cited Findings
Tabla (última actividad = fecha de subida de la última release en PyPI; stars no disponibles salvo ProgPy):

| Ítem | Qué es / cubre | URL | Licencia (metadato PyPI) | Última versión · fecha | Estado | Idoneidad / riesgo |
|---|---|---|---|---|---|---|
| lifelines | Supervivencia: KM, Nelson-Aalen, Cox, AFT (Weibull, LogNormal…), censura derecha/izq/intervalo | https://github.com/CamDavidsonPilon/lifelines | MIT | 0.30.3 · 2026-03-05 (changelog: re-publicación, exige Python>=3.11) | VERIFICADO (PyPI+changelog raw) | Alta para supervivencia/Weibull con censura. No modela reparables (procesos de renovación/NHPP) de forma nativa; inferencia: usar otro módulo para eso. |
| reliability | Ingeniería de confiabilidad: ajuste Weibull/otras distribuciones con censura, ALT, Weibull mixtos, crecimiento de confiabilidad, RBD/Fault tree en versión reciente (ver docs) | https://reliability.readthedocs.io/en/latest/ (repo MatthewReid854/reliability) | LGPLv3 | 0.9.0 · 2025-03-07 | VERIFICADO (PyPI; README raw confirma badge LGPLv3, CI, DOI Zenodo) | Muy idónea para Weibull/ALT; >12 meses sin release a 2026-10-27 (mantenimiento lento). LGPL: ok usar como librería sin modificarla; revisar si se redistribuye. Cobertura de reparables: NO-VERIFICADO. |
| scikit-survival | Cox penalizado, Random Survival Forest, gradient boosting survival, SVM survival; métricas (C-index, IBS) | https://github.com/sebp/scikit-survival | GPL-3.0-or-later | 0.28.0 · 2026-07-05 | VERIFICADO (PyPI) | Técnicamente fuerte (censura derecha). GPL-3: riesgo de copyleft si se integra/distribuye en producto cerrado; uso interno/SaaS sin distribución suele ser menos problemático (consultar legal). |
| pycox | Supervivencia con redes neuronales PyTorch (DeepSurv, DeepHit, Cox-Time...) + datasets | https://github.com/havakv/pycox | BSD-2 (README badge raw) / "BSD license" PyPI | 0.3.0 · 2024-09-04 | VERIFICADO | Útil para experimentos; >2 años sin release; riesgo de compatibilidad con PyTorch reciente (inferencia, no probado). |
| sktime | Framework unificado de series: forecast, clasificación, anomalías (parcial), clustering | https://www.sktime.net / https://github.com/sktime/sktime | BSD-3 | 1.2.0 · 2026-09-22 | VERIFICADO | Alta; activa. |
| darts | Forecasting + detección de anomalías, modelos locales/globales/DL | https://github.com/unit8co/darts | Apache-2.0 | 0.48.1 · 2026-10-16 | VERIFICADO | Alta; muy activa. |
| tsfresh | Extracción automática de features de series + selección | https://github.com/blue-yonder/tsfresh | MIT | 0.21.2 · 2026-05-31 | VERIFICADO | Útil para features de vibración/sensores; cuidado con fuga al seleccionar features con todo el set. |
| PyOD | Detección de anomalías (>40 algoritmos, tabulares) | https://github.com/yzhao062/pyod ; docs https://pyod.readthedocs.io | BSD-2 | 3.6.7 · 2026-10-12 | VERIFICADO | Alta; activa. |
| Merlion (salesforce-merlion) | Forecast + anomalías + change-point, benchmarking | https://github.com/salesforce/Merlion | BSD-3 | 2.0.4 · 2024-06-20 | VERIFICADO (PyPI; README raw) | Media-baja: >2 años sin release. No incorporar como dependencia núcleo. |
| stumpy | Matrix profile (motivos, discords) | https://github.com/stumpy-dev/stumpy | BSD-3 | 1.14.1 · 2026-02-08 | VERIFICADO | Buena para anomalías en series; moderado ritmo. |
| ProgPy (NASA) | Prognostics model-based/data-driven, RUL con propagación de incertidumbre; incluye prog_models+prog_algs | https://github.com/nasa/progpy ; https://nasa.github.io/progpy/ | NOSA / NASA-1.3 (PyPI "NASA-1.3"; README badge "NOSA") | 1.9.0 · 2026-10-23 (PyPI). prog_algs 1.5.1 · 2023-08-18 (absorbido) | VERIFICADO (PyPI, README raw, WebFetch GitHub: 136 estrellas, 733 commits, Releases vacío) | Alta técnica (README: "2024 NASA Software of the Year"). Licencia NOSA no es OSI/permisiva estándar: revisión legal antes de incorporar. |
| tslearn | ML de series (DTW, clustering) | https://github.com/tslearn-team/tslearn | BSD-2 | 0.10.0 · 2026-10-22 | VERIFICADO | Complementaria. |
| statsforecast (Nixtla) | Forecast estadístico rápido | https://github.com/Nixtla/statsforecast | Apache | 2.1.1 · 2026-07-16 | VERIFICADO | Complementaria. |
| MLflow | Tracking/registro de modelos, ahora también tracing de agentes LLM | https://mlflow.org ; https://github.com/mlflow/mlflow | PyPI muestra "Copyright 2018 Databricks…" (texto Apache-2.0 implícito, NO leí SPDX) | 3.17.2 · 2026-10-21 | VERIFICADO versión/fecha; licencia exacta SOLO-metadato | Recomendada para MLOps. Confirmar Apache-2.0 en LICENSE antes de aprobar. |
| R: survival, flexsurv, WeibullR, ReliaGrowR, SPREDA | Supervivencia/Weibull en R | cran.r-project.org/web/packages/<pkg> | — | — | NO-VERIFICADO (CRAN inaccesible) | No afirmo versión ni licencia. Verificar luego. |

- Los metadatos de licencia y fechas de arriba provienen de https://pypi.org/pypi/<paquete>/json (consulta directa, 2026-10-27), p. ej. [lifelines](https://pypi.org/pypi/lifelines/json), [progpy](https://pypi.org/pypi/progpy/json), [scikit-survival](https://pypi.org/pypi/scikit-survival/json).
- ProgPy: "combina prog_models y prog_algs", "pip3 install progpy", "2024 NASA Software of the Year" — [README](https://raw.githubusercontent.com/nasa/progpy/master/README.md); 136 stars y 733 commits en [GitHub](https://github.com/nasa/progpy) (WebFetch).
- lifelines changelog 0.30.3 (2026-03-05) exige Python >= 3.11 — [CHANGELOG](https://raw.githubusercontent.com/CamDavidsonPilon/lifelines/master/CHANGELOG.md).
- `reliability`: LGPLv3, CI de GitHub Actions, DOI Zenodo — [README](https://raw.githubusercontent.com/MatthewReid854/reliability/master/README.md).
- Merlion: cubre forecasting, anomalías y change-point uni/multivariados — [README](https://raw.githubusercontent.com/salesforce/Merlion/master/README.md).

### Inferences
- Para Weibull con censura, la combinación `reliability` (LGPL) + lifelines (MIT) cubre el núcleo; ninguna fuente que vi confirma soporte de sistemas reparables (NHPP/Crow-AMSAA); no asumir.
- scikit-survival (GPL-3) y ProgPy (NOSA) requieren decisión de licencia explícita antes de empaquetar en un agente distribuido.

### Gaps
- Estrellas y último commit de casi todos los repos (API/GitHub bloqueados). Versiones y licencias de paquetes R (CRAN bloqueado). Licencia SPDX exacta de MLflow. Si `reliability` maneja reparables: no verificado.

## 2. Datasets públicos de PdM / falla

### Takeaway
Sólo pude verificar directamente metadatos de Backblaze (vía HF) y de repos "awesome" de rodamientos; el resto es SOLO-SNIPPET. Hay dos alertas fuertes: AI4I es sintético y sin identidad de unidad/tiempo (no sirve para RUL), y Paderborn es CC BY-NC (uso comercial restringido). No encontré dataset público real de órdenes de trabajo; sólo sintéticos en HF.

### Cited Findings
| Dataset | Origen oficial | Tamaño / tipo | Licencia / términos | Tarea apta | Defectos / notas | Estado |
|---|---|---|---|---|---|---|
| AI4I 2020 | UCI, DOI 10.24432/C5HS5C (paper S. Matzka) | 10 000 filas, sintético, tabular | CC BY 4.0 | Clasificación de falla | Sintético; ~3.39% fallas según proyecto de terceros; sin unidad ni tiempo → no apto para RUL/supervivencia | SOLO-SNIPPET (UCI no abrió) [búsqueda](https://archive.ics.uci.edu/dataset/601); crítica de ausencia de unidad/tiempo vista en [README de un dataset HF](https://huggingface.co/datasets/rasinmuhammed/predictive-maintenance-remaining-useful-life) (VERIFICADO texto, opinión del autor) |
| NASA C-MAPSS / N-CMAPSS | NASA PCoE (Prognostics Data Repository) | Simulación turbofan; trayectorias hasta falla | NO-VERIFICADO (sitio NASA inaccesible) | RUL | Prácticas dispares: cap RUL=125, selección de subsets y normalización por condición operativa cambian conclusiones; preprint auditó fuga con ajuste de preprocesado ([engrXiv 8145](https://engrxiv.org/preprint/view/8145), SOLO-SNIPPET); N-CMAPSS añade más decisiones de evaluación ([arXiv 2607.19380](https://arxiv.org/pdf/2607.19380), SOLO-SNIPPET) | SOLO-SNIPPET |
| CWRU bearing | Case Western Reserve Univ. Bearing Data Center | Vibración, fallas artificiales (EDM) | NO-VERIFICADO | Diagnóstico | Fallas artificiales, sin defectos combinados; fácil de clasificar, riesgo de resultados optimistas ([arXiv 2509.22267](https://arxiv.org/pdf/2509.22267), SOLO-SNIPPET) | SOLO-SNIPPET |
| FEMTO/PRONOSTIA (PHM 2012) | FEMTO-ST | 17 trayectorias run-to-failure, 3 condiciones; vibración 25.6 kHz | NO-VERIFICADO | RUL de rodamientos | Pocas unidades; fuentes discrepan en tasas de muestreo secundarias | SOLO-SNIPPET |
| XJTU-SY | Xi'an Jiaotong Univ. + Sumyoung | 15 run-to-failure, 3 condiciones, snapshots 1.28 s cada 1 min | NO-VERIFICADO | RUL | — | SOLO-SNIPPET; listado en [awesome-bearing-dataset](https://raw.githubusercontent.com/VictorBauler/awesome-bearing-dataset/main/README.md) (VERIFICADO) |
| IMS bearing (NASA) | NASA PCoE / Univ. Cincinnati | Run-to-failure | NO-VERIFICADO | RUL/anomalías | No verifiqué | NO-VERIFICADO |
| Paderborn (KAt-DataCenter) | Univ. Paderborn | 6 sanos, 12 daño artificial, 14 daño real; vibración + corriente motor | CC BY-NC 4.0; uso académico no comercial con cita | Diagnóstico, transferencia | Brecha de dominio artificial vs. real ([sitio oficial](https://mb.uni-paderborn.de/kat/forschung/kat-datacenter/bearing-datacenter) visto sólo en snippet) | SOLO-SNIPPET |
| Microsoft Azure PdM (Kaggle, arnabbiswas1) | Muestra de Azure AI Notebooks | Telemetría horaria 100 máquinas, 2015; errores, mantenimiento, fallas | NO-VERIFICADO | Falla a horizonte; datos tipo OT mínimos | Distinto de "PdM_telemetry" sintético de IEEE DataPort (DOI 10.21227/q7ae-2809) | SOLO-SNIPPET |
| Backblaze Drive Stats | Backblaze (también HF `backblaze/Drive_Stats`) | >388 M registros (snapshot al Q2 2023 en README), SMART diario, columna Failure | HF: license "other", términos en página de Backblaze; blog dice MIT + atribución, sin reventa (conflicto → leer términos) | Supervivencia con censura, fallas | Datos de discos, no de equipos industriales; fallo = último día | VERIFICADO (README HF [backblaze/Drive_Stats](https://huggingface.co/datasets/backblaze/Drive_Stats)); licencia contradictoria SOLO-SNIPPET [blog](https://www.backblaze.com/blog/backblaze-drive-stats-academic-ai-ml-research/) |
| Datos HF de PdM (comunidad) | HF Hub | Varios; ej. `rasinmuhammed/predictive-maintenance-remaining-useful-life` (sintético, 100 máquinas, 23 118 lecturas, MIT, creado 2026-08-19) | por repo | Pruebas de pipeline | Sintéticos de autores individuales, 20–200 descargas: NO usar como evidencia | VERIFICADO ([lista HF](https://huggingface.co/datasets/rasinmuhammed/predictive-maintenance-remaining-useful-life)) |
| Órdenes de trabajo (OT) | — | HF: `electricsheepafrica/africa-synth-telecom-maintenance-work-orders-nigeria` (sintético, license:other, 63 descargas) | other | Prototipos NLP | Sintético; no encontré corpus real público de OT | VERIFICADO sólo metadatos [HF](https://huggingface.co/datasets/electricsheepafrica/africa-synth-telecom-maintenance-work-orders-nigeria) |

- HF C-MAPSS: sólo copias de usuario con FD002 (`uncledecart/…`, apache-2.0 declarado por el subidor, sin garantía de que pueda relicenciar) — [HF](https://huggingface.co/datasets/uncledecart/cmapss-turbofan-preprocessed).
- Kaggle: no pude abrir ninguna página; cualquier ranking de uso en Kaggle es NO-VERIFICADO.

### Inferences
- Para validar RUL: C-MAPSS/N-CMAPSS y rodamientos run-to-failure; separar por unidad (no por fila) para evitar fuga.
- Para un agente comercial, Paderborn (NC) queda fuera salvo uso de investigación.

### Gaps
- Licencia/términos de NASA (C-MAPSS, IMS), CWRU, FEMTO, XJTU-SY y Azure; tamaños en MB; Kaggle completo; UCI para otros datasets; corpus real de OT.

## 3. Listas "awesome-*", repos de agentes LLM/RAG/MCP de mantenimiento

### Takeaway
Encontré listas útiles pero pequeñas, con licencia MIT. No encontré en GitHub un repo maduro de agente/MCP que combine CMMS+FMEA+RCA; lo hallado son conectores comerciales o conceptuales y papers sin código visible.

### Cited Findings
| Ítem | Qué es | URL | Licencia | Actividad vista | Estado | Calidad |
|---|---|---|---|---|---|---|
| awesome-bearing-dataset | Catálogo de datasets de rodamientos (diagnóstico/prognosis) con ranking por citas (OpenAlex, sep-2026) y docs; librería asociada BearingDatasets | https://github.com/VictorBauler/awesome-bearing-dataset | MIT | README cita datos de septiembre 2026 | VERIFICADO (raw) | Buena como índice |
| RUL-Papers | Lista de papers arXiv sobre RUL/SOH/PdM + CSV | https://github.com/RamtinMoslemi/RUL-Papers | MIT | WebSearch: 9 stars (SOLO-SNIPPET) | VERIFICADO README/licencia | Índice bibliográfico, no código |
| rul_codes_open | Código reproducible de RUL con ML sobre datasets públicos | https://github.com/biswajitsahoo1111/rul_codes_open | MIT | sin fecha visible | VERIFICADO README/licencia | Educativo; código no auditado por mí |
| RCA-MCP Connector | MCP que expone PyRCA (Salesforce) para anomalías/localización causa raíz; incluye prompt FMEA | https://glama.ai/mcp/servers/dave1362/rca-mcp-connector | NO-VERIFICADO (plan de pago $19/mes citado en el listado) | — | SOLO-SNIPPET | Posible marketing; no revisé código/tests |
| MCP "CMMS" en Glama | Servidor MCP para MES/CMMS/IoT | https://glama.ai/mcp/servers/jr2dbu8bx0 (sin verificar cuál de los dos IDs) | NO-VERIFICADO | — | SOLO-SNIPPET | No incorporar sin revisión |
| Composio MaintainX MCP | Integración hosted comercial para CMMS MaintainX | https://composio.dev/toolkits/maintainx | Comercial | — | SOLO-SNIPPET | No es repo abierto |
| PARAM (arXiv 2508.04714) | Agentes prescriptivos con RAG sobre vibración de rodamientos y manuales | https://arxiv.org/html/2508.04714v1 | — | Sin código visto | SOLO-SNIPPET | Referencia de diseño |
| RAG mantenimiento UAV (UAH) | RAG con LangChain+Chroma+Ollama (Qwen3) sobre manuales | https://ebuah.uah.es/dspace/handle/10017/68495 | — | Sin código público visto | SOLO-SNIPPET | Referencia de diseño |

### Inferences
- Construir el agente sobre bibliotecas estándar y tratar los MCP de terceros como inspiración, no dependencia.

### Gaps
- No pude buscar en GitHub (search y API bloqueados); no hay inventario real de awesome-PHM ni de repos de agentes con estrellas/tests. Se requiere nueva pasada con acceso a GitHub.

## 4. Modelos fundacionales de series de tiempo

### Takeaway
Chronos-2 (Apache-2.0), TimesFM (Apache-2.0) y MOMENT (MIT) son de licencia permisiva; no encontré fuente de uso demostrado en PdM industrial, así que su valor es hipótesis a validar.

### Cited Findings
| Modelo | URL | Licencia | Actividad vista | Estado | Notas |
|---|---|---|---|---|---|
| Chronos-2 (120M, forecasting zero-shot, multivariado y covariables) | https://huggingface.co/amazon/chronos-2 ; paquete `chronos-forecasting` 2.3.2 · 2026-09-08 | Apache-2.0 | HF actualizado 2026-06-05; 13.4 M descargas (amazon/) | VERIFICADO | Tareas: forecasting; no anomalías/RUL directo |
| TimesFM 2.5 / 3.0 | https://huggingface.co/google/timesfm-3.0-pytorch ; paquete `timesfm` 3.0.2 · 2026-09-09 | Apache-2.0 (README 2.5 y PyPI) | HF 3.0 actualizado 2026-09-02 | VERIFICADO (licencia 2.5/PyPI); licencia de 3.0 en HF no leída | README: "not an officially supported Google product" |
| MOMENT-1 | https://huggingface.co/AutonLab/MOMENT-1-large ; `momentfm` 0.1.4 · 2025-03-19 | MIT | PyPI sin release en >1 año | VERIFICADO | Soporta forecasting, clasificación, anomalías (reconstrucción), imputación |
| Moirai 2.0 (Salesforce) | https://huggingface.co/Salesforce/moirai-2.0-R-small | NO leída | HF 2026-01-29 | SOLO listado | — |

- Evidencia de uso en PdM: no la encontré en las fuentes abiertas (los README citan benchmarks de forecasting GIFT-Eval/fev-bench, no PdM) — [Chronos-2 README](https://huggingface.co/amazon/chronos-2).

### Inferences
- Útiles como baseline de forecast de telemetría o extracción de embeddings; no sustituyen modelos de supervivencia.

### Gaps
- Papers de FM en PdM no buscados/verificados.

## 5. Recomendación priorizada por tarea del agente

### Takeaway
Priorizar librerías permisivas y activas; marcar para revisión legal GPL/LGPL/NOSA. Todo lo dependiente de datos/CRAN/Kaggle queda pendiente de verificación.

### Cited Findings
(Recomendación = inferencia basada en las tablas anteriores.)

| Tarea | Primera opción | Alternativa | Riesgos de licencia/mantenimiento |
|---|---|---|---|
| Weibull / distribuciones con censura | `reliability` (LGPLv3, 0.9.0, 2025-03) | lifelines WeibullFitter/AFT (MIT); R WeibullR/flexsurv (NO-VERIFICADO) | LGPL: usar como dependencia, no copiar; release >12 meses |
| Supervivencia / Cox | lifelines (MIT, 2026-03) | scikit-survival (GPL-3), pycox (BSD, 2024) | GPL-3 contagio si se distribuye; pycox poco mantenido |
| Reparables (NHPP/Crow-AMSAA) | No identificado en fuentes verificadas | Implementación propia / `reliability` (cobertura NO-VERIFICADA) | Brecha |
| RUL / prognostics | ProgPy (NOSA; release 2026-10-23) | Modelos propios sobre sktime/darts | NOSA: revisión legal |
| Anomalías en tabulares/series | PyOD (BSD-2, 2026-10) + stumpy | darts, sktime; MOMENT (MIT) | Evitar Merlion como núcleo (sin release desde 2024-06) |
| Features de series | tsfresh (MIT) | — | Fuga en selección de features |
| Forecast base | darts / statsforecast / Chronos-2 (Apache) | TimesFM, MOMENT | Sin evidencia PdM |
| NLP de OTs | No hay corpus abierto real verificado; sólo sintético en HF | — | Evitar datasets sintéticos de HF como validación |
| RAG / agente | Diseño propio; referencias PARAM/UAH | MCP de terceros (RCA-MCP, CMMS) sólo tras auditar código | SOLO-SNIPPET, posible marketing |
| MLOps | MLflow (3.17.2, 2026-10-21) | — | Confirmar licencia SPDX |
| Validación de datasets | C-MAPSS/N-CMAPSS, XJTU-SY, FEMTO (licencias por verificar); Backblaze para censura | AI4I sólo clasificación; Paderborn NC excluido para comercial | Fuga por split de filas en vez de unidades |

### Gaps
- Todo lo marcado NO-VERIFICADO: CRAN, términos NASA/CWRU/FEMTO/XJTU/Azure, Kaggle, estrellas/commits GitHub, repos de agentes con código.
