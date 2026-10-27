# Referencia: ML Visual Lab v2 (modelos para mantenimiento predictivo)

Fuente: reliabilit_ia_ml_visual_lab_v2_ampliado.html (Reliabilit-IA · ML Visual Lab v2). Registro: **material aportado por la persona**, pedagógico; no es evidencia científica. Los puntajes (0 a 5) son criterios pedagógicos del archivo, no resultados medidos. Los datos estructurados están en historial/dossiers/chumacera_polea_faja/ml_lab.json.

Total: 29 modelos (15 en la Sesión 1, 14 en la Sesión 2).

## Sesión 1 · Clasificación de Fallas (15 modelos)

Flujo del archivo: Datos de sensores → EDA → Feature engineering → Split por tiempo/equipo → Balanceo → Entrenamiento → Validación → Métricas → Despliegue.

| Modelo | Qué hace | Cuándo usarlo | Datos | Métrica a vigilar | Evitar si | Familia | Interp / No lineal / Veloc / Pocos datos |
|---|---|---|---|---|---|---|---|
| Regresión Logística | Baseline probabilístico e interpretable | Buena primera opción cuando necesitas explicar el efecto de cada variable y obtener probabilidades calibrables. | Datos: Escalados ayudan; Fallas: Etiquetas necesarias; Complejidad: Baja; Salida: Probabilidad | Precision, Recall de falla, F1, PR-AUC, ROC-AUC, calibración. | Evítala como modelo único si la relación entre variables y falla es fuertemente no lineal y no haces ingeniería de características. | Supervisado / Tabular / Interpretable | 5/1/5/4 |
| LDA / QDA | Fronteras basadas en distribuciones | Útiles cuando las clases tienen estructuras aproximadamente gaussianas; LDA comparte covarianza y QDA permite una por clase. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Baja-media; Salida: Clase/probabilidad | Recall, F1, PR-AUC y matriz de confusión por modo de falla. | Pierden robustez con supuestos distributivos muy incumplidos o demasiadas variables respecto al número de muestras. | Supervisado / Estadístico / Interpretable | 4/2/5/4 |
| Naive Bayes | Probabilidades con independencia condicional | Buen baseline cuando hay muchas variables y necesitas entrenamiento/inferencia muy rápidos. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Muy baja; Salida: Probabilidad | Recall, Precision, F1 y calibración de probabilidades. | Puede degradarse si las variables están fuertemente correlacionadas y el supuesto de independencia es pobre. | Supervisado / Probabilístico / Muy rápido | 4/1/5/4 |
| K-Nearest Neighbors | Predicción por vecinos similares | Didáctico y útil cuando equipos con estados similares tienden a compartir el mismo modo de falla. | Datos: Escalado crítico; Fallas: Etiquetas necesarias; Complejidad: Inferencia alta; Salida: Voto | Recall, F1 y análisis del desempeño por K. | Sufre en alta dimensionalidad, grandes volúmenes y variables sin escalar. | Supervisado / Distancias / No paramétrico | 4/3/2/4 |
| Árbol de Decisión | Reglas if/else fáciles de explicar | Excelente para talleres y reglas operacionales; permite explicar umbrales de temperatura, vibración o carga. | Datos: No exige escalado; Fallas: Etiquetas necesarias; Complejidad: Baja; Salida: Reglas | Recall, F1, PR-AUC y profundidad/complejidad del árbol. | Un solo árbol puede sobreajustar y ser inestable ante pequeños cambios del dataset. | Supervisado / Reglas / Interpretable | 5/3/5/4 |
| Random Forest | Muchos árboles votando | Muy buen modelo general para datos tabulares de mantenimiento, relaciones no lineales e interacciones. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Media; Salida: Voto/prob. | Recall, F1, PR-AUC, OOB score, importancia/permutación de variables. | Menos interpretable que un árbol; modelos muy grandes consumen memoria y pueden ocultar drift. | Supervisado / Bagging / Robusto | 3/4/3/4 |
| Extra Trees | Árboles aún más aleatorizados | Alternativa potente a Random Forest cuando quieres más aleatoriedad y entrenamiento rápido en datos tabulares. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Media; Salida: Ensamble | Recall, F1, PR-AUC e importancia por permutación. | Puede aumentar sesgo en algunos problemas y sigue siendo menos interpretable que modelos simples. | Supervisado / Ensamble / Muy aleatorio | 3/4/4/4 |
| SVM | Margen máximo; kernels opcionales | Útil con datasets medianos, fronteras complejas y muchas variables; kernel RBF puede capturar no linealidad. | Datos: Escalado crítico; Fallas: Etiquetas necesarias; Complejidad: Media-alta; Salida: Margen | Recall, F1, PR-AUC; si necesitas probabilidades, revisar calibración. | Puede ser costoso con datasets muy grandes y requiere escalado/ajuste cuidadoso de C y gamma. | Supervisado / Margen / Kernel | 2/4/2/4 |
| Gradient Boosting | Corrige errores secuencialmente | Muy competitivo en datos tabulares cuando las relaciones son no lineales y buscas alta capacidad predictiva. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Media; Salida: Score/prob. | PR-AUC, Recall, F1, curvas de aprendizaje y SHAP/permutación. | Puede sobreajustar sin regularización; requiere tuning más cuidadoso que modelos baseline. | Supervisado / Boosting / No lineal | 2/5/3/4 |
| XGBoost | Boosting regularizado y optimizado | Frecuentemente fuerte en mantenimiento tabular con variables heterogéneas, missing values controlados e interacciones. | Datos: Tabulares; Fallas: Etiquetas necesarias; Complejidad: Media-alta; Salida: Score/prob. | PR-AUC, Recall, F1, coste esperado y explicabilidad SHAP. | No asumas que siempre ganará: requiere tuning, validación temporal y control de leakage. | Supervisado / Boosting / Tabular | 2/5/3/4 |
| LightGBM | Boosting eficiente con árboles por hojas | Conveniente cuando hay muchas filas/variables y necesitas acelerar entrenamiento sin renunciar a alta capacidad. | Datos: Tabulares grandes; Fallas: Etiquetas necesarias; Complejidad: Media-alta; Salida: Score/prob. | PR-AUC, Recall, F1, coste y estabilidad entre folds temporales. | Con datasets pequeños puede sobreajustar si no controlas hojas, profundidad y min_data_in_leaf. | Supervisado / Boosting / Escalable | 2/5/5/2 |
| CatBoost | Boosting con categóricas bien manejadas | Interesante si mezclas variables numéricas con categóricas como familia de equipo, fabricante, turno o tipo de operación. | Datos: Numéricas+categóricas; Fallas: Etiquetas necesarias; Complejidad: Media-alta; Salida: Score/prob. | PR-AUC, Recall, F1, coste por falsa negativa y SHAP. | Puede ser excesivo si todas las variables son simples y un modelo más interpretable cumple el objetivo. | Supervisado / Boosting / Categóricas | 2/5/3/4 |
| Red Neuronal MLP | Capas densas para relaciones complejas | Puede ser útil con suficientes datos y relaciones complejas entre variables de condición. | Datos: Escalado importante; Fallas: Etiquetas necesarias; Complejidad: Alta; Salida: Probabilidades | PR-AUC, Recall, F1, calibración, curvas train/validation. | Con pocos datos tabulares suele ser más difícil de ajustar y explicar que ensembles de árboles. | Supervisado / Deep Learning / No lineal | 1/5/2/2 |
| CNN 1D | Patrones locales en señales de sensores | Adecuada para vibración, corriente o acústica cuando la forma local de la señal contiene firmas de falla. | Datos: Ventanas de señal; Fallas: Etiquetas necesarias; Complejidad: Alta; Salida: Clase | Recall por modo de falla, F1 macro, PR-AUC, matriz de confusión por equipo. | Necesita ventanas bien construidas, suficientes ejemplos y cuidado con leakage entre ventanas del mismo evento. | Supervisado / Series temporales / Deep Learning | 1/5/2/1 |
| LSTM / GRU | Dependencias temporales largas | Útil si la evolución temporal previa a la falla importa más que una fotografía instantánea del equipo. | Datos: Secuencias; Fallas: Etiquetas temporales; Complejidad: Alta; Salida: Clase/secuencia | Recall por evento, lead time, F1, PR-AUC y evaluación temporal. | Más costosa y sensible al diseño de ventanas; no siempre supera a features temporales + boosting. | Supervisado / Series temporales / Secuencial | 1/5/1/1 |

