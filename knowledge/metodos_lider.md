# Métodos del líder: datos, priorización, estadística, causa raíz, FMECA, predictivo y economía

Secciones 3 a 9 del archivo del líder (`.claude/agents/reliability-engineer.md`), movidas aquí sin cambios para que el líder no las cargue en cada invocación. La numeración se conserva porque el líder, el checklist y `tools/reliability/README.md` citan estas secciones (por ejemplo, el árbol de decisión es la sección 5.1). El líder las lee cuando resuelve un caso simple por sí mismo, redacta un encargo técnico a un especialista o contrasta una entrega; los especialistas llevan su propio método en su archivo.

## 3. FASE 2–3 · DATOS Y ESTRUCTURA DEL ACTIVO

### 3.1 Auditoría de datos (obligatoria, antes de cualquier número)

1. **Inventario**: filas, columnas, rango de fechas, granularidad (evento, OT, aviso, lectura de sensor).
2. **Perfil por campo**: % nulos, valores únicos, formatos de fecha, unidades, outliers, duplicados.
3. **Reglas de limpieza documentadas** (cada regla con su conteo de filas afectadas): normalizar IDs de equipo, deduplicar, excluir trabajo no-falla (proyectos, modificaciones, calibraciones, inspecciones rutinarias), reconciliar husos horarios.
4. **Definir la unidad de tiempo correcta**: horas de operación/ciclos/toneladas/km — **no** días calendario salvo que sea lo único disponible (y entonces se declara).
5. **Definir el evento "falla"**: función perdida (falla funcional) vs. falla parcial vs. intervención preventiva. Mezclarlas corrompe todo el análisis.
6. **Censura**: identificar suspensiones (en operación al cierre de ventana, retiradas por otra causa). Un dataset sin censura casi nunca es honesto.
7. **Sesgos**: truncamiento por izquierda (equipos instalados antes de la ventana), subregistro de fallas menores, codificación inconsistente entre planta/turnos, texto libre vs. código.

Entregable de la fase: tabla "Calidad de datos" (campo · % faltante · tratamiento · impacto en el análisis).

### 3.2 Jerarquía y taxonomía

- Estructura **MECE** (planta → área → sistema → equipo → subsistema → componente → pieza mantenible) ligando OTs al nivel correcto.
- Taxonomía de falla (modo, mecanismo, causa) **validada contra ISO 14224** u OREDA cuando el componente esté en su alcance; para otros dominios, el estándar sectorial (IEEE eléctrico, DNV/ABS naval, API, etc.). Si la norma no cubre el componente exacto, **dilo** — no fuerces equivalencias.
- Distingue siempre: **modo de falla** (cómo se manifiesta) ≠ **mecanismo** (proceso físico) ≠ **causa raíz** (por qué ocurrió el mecanismo).

---

## 4. FASE 4 · PRIORIZACIÓN (CRITICIDAD Y BAD ACTORS)

### 4.1 Bad actors (alta frecuencia/costo/downtime)
- Agrega por **activo mantenible**, no por OT.
- Produce **tres Paretos** (costo, frecuencia, downtime) y **reconcílialos** (cruza las listas; un activo alto en varias vistas es bad actor real).
- Separa **crónico** (recurrencia con mismo código/patrón) de **evento único costoso**.
- Resultado: lista corta con hipótesis de partida y orden recomendado de RCA. **Prioriza; no declares causas raíz aquí.**

### 4.2 Criticidad
- Matriz de consecuencia × probabilidad con **criterios escritos y calibrados** (seguridad, ambiente, producción, costo, calidad). Escalamiento transparente, no "colores por intuición".
- La probabilidad se alimenta con datos reales (frecuencia observada) cuando existen; la consecuencia suele ser juicio de ingeniería → **etiquétala [JUICIO]** y valídala con operaciones/mantenimiento (la IA no puede juzgar consecuencias que no están en los datos).
- Sensibilidad: ¿cambia el ranking si se mueve un criterio un nivel? Reporta la estabilidad del ranking.

---

## 5. FASE 5 · ESTADÍSTICA DE FALLAS (el núcleo cuantitativo)

### 5.1 Árbol de decisión del método (decide ANTES de ajustar)

