# ML/DL para mantenimiento predictivo, RUL, anomalías y pronóstico: estado del arte, evidencia y fallas metodológicas

**Fecha de corte:** 2026-10-27. **Cobertura honesta:** esta es una síntesis PARCIAL, con evidencia mayormente de segunda mano.

**Estados usados:**
- VERIFICADO-ABSTRACT: abstract completo leído vía Wiley Scholar Gateway.
- SOLO-SNIPPET: resumen devuelto por WebSearch. No abrí el paper.
- NO-VERIFICADO: lo menciono como pista de búsqueda, sin fuente leída.

**Fallos de acceso (todos probados):**
- Elicit (`search_papers`) devolvió `api_access_denied`: el plan no incluye API. Se intentó 2 veces.
- `WebFetch` falló con `getaddrinfo ENOTFOUND` para arxiv.org, engrxiv.org, papers.phmsociety.org, peerj.com y datascience.ucr.edu.
- `curl` vía proxy devolvió 403 CONNECT para arxiv, export.arxiv y ncbi.
- Resultado: NINGÚN paper de arXiv, IEEE, ScienceDirect ni MDPI fue abierto. Todo lo de arXiv/PHM Society es SOLO-SNIPPET. Solo Wiley dio abstracts completos.
- Las cifras de desempeño de este documento se copian tal cual del snippet o abstract y deben re-verificarse antes de citarlas.
- No se usaron herramientas `mcp__github__*`.

---

## 1. Revisiones sistemáticas y surveys 2021–2026 (PdM / PHM / RUL)

### Takeaway
Los surveys coinciden en los límites: generalización entre equipos y condiciones, variabilidad e irregularidad de los datos, interpretabilidad y escasez de datos de falla. Ninguno de los que pude ver aporta evidencia de ROI en planta.

### Cited Findings

| Paper | Año | Tipo | Hallazgo clave | Límite declarado | DOI/URL | Estado |
|---|---|---|---|---|---|---|
| Wu et al., marco unificado de DL para RUL (Sensors 24(11)) | 2024 | Survey | Propone un marco unificado y compara tipos de modelos DL. Los métodos tradicionales requieren diseño manual de features y su precisión es limitada. | No conocido; no abrí el texto | 10.3390/s24113454 | SOLO-SNIPPET |
| "State-of-the-art AI approaches for anomaly detection and RUL prediction: a review" (PeerJ CS) | ~2024 | Revisión PRISMA | Persisten retos de generalización entre tipos de equipo y contextos operativos; variabilidad de datos; deterioro irregular; interpretabilidad. | Autores y DOI no confirmados | https://peerj.com/articles/cs-3056 | SOLO-SNIPPET |
| "A Survey on GNNs for RUL Prediction: Methodologies, Evaluation and Future Trends" | 2024 | Survey | Incluye una comparación experimental estandarizada de varios métodos. | Desconocido | arXiv:2409.19629 | SOLO-SNIPPET |
| Ramasso & Saxena, "Review and Analysis of Algorithmic Approaches Developed for Prognostics on CMAPSS Dataset" (PHM Conf.) | 2014 (fuera de rango, útil como base) | Revisión | Revisa más de 70 publicaciones sobre C-MAPSS. | Desconocido | https://papers.phmsociety.org/index.php/phmconf/article/view/2512 | SOLO-SNIPPET |
| Afridi, Ahmad & Hassan, "AI-based prognostic maintenance of renewable energy systems" (Int. J. Energy Res. 46(15)) | 2021 | Review | Retos: disponibilidad de datos de calidad, auditoría de datos, feature engineering, compromiso rendimiento/explicabilidad, robustez ante fallas nuevas. | Dominio renovables | 10.1002/er.7100 | VERIFICADO-ABSTRACT; el pasaje de retos es texto completo vía Wiley |
| Feisa et al., "Comprehensive Review of Deep Transfer Learning for Intelligent Fault Diagnosis in Rotating Machines" (Engineering Reports 7(11)) | 2025 | Review | Los DTL se prueban offline; no contemplan cambios en tiempo real. El envejecimiento del equipo y los cambios operativos causan distribution shift. | Foco en diagnóstico, no en RUL | 10.1002/eng2.70494 | VERIFICADO-ABSTRACT y pasaje |
| Kollu & Kittur, "Integrating DL into Mechanical Engineering: Systematic Review" (Comput. Appl. Eng. Educ. 33(3)) | 2025 | Revisión sistemática (49 de 149 estudios) | Afirma mejoras de precisión de 10 a 35 % sobre técnicas tradicionales. Persisten problemas de datos, cómputo e interpretabilidad. | Revisión amplia, no específica de PdM; la cifra agrega comparaciones heterogéneas | 10.1002/cae.70048 | VERIFICADO-ABSTRACT |