## Sesión 2 · Detección de Anomalías (14 modelos)

Flujo del archivo: Datos sanos/mistos → EDA → Escalado robusto → Modelo de normalidad → Anomaly score → Umbral → Consenso → Revisión experta.

| Modelo | Qué hace | Cuándo usarlo | Datos | Métrica a vigilar | Evitar si | Familia | Interp / No lineal / Veloc / Pocos datos |
|---|---|---|---|---|---|---|---|
| Z-Score / IQR / MAD | Reglas estadísticas univariadas | Excelente baseline para variables individuales con límites relativamente estables; MAD es más robusto a outliers. | Etiquetas: No requeridas; Escala: Univariada; Complejidad: Muy baja; Salida: Desviación | Tasa de alertas, precision/recall si hay eventos, alertas por hora y validación experta. | No detecta bien anomalías multivariadas ni interacciones complejas entre sensores. | No supervisado / Estadístico / Baseline | 5/1/5/5 |
| Distancia de Mahalanobis | Rareza multivariada con covarianza | Útil cuando sensores correlacionados forman una nube aproximadamente elíptica y una observación se aleja en conjunto. | Etiquetas: No requeridas; Escala: Global; Complejidad: Baja; Salida: Distancia | Distancia, percentil/umbral, tasa de alertas y validación con eventos. | Sensible a covarianza mal estimada, distribuciones no gaussianas y alta dimensionalidad con pocas muestras. | No supervisado / Multivariado / Estadístico | 4/1/5/4 |
| PCA · T² / SPE-Q | Subespacio normal + error residual | Clásico en monitoreo multivariado: T² detecta desviaciones dentro del subespacio y SPE/Q mide error fuera del subespacio. | Etiquetas: No requeridas; Escala: Global; Complejidad: Media; Salida: T² + SPE | T², SPE/Q, contribution plots y tasa de alertas por régimen. | Captura relaciones lineales; puede perder anomalías no lineales y requiere selección adecuada de componentes. | No supervisado / Alta dimensionalidad / Multivariado | 4/1/5/4 |
| K-Means + distancia | Rareza respecto al centroide | Práctico cuando existen regímenes operativos claros y quieres medir distancia al patrón típico de cada régimen. | Etiquetas: No requeridas; Escala: Por cluster; Complejidad: Baja; Salida: Distancia | Distancia al centroide, percentil por cluster y estabilidad de clusters. | Clusters esféricos y K fijo; sensible al escalado y a formas de cluster complejas. | No supervisado / Clustering / Regímenes | 4/2/5/4 |
| DBSCAN | Densidad + ruido sin fijar K | Útil para descubrir zonas densas de operación y marcar puntos aislados como ruido, incluso con clusters no esféricos. | Etiquetas: No requeridas; Escala: Local; Complejidad: Media; Salida: Cluster/ruido | Número de puntos ruido, estabilidad ante eps/min_samples y validación experta. | Un único eps puede fallar cuando las densidades cambian mucho y la dimensionalidad es alta. | No supervisado / Densidad / Ruido | 4/4/3/4 |
| HDBSCAN | Densidad variable y clusters persistentes | Más flexible que DBSCAN cuando los regímenes tienen densidades distintas y quieres puntuaciones de outlier. | Etiquetas: No requeridas; Escala: Local; Complejidad: Media; Salida: Cluster+score | Outlier score, estabilidad de clusters y alertas revisadas. | Más complejo de explicar y requiere revisar estabilidad/selección de clusters. | No supervisado / Densidad / Clusters variables | 3/5/3/4 |
| Isolation Forest | Aísla rarezas con cortes aleatorios | Muy buena opción general para anomalías en datos tabulares, especialmente con pocas fallas y relaciones complejas. | Etiquetas: No requeridas; Escala: Global; Complejidad: Media; Salida: Anomaly score | Anomaly score, precision/recall si hay fallas, alertas por día, lead time. | No modela explícitamente secuencia temporal; el threshold y contamination deben validarse con contexto operativo. | No supervisado / Árboles / Anomaly score | 3/4/5/5 |
| Local Outlier Factor | Densidad relativa frente a vecinos | Muy útil cuando una observación es extraña respecto a su vecindario aunque no sea extrema globalmente. | Etiquetas: No requeridas; Escala: Local; Complejidad: Media; Salida: LOF score | LOF score, precision/recall si hay etiquetas parciales y estabilidad por K. | Costoso en datasets grandes y sensible a escala/número de vecinos. | No supervisado / Densidad local / Outliers | 4/4/2/5 |
| One-Class SVM | Frontera alrededor de la normalidad | Adecuada cuando tienes principalmente datos sanos y quieres aprender una frontera flexible de operación normal. | Etiquetas: Normalidad suficiente; Escala: Global; Complejidad: Media-alta; Salida: Decision score | Decision function, tasa de alertas, precision/recall con eventos y sensibilidad al umbral. | Escala mal a grandes datasets y es sensible a nu/gamma y al escalado. | Semi/no supervisado / Kernel / Frontera | 2/5/2/4 |
| Elliptic Envelope / MCD | Covarianza robusta para nube elíptica | Interesante cuando la operación normal es aproximadamente gaussiana y quieres robustez frente a una fracción de outliers. | Etiquetas: No requeridas; Escala: Global; Complejidad: Baja; Salida: Distancia robusta | Distancia robusta, tasa de outliers y revisión por régimen. | No sirve bien para fronteras multimodales o altamente no lineales. | No supervisado / Robusto / Gaussiano | 4/1/4/4 |
| Autoencoder | Error de reconstrucción | Potente para aprender normalidad no lineal con muchas variables cuando dispones de bastante historial sano. | Etiquetas: No requeridas; Escala: Global; Complejidad: Alta; Salida: Error reconstrucción | Reconstruction error, threshold por validación, precision/recall, contribution por feature. | Requiere más datos/tuning; el error de reconstrucción no siempre es interpretable por sí solo. | No supervisado / Deep Learning / No lineal | 2/5/1/2 |
| Variational Autoencoder | Latente probabilístico + reconstrucción | Útil cuando quieres un espacio latente probabilístico y modelar incertidumbre además de reconstrucción. | Etiquetas: No requeridas; Escala: Global; Complejidad: Muy alta; Salida: Score probabilístico | Reconstruction loss, KL, anomaly score combinado y validación por eventos. | Más complejo de ajustar e interpretar que un autoencoder básico; no es primera opción para un baseline. | No supervisado / Deep Learning / Probabilístico | 1/5/1/1 |
| LSTM Autoencoder | Reconstrucción de secuencias | Adecuado cuando la anomalía depende del patrón temporal completo y tienes historial de secuencias normales. | Etiquetas: No requeridas; Escala: Secuencia; Complejidad: Muy alta; Salida: Error temporal | Error por ventana, lead time, recall por evento, alertas/hora y estabilidad temporal. | Ventanas, normalización, drift y costo de entrenamiento requieren mucha atención. | No supervisado / Series temporales / Deep Learning | 1/5/1/1 |
| Residual de Forecasting | Predicción esperada vs señal real | Muy intuitivo para mantenimiento: pronosticas el comportamiento normal y alertas cuando el residual supera un umbral. | Etiquetas: No imprescindibles; Escala: Temporal; Complejidad: Variable; Salida: Residual | Residual normalizado, cobertura, lead time, alertas por día y recall por evento. | Si el modelo de forecasting es pobre, confundirás error de pronóstico con anomalía. | Semi/no supervisado / Series temporales / Residual | 5/4/3/4 |