```
¿El ítem es REPARABLE o NO reparable?
├─ NO reparable (rodamiento, sello, filtro, tela, cable… hasta que se reemplaza)
│    → modelo de tiempo-hasta-falla (TTF): Weibull / lognormal / exponencial,
│      Kaplan-Meier (no paramétrico), con CENSURA por derecha.
│      Si hay covariables → Cox PH o AFT.
└─ REPARABLE (la unidad se repara y vuelve a operar)
     → NO ajustes Weibull a los TBF como si fueran iid sin probar tendencia.
       1) Prueba de tendencia (Laplace / MIL-HDBK-189) y gráfico MCF (media acumulada de fallas).
       2) Sin tendencia (HPP): tasa λ constante, intervalos ~ exponencial; MTBF válido.
       3) Con tendencia: NHPP (Crow-AMSAA / power-law); reporta β_CA y su significado
          (β_CA<1 mejora, ≈1 estable, >1 deterioro) y ROCOF.
VARIAS unidades reparables con fin de observación T_k distinto (flota)
     → NO concatenes sus tiempos en una serie: analízalas como sistemas múltiples. MCF multiunidad
       (con IC) + Crow-AMSAA condicional (tasa propia por unidad, β común; u=t/T_k) y Laplace agrupada;
       contrasta con λ común solo si no hay heterogeneidad. Reporta unidades sin eventos, eventos duplicados
       (varios en el mismo instante: conserva y haz sensibilidad) y la sensibilidad a la ventana final
       (si la conclusión depende de la cola con pocas unidades en riesgo, es frágil: dilo).
¿Hay modos de falla mezclados? → SEPARA por modo (competing risks); un Weibull "mixto"
  con curva quebrada suele indicar poblaciones mezcladas, no un β intermedio.
```

### 5.2 Weibull (IEC 61649) — procedimiento
1. Datos: tiempos a falla + suspensiones, en la unidad correcta (sec. 3.1.4).
2. Estimación: **MLE** (preferida con censura y n moderado) y/o regresión por rangos (MRR, con mediana de rangos de Bernard/ajuste Johnson para censura) como contraste; reporta el método. Con n muy pequeño, MLE sesga β: aplica corrección de sesgo o declara el sesgo.
3. **Incertidumbre obligatoria**: intervalos por razón de verosimilitud o bootstrap (no solo el valor puntual). Reporta n de fallas y n de suspensiones.
4. **Bondad de ajuste**: gráfico de probabilidad Weibull (WW-plot), coeficiente de correlación del gráfico, Anderson-Darling o equivalente; compara con lognormal/exponencial. Si ajusta mal, no lo uses: diagnostica (poblaciones mezcladas, tiempo de arranque γ ≠ 0 → Weibull de 3 parámetros solo con respaldo físico).
5. **Interpretación (no solo el número)**:
   - β < 1: mortalidad infantil → corregir instalación/puesta en marcha/calidad, **no** fijar intervalo de reemplazo.
   - β ≈ 1: aleatoria → PM por edad es desperdicio; ir a on-condition o run-to-failure si las consecuencias lo permiten.
   - β > 1: desgaste → una tarea basada en edad **puede** ser válida; calcula B10/B50 y reemplazo óptimo (sec. 9.2).
   - **MTBF ≠ vida útil**: es una tasa, no una edad segura de reemplazo. Rechaza planes que lo usen como vida garantizada.
6. Reporta B10, B50, η, MTTF **con intervalos**, nunca solo puntos.

### 5.3 Crow-AMSAA / NHPP (IEC 61164)
Para reparables con tendencia: estima λ y β por MLE sobre tiempos acumulados, prueba de bondad (Cramér-von Mises), intervalos, gráfico log-log de fallas acumuladas vs. tiempo (pendiente = β), proyección de ROCOF **con su incertidumbre** y declarando los supuestos (misma configuración, mismo régimen de uso).

### 5.4 Supervivencia no paramétrica y regresión
- **Kaplan-Meier** con IC y prueba log-rank para comparar grupos (flotas, proveedores, turnos).
- **Cox PH**: verifica **proporcionalidad de riesgos** (residuos de Schoenfeld); declara si el modelo es **exploratorio** (pocas covariables o eventos; regla práctica de ≥10 eventos por covariable, tratada como orientación y no como ley).
- Covariables tiempo-dependientes cuando el régimen de carga cambia.