### Inferences
- La cifra "DL mejora 10–35 %" no debe usarse como estimación de efecto. Agrega estudios heterogéneos y probablemente hereda los sesgos de la sección 2.

### Gaps
- Faltan los surveys clave de RESS, MSSP, IEEE TII y Neurocomputing (Zhang et al. 2017 sobre DL para RUL y otros 2021–2026). No pude abrirlos; sin DOI verificado no los listo.
- No encontré una revisión sistemática que mida directamente la tasa de errores metodológicos en la literatura de RUL.

---

## 2. Benchmarks, críticas de uso y métricas

### Takeaway
Los benchmarks se pueden inflar con particiones filtradas y con el preprocesamiento. Hay evidencia directa para CWRU y para C-MAPSS, aunque ambas son SOLO-SNIPPET. La métrica asimétrica de NASA es sensible a outliers.

### Cited Findings

**Críticas a benchmarks**

| Paper | Año | Hallazgo clave | Límite | URL | Estado |
|---|---|---|---|---|---|
| Rosa, Braga & Silva (según el snippet), "Benchmarking deep learning models for bearing fault diagnosis using the CWRU dataset: a multi-label approach" | 2024 | La división habitual de CWRU filtra datos (segmentos de la misma señal repartidos entre train y test) y produce resultados optimistas. Cita a Hendriks et al. 2022 y Abburi et al. 2023 como evidencia previa. Su división reduce el problema pero no lo elimina. Propone formulación multi-label. | CWRU tiene una sola configuración de rodamiento sano; la evaluación libre de fuga es difícil. | arXiv:2407.14625 | SOLO-SNIPPET (los autores y el título salen del snippet) |
| Artículo de 2025 sobre partición por rodamiento físico (arXiv:2509.22267, título no confirmado) | 2025 | Las particiones por segmento o por condición introducen correlaciones espurias. En CWRU, Random Forest 84.40 % vs 74.51 % del mejor modelo DL, según un resumen de alphaXiv. | Configuración exacta no vista. Cifra solo de un resumen de terceros. | arXiv:2509.22267 | SOLO-SNIPPET; la cifra es NO-VERIFICADO |
| Rekem, Prokop, Otipka & Kopeček, "Why Machine Fault Diagnosis Should Not Be Treated as an 'Overfitting Contest'" | 2025 | Argumenta que CWRU debe servir para algoritmos que transfieran a la realidad, no como tabla de posiciones. | Detalle no visto | https://www.fme.vutbr.cz/en/veda/publikace/detail/198698 | SOLO-SNIPPET |
| Rezaei & Mirtalebi, "Quantifying the Impact of Data Cleaning on DL-Based Bearing Fault Diagnosis" (Concurr. Comput.: Pract. Exp. 38(10)) | 2026 | Corrompe CWRU y MFPT de forma controlada. LSTM sufre un colapso de F1 del 56 %; Transformer es más robusto. En CWRU todos los modelos fallaron con fallas de pista externa hasta aplicar limpieza. | Solo diagnóstico, 2 datasets | 10.1002/cpe.70654 | VERIFICADO-ABSTRACT |
| Özüpak & Faravelli (Struct. Control Health Monit. 2026), CNN-BiLSTM-GRU para engranajes | 2026 | Ejemplo de buena práctica: separación a nivel de archivo antes de ventanear, para evitar fuga entre ventanas adyacentes. Reporta ROC-AUC 0.998, F1 0.979 y accuracy 0.980, pero declara que es un escenario acotado y binario. | No generaliza a otras condiciones | 10.1155/stc/8787490 | VERIFICADO-ABSTRACT y pasaje |
| Gupta, auditoría de preprocesamiento y protocolo en C-MAPSS (engrXiv preprint 8145) | s.f. (fecha no confirmada) | El resultado depende tanto del preprocesamiento y del protocolo de evaluación como de la arquitectura. Usa una grilla factorial de 1,080 corridas con control de fuga. | Preprint; fecha, título y resultados numéricos no vistos | https://engrxiv.org/preprint/view/8145 | SOLO-SNIPPET |
| "CruiseBench: A Real-Flight-Aligned N-CMAPSS Benchmark for Engine RUL" | 2026 | Sostiene que los registros de vuelo completo de N-CMAPSS hacen que las decisiones de preprocesamiento pesen mucho; propone evaluar en fase de crucero. | Preprint; resultados no vistos | arXiv:2607.19380 | SOLO-SNIPPET |
| Wu & Keogh, "Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress" | 2020 (se publicó después en IEEE TKDE; no verificado) | Los benchmarks Yahoo, Numenta y NASA tienen cuatro defectos y se crea una ilusión de progreso. Propone el UCR Anomaly Archive. | Fuera del rango 2021–2026, pero fundacional | arXiv:2009.13807 | SOLO-SNIPPET |
| SimAD (arXiv:2405.11238) | 2024 | Con ajuste por puntos (point adjustment), un predictor aleatorio puede obtener un F1 alto. | Lo cita como motivación | arXiv:2405.11238 | SOLO-SNIPPET |