## Selector: «¿Qué modelo conviene explorar primero?»

Entradas (cuatro listas):

| Control | Opciones |
|---|---|
| Etiquetas de falla | No importa; Sí, tengo clases/etiquetas; Muy pocas fallas etiquetadas; No tengo etiquetas |
| Tipo de señal | Cualquiera; Variables tabulares; Serie temporal / sensores; Muchas variables |
| Prioridad | Equilibrada; Interpretabilidad; Capacidad no lineal; Entrenamiento simple |
| Patrón esperado | No lo sé; Anomalía global; Anomalía local; Regímenes operativos; Dependencia temporal |

Reglas:

- Se ignoran los controles en «any». Si todos están en «any», no se filtra nada.
- Los controles activos se combinan con Y lógico: el modelo debe cumplir todos.
- Etiquetas = «Sí, tengo clases/etiquetas»: solo pasan los modelos de la Sesión 1 (Clasificación de Fallas); en la Sesión 2 no pasa ninguno.
- Etiquetas = «Muy pocas fallas etiquetadas» o «No tengo etiquetas»: en la Sesión 2 pasan todos los modelos en este criterio; en la Sesión 1 no pasa ninguno, porque ningún modelo de clasificación declara esos valores.
- Tipo de señal, Prioridad y Patrón: el modelo pasa si su lista de ajuste contiene el valor elegido (tabular, timeseries, highdim, interpret, performance, fast, global, local, cluster, sequence).
- El filtro actúa sobre la sesión (pestaña) activa; hay además un buscador por nombre.
- Si ningún modelo cumple todo, el panel muestra: «No hay modelos que cumplan todos los filtros. Prueba flexibilizar una condición.»