### 5.5 Conciliación de modelos contradictorios
Si Weibull y Crow-AMSAA parecen discrepar, **explica por qué** (uno mide la forma de la distribución de vida entre reparaciones; el otro la tendencia del proceso de reparaciones en el tiempo). Nunca elijas uno en silencio ni ocultes la discrepancia.

### 5.6 Sistemas (RBD, FTA cuantitativo, redundancia)
Series/paralelo/k-de-n, disponibilidad de sistemas con reparación, dependencias de causa común. No entregues cálculos "caja negra": muestra el diagrama, las fórmulas y los supuestos de independencia.

### 5.7 Rigor inferencial
- Elige la prueba por supuestos verificados (normalidad, homocedasticidad, independencia); con datos de falla suele convenir no paramétrica (Mann-Whitney U, Wilcoxon, bootstrap).
- Reporta **tamaño de efecto** y IC además del p-valor; corrige comparaciones múltiples (Holm-Bonferroni o FDR).
- Define la significancia **antes** de mirar los datos. No hagas p-hacking ni elijas la ventana temporal a posteriori.
- Reproducibilidad: semilla fija, versión de librerías, script guardado junto al resultado.

### 5.8 Gráficos estadísticos (matplotlib, 600 dpi, paleta sobria)
Un solo color de acento reservado al elemento más crítico + una familia monocromática; fondo blanco; ejes rotulados con unidades; **cada figura con n, fuente de datos y método en el pie**. Catálogo según datos disponibles (no fuerces una figura sin datos suficientes; declara el vacío): WW-plot con bandas, h(t), PDF con B10/B50/moda/MTTF, MCF/Crow-AMSAA, Kaplan-Meier, Cox (forest plot), Pareto, matriz de riesgo, Ishikawa, curva P-F (conceptual si no hay datos de condición), RUL por Monte Carlo.

---

## 6. FASE 5 · ANÁLISIS DE CAUSA RAÍZ (ACR/RCA) Y ANÁLISIS DE FALLA

### 6.1 Principios
- La **evidencia precede a la hipótesis**: preservar evidencia física, tomar fotos/medidas, cadena de custodia, entrevistas, registros de proceso/SCADA, historial de OTs, condiciones de operación previas al evento.
- Una causa se clasifica por su **nivel de evidencia**: **Confirmada** (prueba directa), **Probable** (evidencia indirecta convergente), **Posible** (compatible, sin evidencia), **Descartada** (con la prueba que la descarta). Nunca presentes una "Posible" como "Confirmada".
- Se llega a la **causa latente/organizacional** (sistemas, procedimientos, decisiones), no se detiene en el error humano ni en el componente. Clasificación PROACT: causas **físicas → humanas → latentes**.

### 6.2 Procedimiento (IEC 62740 + PROACT®)
1. Definir el evento y su costo/consecuencia (cuantificada solo con datos reales).
2. Línea de tiempo con fuentes (qué pasó, cuándo, quién lo registró).
3. **FTA (IEC 61025)** con puertas explícitas. Si los datos no permiten sustentar lógica AND sin especular, el árbol se limita a OR y **se declara**. Cada rama trazada a evidencia (texto de eventos, ensayo, cita). Construirlo como **tabla nativa editable**, no imagen.
4. Cruzar con Ishikawa 6M (causas trazables a texto real) y 5-Why **solo** como herramienta de profundización, no como sustituto de evidencia.
5. **Mecanismo físico verificado para ESE activo**: Archard (desgaste), Hertz (contacto), Paris-Erdogan (propagación de grieta), Arrhenius (térmico), Goodman/Soderberg (fatiga), Miner (daño acumulado)… solo si el mecanismo dominante del activo es realmente ese; confírmalo en literatura antes de aplicarlo.
6. **Ensayos y verificación**: lista de NDT/ensayos pertinentes con la norma específica (ISO/ASTM/EN) verificada contra su publicador; análisis metalográfico/fractográfico cuando aplique.
7. **Plan de acción CAPA** (correctiva y preventiva): responsable, fecha, indicador de verificación de eficacia, y **cómo se sabrá que la causa quedó eliminada**.

### 6.3 Pruebas de calidad del ACR
- ¿Cada causa raíz declarada tiene evidencia asociada? ¿Hay alternativas descartadas explícitamente?
- ¿Se distinguió causa inmediata, contribuyente y raíz?
- ¿Las acciones atacan la causa (no solo el síntoma)? ¿Se definió métrica de eficacia?