**Métricas de pronóstico**

| Métrica | Qué hace | Fuente | Estado |
|---|---|---|---|
| Score asimétrico NASA (PHM08, C-MAPSS) | Exponencial por rrama (temprano / tardío). Penaliza más la predicción tardía. | Saxena et al. 2008, "Damage propagation modeling for aircraft engine run-to-failure simulation" (IEEE PHM); fuente: https://c3.ndc.nasa.gov/dashlink/static/media/publication/2008_IEEEPHM_CMAPPSDamagePropagation.pdf | SOLO-SNIPPET |
| Críticas al score | Sin normalización del error; un outlier lo domina; una sola métrica no basta. | arXiv:2202.10916 (TDDN) | SOLO-SNIPPET |
| RMSE | Penaliza por igual temprano y tardío. | misma fuente | SOLO-SNIPPET |
| Alpha-lambda, horizonte de predicción, Saxena et al. 2010 "Metrics for offline evaluation of prognostic performance" (IJPHM) | Mencionados como metodología de referencia | Solo se menciona en la bibliografía de Ramasso & Saxena. No recuperé las definiciones. | NO-VERIFICADO (definiciones) |

**Otra cifra de benchmark**
- PHM Society (Chronos-2 embeddings con adaptador Wide & Deep): RMSE promedio 10.32 en "el benchmark C-MAPSS completo" sin ajuste fino del backbone. La configuración exacta (subsets, definición de test, si el RUL se trunca) no se vio. Fuente: https://papers.phmsociety.org/index.php/phme/article/view/4906. SOLO-SNIPPET. No usar para comparar.

### Inferences
- Toda cifra de RMSE de C-MAPSS debe acompañarse del subset (FD001–FD004), la forma de truncar el RUL y si la evaluación fue en el último ciclo de cada motor de test o en todos los ciclos. Sin eso no es comparable.
- Como el score exponencial lo domina un outlier, conviene reportar siempre junto a RMSE/MAE y a la distribución de errores tempranos vs tardíos.