Orden de las sugerencias: Entre los modelos compatibles se ordenan de mayor a menor por un puntaje del comparador y se muestran como máximo 5 con la etiqueta «Explora:». Clave de orden: Interpretabilidad usa el puntaje de interpretabilidad; Capacidad no lineal usa el puntaje no lineal; Entrenamiento simple usa velocidad; Equilibrada usa pocos datos.

Modelos que pasan cada valor de filtro por sesión (según las listas de ajuste del archivo):

### Sesión 1 · Clasificación de Fallas

| Valor del filtro | Modelos |
|---|---|
| Etiquetas de falla = yes | Regresión Logística, LDA / QDA, Naive Bayes, K-Nearest Neighbors, Árbol de Decisión, Random Forest, Extra Trees, SVM, Gradient Boosting, XGBoost, LightGBM, CatBoost, Red Neuronal MLP, CNN 1D, LSTM / GRU |
| Etiquetas de falla = few | ninguno |
| Etiquetas de falla = no | ninguno |
| Tipo de señal = tabular | Regresión Logística, LDA / QDA, Naive Bayes, K-Nearest Neighbors, Árbol de Decisión, Random Forest, Extra Trees, SVM, Gradient Boosting, XGBoost, LightGBM, CatBoost, Red Neuronal MLP |
| Tipo de señal = timeseries | CNN 1D, LSTM / GRU |
| Tipo de señal = highdim | SVM, XGBoost, LightGBM |
| Prioridad = interpret | Regresión Logística, LDA / QDA, Árbol de Decisión |
| Prioridad = performance | Random Forest, Extra Trees, Gradient Boosting, XGBoost, LightGBM, CatBoost, Red Neuronal MLP, CNN 1D, LSTM / GRU |
| Prioridad = fast | Regresión Logística, Naive Bayes, LightGBM |
| Patrón esperado = global | ninguno |
| Patrón esperado = local | ninguno |
| Patrón esperado = cluster | ninguno |
| Patrón esperado = sequence | CNN 1D, LSTM / GRU |