---

## 7. FASE 5–7 · FMEA/FMECA, RCM Y ESTRATEGIA

### 7.1 Funciones y fallas funcionales (antes del FMEA)
Define cada función con **estándar de desempeño cuantificado** ("bombear X m³/h a Y bar", no "bombear"), luego fallas funcionales (total/parcial), luego modos de falla. Sin esto el FMEA es una lista de componentes.

### 7.2 FMEA/FMECA (IEC 60812; MIL-STD-1629A como referencia histórica)
Proceso: función → falla funcional → modo → mecanismo/causa → **efecto local/siguiente nivel/final** → detección actual → severidad, ocurrencia, detección (escalas **definidas y escritas**) → criticidad/RPN → acción. Reglas: la **severidad manda** (RPN alto con severidad baja ≠ riesgo alto; considera criticidad por severidad×ocurrencia o AP/IEC); ocurrencia calibrada con **frecuencia observada** cuando existe; si se usa el formato de 4 hojas del usuario/cliente, ese formato real **gana** sobre cualquier plantilla propia.

### 7.3 RCM y selección de tareas (SAE JA1011 / lógica de decisión)
Por cada modo de falla y según su consecuencia (oculta, seguridad/ambiente, operacional, no operacional), recorre la lógica: ¿on-condition técnicamente factible y valiosa? → ¿restauración/reemplazo programado (solo si hay desgaste, β>1, y edad identificable)? → ¿búsqueda de fallas (funciones ocultas)? → ¿rediseño? → ¿run-to-failure (solo si consecuencias lo toleran)? Cada tarea con **factibilidad técnica** y **justificación de costo-efectividad**.

### 7.4 Intervalos
- **P-F**: el intervalo de inspección ≈ una fracción del intervalo P-F (regla práctica: la mitad o menos) **solo si el P-F está respaldado por datos o evidencia**; si es conceptual, rotúlalo así. Define umbrales de alerta con base física.
- **PM**: desafía PM calendarias sin fundamento ("fake PM"): contrasta con los datos de OTs (¿la tarea previene falla o genera falla por intervención? ¿mortalidad infantil post-PM?).
- **Edad de reemplazo**: solo con β>1 y razón de costos favorable (sec. 9.2).

### 7.5 Otros
Paradas de planta/shutdown: alcance basado en riesgo con justificación de diferimiento; planes de trabajo (PMI/SOP/paquetes) con pasos verificables.

---

## 8. FASE 5 · CIENCIA DE DATOS PARA MANTENIMIENTO PREDICTIVO

### 8.1 Antes de modelar
1. **¿Se necesita ML?** Si un umbral de ingeniería, una carta de control o un Weibull resuelven el problema, **empieza por ahí** y úsalo como *baseline* contra el que el ML debe ganar con evidencia.
2. **Definir el objetivo**: clasificación de falla en horizonte H, regresión de RUL, detección de anomalías, clasificación de condición. El horizonte y el costo de errores se definen con el negocio.
3. **Etiquetado**: define "falla" y la ventana de predicción sin mirar el futuro; en RUL, trata la censura (unidades que no han fallado) — no las trates como RUL=0 ni las descartes sin analizar el sesgo.
4. **Ingeniería de variables** con significado físico (RMS, curtosis, factor de cresta, bandas de frecuencia, tendencias en ventana, tiempo desde último evento, carga acumulada). Evita variables que filtren el futuro.

### 8.2 Validación (donde fallan la mayoría de proyectos)
Evita los errores fatales:
1. **Fuga de datos (leakage)**: variables calculadas con información posterior al evento, normalización ajustada con todo el dataset, etiquetas derivadas de las mismas columnas.
2. **Partición aleatoria en series temporales**: usa **división por fecha / out-of-time (OOT)** y validación con ventana expansiva (*walk-forward*). Para flotas, particiona también **por activo** para evaluar generalización a unidades no vistas.
3. **Desbalance extremo**: no uses accuracy. Reporta PR-AUC, recall/precisión **por clase**, matriz de confusión y la curva precisión-recall; el umbral se elige con **costo de FN vs. FP** reales (o se declara [VACÍO]).
4. **Calibración** de probabilidades (curva de calibración, Brier) antes de usarlas para decidir.
5. **Comparación contra baseline** y contra el estado actual (¿cuántas fallas habría detectado con antelación útil? ¿cuántas falsas alarmas por mes?).
6. **Incertidumbre**: intervalos de predicción (cuantiles, conformal, ensambles); un RUL es una **distribución**, no un número.
7. **Estabilidad**: repetir con varias semillas/particiones; reportar varianza.
8. **Interpretabilidad** (importancia por permutación, SHAP) como ayuda de diagnóstico, nunca como prueba causal.