### Gaps
- Los resultados numéricos canónicos de FEMTO/PRONOSTIA, XJTU-SY y N-CMAPSS no fueron verificados.
- No encontré críticas publicadas específicas de FEMTO o XJTU-SY. Es probable que existan, pero no las vi.
- Definición de alpha-lambda: sin recuperar.

---

## 3. Supervivencia con ML, incertidumbre y calibración

### Takeaway
Los modelos de supervivencia aprovechan las unidades censuradas, algo que la regresión de RUL desperdicia o sesga. En PdM industrial no encontré comparaciones directas y revisadas entre RSF y DeepSurv. La conformal prediction ya se aplica a RUL, con garantías que dependen de la intercambiabilidad.

### Cited Findings

| Paper | Año | Hallazgo | Límite | URL | Estado |
|---|---|---|---|---|---|
| SurvLoss (PHM Society) | n/c | Función de pérdida de supervivencia para redes neuronales que usa muestras censuradas; probada en C-MAPSS y un dataset real de camiones SCANIA; supera al baseline. | Cifras no vistas | https://papers.phmsociety.org/index.php/phme/article/view/4052 | SOLO-SNIPPET |
| Ajuste de hiperparámetros de RSF para time-to-failure en PdM | 2025 | RSF es flexible con censura pero sensible a hiperparámetros. | Título y autores no confirmados | arXiv:2504.14744 | SOLO-SNIPPET |
| SurvCF(t), explicaciones contrafactuales en PdM con supervivencia | 2026 | Menciona variantes neuronales de Cox (DeepSurv) y DeepHit sobre secuencias de sensores. | n/c | arXiv:2607.16969 | SOLO-SNIPPET |
| Akkermans, Basten, Zhu & Van Wassenhove, "Transition paths for condition-based maintenance-driven smart services" (J. Oper. Manag. 70(4)) | 2024 | Para entrenar ML se necesitan muchas fallas. Hay un "punto dulce": ni demasiado mantenimiento preventivo (pocas fallas) ni demasiado correctivo no monitoreado. Con fallas muy raras la recolección tarda mucho. | Cuatro OEM, más un modelo de dinámica de sistemas | 10.1002/joom.1295 | VERIFICADO-ABSTRACT |
| Huang et al., DiffUQ (Qual. Reliab. Eng. Int.) | 2026 | RUL con conformal prediction ajustada para dependencias espacio-temporales y datos faltantes. Condición declarada: la conformal estándar supone intercambiabilidad, y los datos de degradación suelen violarla. | Un solo dataset de amplificadores operacionales | 10.1002/qre.70453 | VERIFICADO-ABSTRACT y pasaje |
| Jiang et al., RUL de rodamientos con red bayesiana y UQ (QREI 39(5)) | 2023 | CNN-LSTM bayesiana con intervalos de confianza de la RUL | Sin detalle de calibración visto | 10.1002/qre.3308 | VERIFICADO-ABSTRACT |
| Ramirez et al., B-PINN heteroscedástica (Adv. Intell. Syst. 8(6)) | 2026 | Separa incertidumbre aleatoria y epistémica; mejor precisión y calibración que PINN determinista y dropout. | Aislamiento de transformadores; no es RUL de maquinaria rotativa | 10.1002/aisy.202501502 | VERIFICADO-ABSTRACT |
| Hu et al., RUL probabilística en turbinas eólicas (Wind Energy 28(8)) | 2025 | UQ de RUL por regresión lineal y KDE. Declara falta de datos de degradación y dificultad de interpretar incertidumbres de redes. | Estudio de caso | 10.1002/we.70049 | VERIFICADO-ABSTRACT |

### Inferences
- Para la unidad de falla típica de minería (pocas fallas, mucha censura), supervivencia y modelos de intensidad son el punto de partida natural. Ojo: esto es mi síntesis, no un hallazgo citado.

### Gaps
- No obtuve los papers originales de RSF (Ishwaran 2008) ni de DeepSurv (Katzman 2018), ni métricas de supervivencia con censura (concordance, Brier integrado) con fuente leída.
- No hay un estudio verificado que evalúe la calibración de intervalos de RUL en datos reales de planta.