### Sesión 2 · Detección de Anomalías

| Valor del filtro | Modelos |
|---|---|
| Etiquetas de falla = yes | ninguno |
| Etiquetas de falla = few | Z-Score / IQR / MAD, Distancia de Mahalanobis, PCA · T² / SPE-Q, K-Means + distancia, DBSCAN, HDBSCAN, Isolation Forest, Local Outlier Factor, One-Class SVM, Elliptic Envelope / MCD, Autoencoder, Variational Autoencoder, LSTM Autoencoder, Residual de Forecasting |
| Etiquetas de falla = no | Z-Score / IQR / MAD, Distancia de Mahalanobis, PCA · T² / SPE-Q, K-Means + distancia, DBSCAN, HDBSCAN, Isolation Forest, Local Outlier Factor, One-Class SVM, Elliptic Envelope / MCD, Autoencoder, Variational Autoencoder, LSTM Autoencoder, Residual de Forecasting |
| Tipo de señal = tabular | Z-Score / IQR / MAD, Distancia de Mahalanobis, K-Means + distancia, DBSCAN, HDBSCAN, Isolation Forest, Local Outlier Factor, One-Class SVM, Elliptic Envelope / MCD, Autoencoder |
| Tipo de señal = timeseries | LSTM Autoencoder, Residual de Forecasting |
| Tipo de señal = highdim | PCA · T² / SPE-Q, Isolation Forest, One-Class SVM, Autoencoder, Variational Autoencoder |
| Prioridad = interpret | ninguno |
| Prioridad = performance | Autoencoder, Variational Autoencoder, LSTM Autoencoder |
| Prioridad = fast | Z-Score / IQR / MAD, Isolation Forest |
| Patrón esperado = global | Z-Score / IQR / MAD, Distancia de Mahalanobis, PCA · T² / SPE-Q, Isolation Forest, One-Class SVM, Elliptic Envelope / MCD |
| Patrón esperado = local | DBSCAN, HDBSCAN, Local Outlier Factor |
| Patrón esperado = cluster | K-Means + distancia, DBSCAN, HDBSCAN |
| Patrón esperado = sequence | LSTM Autoencoder, Residual de Forecasting |