### 8.3 Modelos recomendados por contexto
Tabular + pocos datos: regresión logística / Cox / random forest / gradient boosting (XGBoost, LightGBM). Series de sensores densas: 1D-CNN, LSTM/GRU/TCN, autoencoders para anomalías; deep learning **solo** si hay volumen y el baseline simple no basta. Tamaño de muestra insuficiente → modelo simple, y se rotula **exploratorio/prototipo**.

### 8.4 Despliegue y operación
Monitoreo de *drift* de datos y de desempeño, reentrenamiento con criterios, registro de versiones (registro de experimentos o equivalente), plan de intervención humano-en-el-lazo, y definición de **qué acción dispara cada alerta** (una alerta sin acción asociada no genera valor).

### 8.5 Visión por computadora (inspección de desgaste, corrosión, fugas, alineamiento, roturas)
- Protocolo de captura (iluminación, ángulo, distancia, resolución) y de **anotación** con guía escrita y acuerdo entre anotadores (κ).
- **Partición por activo/sesión/fecha, nunca por fotograma** (los cuadros consecutivos son casi idénticos: partir por cuadro infla métricas).
- Métricas por clase (mAP50, mAP50-95, P, R, F1); en clases críticas (ej. rotura) **priorizar recall** y analizar los falsos negativos uno por uno.
- Probar bajo variación real (luz, suciedad, velocidad); conservar un conjunto de prueba de campo nunca usado en el desarrollo.
- Si hay una plataforma de visión por computadora conectada, úsala para gestión de datasets, entrenamiento y evaluación; no subas imágenes de terceros sin confirmación.

### 8.6 Búsqueda semántica en históricos
Para consultas tipo "¿hemos visto esta falla antes?": chunking que preserve contexto del ACR (equipo, fecha, causa), embeddings, recuperación + reordenamiento, y **respuestas siempre con cita al documento fuente**; si no hay recuperación suficiente, responder "no encontrado" en vez de inferir.

---

## 9. FASE 7 · ECONOMÍA, REPUESTOS Y KPIs

### 9.1 LCC (costo de ciclo de vida)
Estructura: CAPEX, OPEX, costos de falla (reparación + lucro cesante + consecuencias), mantenimiento, fin de vida. Descuenta a VPN con tasa **declarada** y calcula CAE/EAC para comparar vidas distintas. **Análisis de sensibilidad** sobre las 2–3 variables más inciertas. Si falta el costo de falla/reemplazo → [VACÍO] y entregas la **estructura del cálculo con celdas pendientes**, no un número supuesto.

### 9.2 Reemplazo óptimo
Política por edad (Barlow-Proschan): solo tiene mínimo interior de costo cuando la tasa de riesgo crece (β>1) y el costo de falla supera al preventivo. Si β≤1 o los costos no están, **no hay edad óptima calculable** y se dice.

### 9.3 Repuestos
Criticidad × tiempo de reposición × demanda observada. Para demanda intermitente usa modelos adecuados (Poisson/Croston/bootstrap) y un nivel de servicio explícito; decisiones de rotables y de repuestos críticos justificadas por consecuencia, no por costumbre.

### 9.4 KPIs ligados a decisiones
Para cada KPI: **definición formal (fórmula), fuente, frecuencia, dueño, umbral y decisión que dispara**. Ejemplos: MTBF, MTTR, disponibilidad (inherente/lograda/operacional), confiabilidad R(t), OEE, % trabajo planificado, cumplimiento de PM, backlog en semanas, repetibilidad de fallas, costo de mantenimiento por unidad producida (EN 15341 como referencia de indicadores). Sin KPI vanidoso: si no cambia una decisión, no entra.
**Tableros de BI**: modelo en estrella (dimensión Activo/Tiempo/Código de falla; hechos OT/evento), medidas explícitas y documentadas, manejo de contexto de filtro, y notas de calidad de datos visibles en el tablero.

---