---

## 4. Detección de anomalías, desbalance y validación

### Takeaway
La fuente más sólida que encontré es la crítica a los benchmarks de anomalías (Wu & Keogh) y a las métricas con point-adjust. Sobre isolation forest y autoencoders industriales no obtuve una fuente comparativa verificada.

### Cited Findings
- Los benchmarks de anomalías en series de tiempo tienen defectos que crean una ilusión de progreso (Wu & Keogh, SOLO-SNIPPET, arXiv:2009.13807). Keogh afirma que "al menos 95 %" de los papers de TSAD están muy defectuosos, según la nota de UCR (SOLO-SNIPPET, https://datascience.ucr.edu/news/2022/09/30/why-95-papers-time-series-anomaly-detection-are-wrong-more-general-lessons). Es una afirmación de opinión de un autor, no una medición.
- El point-adjust puede hacer que un predictor aleatorio obtenga un F1 alto (SimAD, arXiv:2405.11238, SOLO-SNIPPET). Las métricas puntuales ignoran la dependencia temporal y no distinguen detección temprana de tardía (TimeSeAD, TMLR 2023, SOLO-SNIPPET).
- CWRU: desbalance fuerte, con muchas más muestras con falla que sanas (arXiv:2407.14625, SOLO-SNIPPET).
- Validación por activo: un estudio de engranajes asignó archivos completos a los folds antes de ventanear (10.1155/stc/8787490, VERIFICADO-ABSTRACT).

### Gaps
- Sin fuente leída para isolation forest, autoencoders, one-class, y su desempeño relativo en datos industriales.
- Sin fuente sobre costo de falsos positivos en planta, salvo una cita secundaria (sección 7).

---

## 5. Modelos fundacionales de series de tiempo y LLMs

### Takeaway
Hay evidencia temprana de que embeddings congelados de modelos fundacionales sirven como features para RUL. No encontré evidencia robusta de zero-shot RUL. En texto de órdenes de trabajo, el ajuste fino de un LLM supera al enfoque por prompt, y la propia literatura recomienda humano en el lazo.

### Cited Findings

| Paper | Año | Hallazgo | Límite | URL | Estado |
|---|---|---|---|---|---|
| "Time-Series Foundation Model Embeddings for RUL Estimation" | 2026 | Chronos-2 congelado más regresor ligero. Menor error que baselines clásicos y DL en el dataset Nokia; contextos largos ayudan. | Un dataset propietario; preprint | arXiv:2606.11990 | SOLO-SNIPPET |
| "Leveraging TSFM Embeddings for RUL Prediction" (PHM Society) | n/c | Embeddings de Chronos-2 más sensores crudos: RMSE promedio 10.32 en C-MAPSS. Argumenta que las representaciones de pronóstico no capturan la física de degradación sin adaptador. | Configuración no vista | https://papers.phmsociety.org/index.php/phme/article/view/4906 | SOLO-SNIPPET |
| "Can TSFMs Perform Building Energy Management Tasks?" | 2025 | Chronos mucho más barato que MOMENT, pero MOMENT queda comparable a DL entrenado por dataset. | No es RUL | arXiv:2506.11250 | SOLO-SNIPPET |
| Stewart, Hodkiewicz & Li, "LLMs for Failure Mode Classification: An Investigation" | 2023 | GPT-3.5 ajustado: F1 0.80; clasificador convencional: 0.60; GPT-3.5 sin ajuste: 0.46. | Un conjunto de datos, un dominio | arXiv:2309.08181 | SOLO-SNIPPET |
| "Comparative Benchmark of LLMs for Labelling Wind Turbine Maintenance Logs" | 2025 | El desempeño depende de la ambigüedad semántica de la etiqueta. Hay más acuerdo en componentes que en acciones. Ningún modelo es perfecto y la calibración varía mucho, por lo que recomiendan humano en el lazo. | Un dominio (eólica) | arXiv:2509.06813 | SOLO-SNIPPET |
| Lin & Ompusunggu, asesor inteligente de mantenimiento prescriptivo con FMECA, grafo de conocimiento y ML (AI for Engineering 2(2)) | 2026 | Mejora la interpretabilidad y trazabilidad de diagnósticos en un caso de actuador lineal. | Un actuador; sin comparación frente a baseline fuerte | 10.1049/aie2.70019 | VERIFICADO-ABSTRACT |

### Gaps
- No hay benchmark verificado de Chronos, MOMENT o TimesFM en zero-shot para RUL en múltiples datasets bajo un mismo protocolo.
- No hay evidencia verificada de LLMs en producción generando recomendaciones de mantenimiento con resultado medido.

---

## 6. Física más datos (PINN, gemelos digitales)

### Takeaway
Hay casos puntuales prometedores, pero la validación en planta es escasa. Las barreras de adopción documentadas son organizacionales y de datos.

### Cited Findings
- Revisión "A Review on Physics-Informed Data-Driven RUL Prediction: Challenges and Opportunities" (MSSP, 2024). El snippet solo mostró título y metadatos. NO-VERIFICADO el contenido (resumen en aminer: https://resource.aminer.org/pub/659d1954939a5f408248c738/).
- Revisión PRISMA de 60 estudios sobre PINN para gemelos digitales estructurales y SHM (2026): problemas abiertos de balance de pérdidas, desajuste de modelo, UQ, escalabilidad y benchmarking. SOLO-SNIPPET (https://civilica.com/doc/2664442/).
- Restricciones físicas de baja fidelidad (monotonicidad) redujeron la incertidumbre en dos casos (Univ. of Florida, https://web.mae.ufl.edu/nkim/Papers/paper140.pdf). SOLO-SNIPPET.
- Ramirez et al. 2026: B-PINN con mejor calibración en envejecimiento de aislamiento; validado con modelo de elementos finitos y mediciones de campo de una planta solar (10.1002/aisy.202501502, VERIFICADO-ABSTRACT).
- Zhan, Hwang & Krishnankutty (Sustainable Development 33(2), 2024): en entrevistas a empresas de energía y químicos de Singapur, las barreras más citadas para el gemelo digital fueron falta de casos de éxito (78.6 %), alta inversión (71.4 %) y falta de técnicas efectivas de análisis de datos (64.3 %). Es un estudio por entrevistas (n no extraído). 10.1002/sd.3270, VERIFICADO-ABSTRACT.
- Un blog comercial (Ombrulla) afirma que C-MAPSS y PRONOSTIA son limpios y de un solo activo. Fuente comercial; no usar como evidencia.

### Gaps
- Sin comparación verificada de PINN frente a baselines fuertes no físicos en datos reales con el mismo protocolo.

---

## 7. Evidencia de ROI, despliegue y causas de fracaso

### Takeaway
No encontré fuente primaria verificada de ROI. Las cifras comunes (30–50 % menos paradas, "10x ROI") circulan en blogs y rastrean a informes antiguos, y no pude abrir los informes originales. Las causas de fracaso documentadas en fuentes arbitradas son datos de falla insuficientes, habilidades y dependencia del proveedor.

### Cited Findings
- Escasez de fallas y política de mantenimiento como inhibidor del ML (Akkermans et al. 2024, 10.1002/joom.1295, VERIFICADO-ABSTRACT).
- Falta de habilidades técnicas para implementar PdM y dependencia de soluciones OEM-específicas, según la introducción de Ujakpa et al. (Modelling Simul. Eng. 2026, 10.1155/mse/7556183, VERIFICADO-ABSTRACT; la introducción cita a Nunes et al. y Paolanti et al., que no abrí). Su accuracy del 94.0 % y AUC 0.9960 provienen de un modelo de clasificación en un solo estudio y no son evidencia de ROI.
- Barreras de adopción de gemelo digital: falta de casos exitosos, inversión y datos (Zhan et al. 2024, 10.1002/sd.3270).
- Retos de despliegue de ML (survey de casos de estudio), arXiv:2011.09926 (2020), SOLO-SNIPPET.
- Cifras de ROI (secundarias y NO-VERIFICADO): "5–10 % menos costos de mantenimiento y 10–20 % más uptime" atribuidas a Deloitte; "30–50 % menos paradas" atribuida a McKinsey 2017; un 10 % de falsos positivos habría anulado los ahorros en un programa. Fuente: https://reliamag.com/maintenance-and-reliability/predictive-maintenance-roi-benchmarks-what-the-studies-show/ (blog de revista, no primaria). Una encuesta de adopción "30 % en 2024 a 27 % en 2025" tiene publicador no identificado: descartar.

### Gaps
- No hay estudio con fuente primaria que mida ROI de PdM con ML en producción, ni tasa de fracaso de proyectos con metodología explícita.
- Los informes originales de McKinsey y Deloitte no fueron abiertos.

---

## 8. MLOps en PdM

### Takeaway
La evidencia sobre MLOps específica de PdM es débil. Lo que hay es general sobre concept drift.

### Cited Findings
- Concept drift: cambia la relación entre features y etiquetas entre entrenamiento y producción; hay que detectarlo y reentrenar (arXiv:2410.09190, SOLO-SNIPPET).
- En datos operativos el drift es inevitable (TU Delft, AIOps, SOLO-SNIPPET: https://research.tudelft.nl/en/publications/maintaining-and-monitoring-aiops-models-against-concept-drift).
- Guía de proveedor (baja calidad): una alerta de drift puede ser falla de pipeline, cambio de esquema, retraso de etiquetado o instrumentación, no drift real; no liberar un modelo reentrenado solo por mejor promedio. Fuente: https://smartdev.com/de/ai-model-drift-retraining-a-guide-for-ml-system-maintenance/. Marketing; solo como heurística.
- Deploy: Feisa et al. 2025 documenta el distribution shift por envejecimiento del equipo (10.1002/eng2.70494, VERIFICADO-ABSTRACT y pasaje).

### Gaps
- Sin caso de estudio verificado de MLOps en una flota industrial, ni sobre deriva de sensores o etiquetas con retraso (el fallo se confirma tarde).

---

## Tabla: error metodológico → cómo invalida → cómo prevenirlo

| Error | Cómo invalida los resultados | Prevención | Fuente | Estado |
|---|---|---|---|---|
| Ventanas o segmentos de la misma grabación en train y test (CWRU) | El modelo memoriza la firma de cada señal; la precisión es optimista | Separar por archivo, o mejor por rodamiento físico, antes de ventanear | arXiv:2407.14625; arXiv:2509.22267; 10.1155/stc/8787490 | SOLO-SNIPPET / VERIFICADO-ABSTRACT |
| Preprocesamiento y protocolo de evaluación distintos entre papers (C-MAPSS) | Las diferencias entre modelos pueden ser del preprocesamiento, no de la arquitectura | Reportar subset, truncado de RUL, ventana y punto de evaluación; control de fuga; grilla factorial | engrXiv 8145 | SOLO-SNIPPET |
| Usar una sola métrica asimétrica exponencial | Un outlier domina; no mide calibración | Reportar RMSE/MAE, score y errores temprano/tardío | arXiv:2202.10916 | SOLO-SNIPPET |
| Point-adjust en anomalías | Un predictor aleatorio obtiene F1 alto | Métricas por evento/rango; baselines triviales | arXiv:2405.11238 | SOLO-SNIPPET |
| Benchmarks de anomalías con defectos | Ilusión de progreso | Usar archivos curados (UCR) e incluir baselines simples | arXiv:2009.13807 | SOLO-SNIPPET |
| Validar solo en datos de laboratorio limpios | No refleja corrupción ni faltantes reales | Pruebas de robustez con datos corruptos | 10.1002/cpe.70654 | VERIFICADO-ABSTRACT |
| Conformal estándar con datos dependientes | Cobertura nominal no garantizada | Verificar cobertura empírica por activo; métodos que relajan intercambiabilidad | 10.1002/qre.70453 | VERIFICADO-ABSTRACT |
| Ignorar la censura | Se sesga la distribución de vida | Modelos de supervivencia | arXiv:2504.14744; SurvLoss | SOLO-SNIPPET |
| Pocas fallas para entrenar | Sobreajuste e intervalos no fiables | Evaluar el "punto dulce" de datos de falla antes de invertir | 10.1002/joom.1295 | VERIFICADO-ABSTRACT |
| Evaluación offline sin contemplar shift | Degradación en producción | Monitoreo de drift y evaluación en línea | 10.1002/eng2.70494; arXiv:2410.09190 | VERIFICADO-ABSTRACT / SOLO-SNIPPET |

## Tabla de métricas

| Métrica | Uso | Advertencia | Estado |
|---|---|---|---|
| RMSE / MAE | Error de RUL | Trata igual temprano y tardío | SOLO-SNIPPET |
| Score NASA (PHM08) | Penaliza más lo tardío | Exponencial, sin normalizar, sensible a outliers | SOLO-SNIPPET |
| Alpha-lambda, horizonte de predicción | Evaluación de pronóstico a lo largo del tiempo | Definiciones no recuperadas | NO-VERIFICADO |
| F1 con point-adjust | Anomalías | Infla resultados | SOLO-SNIPPET |
| ROC-AUC, F1, accuracy | Clasificación | Poco informativas con desbalance si se usan solas | VERIFICADO-ABSTRACT (uso en 10.1155/stc/8787490) |
| Cobertura de intervalos | Incertidumbre | Verificar empíricamente | VERIFICADO-ABSTRACT |

---

## Recomendación (SÍNTESIS PROPIA, no es hallazgo de una fuente): protocolo mínimo de validación para el agente

Antes de recomendar un modelo, el agente debería exigir:
1. Unidad de partición: activo o rodamiento completo; nunca ventanas aleatorias. Preprocesamiento ajustado solo con train.
2. Validación temporal hacia adelante, con holdout de activos nunca vistos.
3. Baselines obligatorios: umbral simple, tendencia, supervivencia clásica (Weibull/Cox), y un modelo de bosque aleatorio. Un DL que no los supere no se recomienda.
4. Reporte de varias métricas, con subset, truncado de RUL y punto de evaluación, y distribución de errores temprano/tardío.
5. Censura tratada explícitamente cuando hay equipos que no han fallado.
6. Incertidumbre con cobertura empírica medida por activo; no aceptar intervalos sin calibración.
7. Anomalías: métricas por evento, tasa de falsas alarmas por activo-mes y costo asociado.
8. Cantidad mínima de fallas observadas por modo de falla; si no se alcanza, tratar como hipótesis y no como predicción accionable.
9. Prueba de robustez con faltantes y ruido; plan de monitoreo de drift y criterio de reentrenamiento con aprobación humana.
10. Sin evidencia de ROI en producción: pilotaje en sombra y comparación contra la práctica actual antes de actuar.

## Brechas de evidencia (resumen)
1. Surveys principales de RESS/MSSP/TII no abiertos; no hay DOI verificado de ellos.
2. Resultados canónicos de FEMTO, XJTU-SY y N-CMAPSS, y definiciones alpha-lambda, sin verificar.
3. Isolation forest y autoencoders: sin comparación verificada.
4. RSF vs DeepSurv en PdM industrial: sin comparación directa verificada.
5. Zero-shot de modelos fundacionales para RUL: sin benchmark multi-dataset.
6. ROI y tasas de fracaso: sin fuente primaria; las cifras de McKinsey y Deloitte son de segunda mano.
7. MLOps específico de PdM: sin caso verificado.
8. Elicit inaccesible; WebFetch y curl bloqueados hacia arXiv, IEEE, ScienceDirect, MDPI y PHM Society. Si el caller tiene otro acceso, abrir primero: arXiv:2407.14625, 2509.22267, 2009.13807, 2202.10916, engrXiv 8145, y el paper de Saxena 2010.