Comparador rápido: Compara tres alternativas por criterios pedagógicos generales, no por accuracy inventada. Criterios: Interpret., No lineal, Velocidad, Pocos datos (escala 0 a 5).

## Advertencias de validación (nota al pie del archivo)

- Las visualizaciones no sustituyen validación con datos reales.
- Separar por tiempo/equipo.
- Evitar fuga de información.
- Controlar desbalance.
- Evaluar coste de falsos negativos.
- Revisar drift.
- Para anomalías, las métricas requieren etiquetas parciales, revisión experta o evaluación basada en eventos.

Otras advertencias dentro de los modelos:

- Las animaciones son conceptuales: sirven para comprender el comportamiento antes de pasar al entrenamiento real en Python.
- XGBoost: no asumir que siempre ganará; requiere tuning, validación temporal y control de leakage.
- CNN 1D: ventanas bien construidas y cuidado con leakage entre ventanas del mismo evento.
- LSTM / GRU: sensible al diseño de ventanas; no siempre supera a features temporales + boosting.
- Random Forest: modelos muy grandes consumen memoria y pueden ocultar drift.
- LSTM Autoencoder: ventanas, normalización, drift y costo de entrenamiento requieren mucha atención.
- Isolation Forest: threshold y contamination deben validarse con contexto operativo.
- Pie del comparador y métricas: sin cifras de accuracy; los puntajes son pedagógicos.
