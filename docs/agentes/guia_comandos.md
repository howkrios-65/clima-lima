# Guía de comandos y uso del equipo de confiabilidad

Esta guía explica cómo manejar el equipo de veinte agentes (un estratega y diecinueve especialistas) y empieza por lo que más se usa: los comandos que se escriben con una barra (`/...`). Todo lo que aquí se afirma sale de los archivos del repositorio: `.claude/commands/`, `.claude/agents/reliability-*.md`, `knowledge/protocolo_agentes.md`, `knowledge/protocolo_dossier_modo_falla.md`, `tools/reliability/README.md` y el caso real `historial/dossiers/chumacera_polea_faja/`. El mapa interactivo del equipo está en `docs/agentes/mapa_agentes.html`.

## 1. Los comandos (`/...`)

El proyecto define dos comandos. Los dos arrancan al mismo estratega (`reliability-engineer`); lo que cambia es el tipo de trabajo que se le encarga.

| Comando | Para qué sirve | Qué escribes después | Qué obtienes |
|---|---|---|---|
| `/modo-de-falla` | Investigar a nivel mundial un modo de falla de un componente y armar el dossier con evidencia | El componente y su modo de falla | Un dossier con sus secciones, cada elemento con su fuente o declarado VACÍO, y un informe HTML verificado |
| `/confiabilidad` | Atender cualquier solicitud de confiabilidad con el equipo completo | El activo, la falla, los datos o el análisis que necesitas | Preguntas de intake, trabajo repartido entre especialistas y un informe verificado |

### 1.1 `/modo-de-falla`

**Sintaxis**

```
/modo-de-falla <componente y modo de falla>
```

**Ejemplo real (el caso ya trabajado en este repositorio)**

```
/modo-de-falla chumacera de polea de faja transportadora
```

**Cómo pedir un modo de falla nuevo.** Escribe el componente y, si lo conoces, el modo de falla, en una sola frase. No hace falta aportar datos de planta. Ejemplos de redacción:

```
/modo-de-falla rodamiento del motor de una bomba centrífuga, falla por fatiga
/modo-de-falla sello mecánico de una bomba de pulpa, fuga por desgaste
/modo-de-falla rodillo de carga de faja transportadora, atascamiento
```

Estos tres ejemplos son solo formas de redactar el encargo; el equipo investigará desde cero cada uno y no reutilizará cifras de otro caso.

**Qué hace el comando**, según su archivo `.claude/commands/modo-de-falla.md`:

1. Usa al agente `reliability-engineer` como estratega.
2. Sigue el protocolo `knowledge/protocolo_dossier_modo_falla.md`.
3. Aplica estas reglas: nada sin fuente; los datos ilustrativos no cuentan; los cálculos los hace el kit; un investigador por frente, en paralelo, respetando la cuota del conector de artículos; el dossier se valida con `validar_dossier`; verificación independiente antes de entregar; preguntas finales a la persona.

**Secciones del dossier** (catálogo del protocolo): mediciones y curvas; diagnóstico y troubleshooting; fenómenos físicos; vida útil y obsolescencia; top de fallas; FMECA y RCM; causa raíz; confiabilidad (Weibull y vida); punto óptimo; costo-riesgo y LCC; inspección basada en riesgo; mantenimiento predictivo y normas; modelos de aprendizaje automático y profundo; referencias.

### 1.2 `/confiabilidad`

**Sintaxis**

```
/confiabilidad <lo que necesitas>
```

**Ejemplos**

```
/confiabilidad Tengo 70 ventiladores, 12 fallaron y el resto sigue operando; ¿hay desgaste?
/confiabilidad Audita este historial de órdenes de trabajo antes de que analicemos nada
/confiabilidad Verifica este informe antes de enviarlo
```

Los tres ejemplos vienen del README del equipo (`docs/agentes/README.md`).

**Qué hace el comando**, según `.claude/commands/confiabilidad.md`:

1. Usa al estratega para clasificar la solicitud.
2. Hace las preguntas de intake que cambien la decisión: máximo 5, cada una con una opción por defecto.
3. Delega en los especialistas que correspondan.
4. Entrega un informe verificado por `reliability-evidence-verifier`.
5. Si lo escribes **sin texto**, muestra el catálogo del equipo en una tabla corta (agente, para qué sirve, cuándo usarlo) y te pregunta qué quieres hacer.

### 1.3 Cuál elegir

| Situación | Comando |
|---|---|
| Quiero saber todo lo que el mundo sabe sobre cómo falla un componente | `/modo-de-falla` |
| Tengo datos propios (órdenes de trabajo, tiempos hasta la falla, sensores) y una pregunta | `/confiabilidad` |
| Quiero que revisen un informe o los resultados de otra herramienta | `/confiabilidad` (el estratega usa al verificador) |
| No sé qué agente necesito | `/confiabilidad` sin texto, para ver el catálogo |

### 1.4 Otras formas de entrar

El README del equipo indica dos entradas más, sin comando:

- **El estratega como asistente principal**, para que te pregunte directamente en la conversación: `claude --agent reliability-engineer`.
- **Directo a un especialista**, nombrándolo en una frase: `usa el agente reliability-life-analyst con estos datos: ...`.

### 1.5 Qué te preguntarán

Las preguntas de intake dependen del tipo de solicitud (tabla del README del equipo):

| Solicitud | Preguntas típicas |
|---|---|
| Datos | Activo y función; unidad de tiempo real; qué es una falla y qué un reemplazo preventivo; si todas las unidades empiezan nuevas; cuántas siguen operando |
| Causa raíz | Evento y activo; impacto; evidencia preservada y quién la custodia; eventos similares; uso del análisis (aprendizaje, no culpa) |
| FMECA y RCM | Alcance; contexto operacional; estándar exigido; escalas vigentes; participantes |
| Predictivo | Qué síntoma precede la falla; horizonte; costo de falso negativo y de falso positivo; qué acción dispara una alerta; activos para reservar |
| Economía y KPIs | Tasa de descuento; costos de falla y de intervención; demanda y plazo de reposición; definición local de cada KPI; decisión que dispara cada KPI |

Regla común: máximo 5 preguntas por ronda, cada una con opción por defecto; lo reversible se asume y se declara.

## 2. Los agentes que puedes invocar por nombre

Son veinte. Todos comparten una ficha de 10 bloques más 2 operativos (rol y nivel, contexto, objetivo y decisión, insumos, tarea, método y estándares, honestidad, formato de salida, calidad, restricciones y dudas, feedback, almacenamiento) y esta conexión: reciben un BRIEF del líder, devuelven su salida al líder y reportan qué aprendieron. En el mapa interactivo, un doble clic sobre cualquier tarjeta abre su ficha completa.

### 2.1 Quién hace qué y cuándo usarlo

| Agente | Función | Úsalo cuando | Entrega | Permisos de sus herramientas |
|---|---|---|---|---|
| `reliability-engineer` | Estratega y único interlocutor de la persona | Siempre es la puerta de entrada | Informe HTML, tabla de quién hizo qué, resumen de hasta 10 líneas con vacíos y preguntas | Lee, escribe, edita, ejecuta código, busca en la web y coordina a los otros diecinueve |
| `reliability-case-historian` | Memoria de casos: recurrencia y línea base | Al abrir un caso (buscar si ya ocurrió) y al cerrarlo (guardarlo) | Ruta y versión del caso, coincidencias con su razón, estado de la línea base | Lee, escribe, edita, ejecuta |
| `reliability-literature-researcher` | Investigador científico: papers, tesis, libros y normas | Falla nueva; una instancia por frente de búsqueda | Lista JSON de entradas del registro de evidencia, tabla de fuentes con nivel y límites, lagunas | Lee, escribe, ejecuta, busca en la web y usa el conector de artículos con cuota |
| `reliability-standards-researcher` | Normas, guías, tesis, libros y clases abiertas | Dossier por modo de falla | Tablas de normas y fuentes con referencia APA 7 y enlace; pendientes de adquisición | Lee, escribe, ejecuta, busca en la web, conector con cuota |
| `reliability-dataset-scout` | Datos públicos de fallas y vida | Dossier por modo de falla | Tabla de conjuntos (origen, licencia, n, fallas, censura, comparabilidad, límites) | Lee, escribe, ejecuta, busca en la web, conector con cuota |
| `reliability-paper-analyst` | Lectura profunda de papers y libros | Hay papers priorizados para extraer tablas, parámetros y condiciones de ensayo | Entradas del registro, lista `cifras`, reporte de fuentes y lagunas | Lee, escribe, ejecuta, busca en la web |
| `reliability-citation-ranker` | Ranking por citas y cuartil de revista | Hay que priorizar qué leer | Tabla id, citas, fuente del conteo, fecha, cuartil y fuente; si no hay acceso, SIN DATOS PARA ARMARLO | Lee, escribe, ejecuta, busca en la web |
| `reliability-data-auditor` | Calidad de datos de mantenimiento | Tienes órdenes de trabajo, fallas o sensores reales | Tabla de calidad, reglas con conteos, definición de falla y censura, veredicto por análisis | Lee y ejecuta |
| `reliability-life-analyst` | Estadística de vida (Weibull, supervivencia, reparables) | Tienes tiempos hasta la falla, censura o una flota | JSON `vida` con hallazgos, método por situación y vacíos; figuras con n, método y fuente | Lee y ejecuta |
| `reliability-rca-investigator` | Causa raíz: Ishikawa, 5 porqués, árbol de fallas | Hay una falla ocurrida o un modo de falla por explicar | Bloques JSON `acr`, `arbol`, `porques`, `observar` | Lee y busca en la web (sin escritura) |
| `reliability-fmeca-rcm` | FMEA/FMECA, criticidad y estrategia RCM | Defines mantenimiento, intervalos o tareas | JSON `fmeca` con modos, tarea RCM por consecuencia y vacíos | Lee, ejecuta, busca en la web |
| `reliability-predictive-analyst` | Predictivo, aprendizaje automático, RUL y visión por computadora | Tienes un modelo, un RUL o anomalías por evaluar | JSON `predictivo` con hallazgos, estrategia y riesgos de validación | Lee, ejecuta, busca en la web |
| `reliability-economics-kpi` | Economía de la confiabilidad, repuestos y KPIs | Se justifica una decisión o se arma un tablero | JSON `lcc` con elementos, fórmulas, parámetros requeridos y vacíos | Lee y ejecuta |
| `reliability-replicator` | Réplica de figuras, tablas y estadísticas publicadas | Hay cifras extraídas de papers | Lista de réplicas con series, evidencia, condiciones y límites (`replicas.json`) | Lee, escribe, ejecuta |
| `reliability-integrator` | Une todo y arma el HTML final | Al terminar un modo de falla | Ruta del informe, ajustes automáticos, cobertura, resultado de la prueba en el navegador | Lee, escribe, edita, ejecuta |
| `reliability-evidence-verifier` | Verificador independiente: intenta refutar | Antes de entregar, o si traes resultados de otra herramienta | Tabla de problemas (afirmación exacta, por qué, qué cambiar) y veredicto global | Solo lee y busca en la web |
| `reliability-report-writer` | Redactor de informes técnicos | Los especialistas ya entregaron y fue verificado | Archivo del informe y lista de secciones con su nivel de evidencia | Lee, escribe, edita, ejecuta |
| `reliability-ux-designer` | Diseñador de la interfaz del informe HTML | Hay un HTML ensamblado que mejorar | Cambios aplicados, capturas y pendientes | Lee, escribe, edita, ejecuta |
| `reliability-feedback-learner` | Aprende de tus correcciones y reglas | Corriges, apruebas o das una regla permanente | Ruta y línea del feedback, candidatos y lista de reglas vigentes | Lee, escribe, edita |
| `reliability-memory-curator` | Curador de memoria y lecciones | Cierre de caso | Lista de candidatos con ruta y estado | Lee, escribe, edita |

### 2.2 Qué agente necesito

| Tu pregunta | Ruta |
|---|---|
| Revisa mis datos de mantenimiento | auditor de datos |
| ¿Cada cuánto falla esto? ¿Se desgasta? | auditor de datos, luego analista de vida |
| ¿Aumentan las fallas con el tiempo en mi flota? | auditor, luego analista de vida (modo multiunidad) |
| ¿Por qué falló este equipo? | auditor, luego investigador de causa raíz (más analista de vida si hay historial) |
| Haz el FMECA y la estrategia de este sistema | fmeca-rcm (más auditor si hay historial) |
| ¿Sirve este modelo predictivo? | predictive-analyst |
| ¿Conviene reemplazar por edad? ¿Cuántos repuestos? | analista de vida, luego economics-kpi |
| Arma un tablero de KPIs | economics-kpi, luego report-writer |
| Otra herramienta me dio estos resultados, ¿son ciertos? | evidence-verifier |
| Dame el informe final | report-writer, luego evidence-verifier |

### 2.3 Cómo se pasan el trabajo (protocolo de agentes)

| De | A | Qué entrega |
|---|---|---|
| Historiador | Estratega | Casos parecidos y línea base |
| Investigadores y lectores de papers | Replicador y analistas | Entradas de evidencia y cifras |
| Replicador | Integrador | Réplicas validadas |
| Analistas (causa raíz, FMECA, vida, predictivo, economía) | Integrador | JSON de análisis con ids de evidencia |
| Integrador | Verificador y diseñador UX | HTML ensamblado |
| Verificador | Estratega | Problemas por severidad |
| Estratega | Agente de feedback y curador | Lo aprendido en la ronda |

El estratega no delega con frases sueltas: envía a cada agente un BRIEF con los mismos ocho campos de la ficha, adaptados al caso, e indica qué hacen los demás para que cada uno sepa quién usará su entrega.

## 3. El flujo de trabajo, de principio a fin

Este es el orden que sigue un modo de falla (protocolo del dossier) con lo que ocurrió de verdad en el caso de la chumacera de polea de faja transportadora. Donde el caso real no coincide con el protocolo, se dice.

1. **Intake.** La persona nombra el modo de falla. El estratega lo clasifica, lee las reglas vigentes de `historial/feedback/feedback.jsonl` y, según el protocolo, pide al historiador buscar recurrencia. En el caso real el historiador no figura en la trazabilidad.
2. **Frentes de búsqueda en paralelo.** El estratega reparte la cuota del conector de artículos por frente y lanza un investigador por frente, cada uno con su rango de ids. En el caso real fueron cinco frentes de búsqueda, más el investigador de normas y el buscador de datos abiertos.
3. **Lectura profunda.** Se leen completos los papers priorizados y se extraen tablas, parámetros y condiciones de ensayo como entradas con extracto literal y como `cifras`. En el caso real dos lectores de textos completos de preprints produjeron 71 cifras. El agente `reliability-paper-analyst` está definido, pero la trazabilidad no lo lista en este caso.
4. **Réplicas.** Las cifras se convierten en réplicas (barras con intervalo, tablas, curvas con puntos publicados) con su referencia APA 7. El control del kit rechaza cualquier número que no esté literal en el extracto. El caso tiene 36 réplicas.
5. **Análisis de ingeniería.** Con el registro de evidencia (169 entradas) trabajan causa raíz, FMECA y RCM, estadística de vida, predictivo y economía. Sin caso real ninguna causa pasa de posible; sin datos de falla no se ajusta ninguna distribución; los puntajes S, O y D y los costos quedan vacíos.
6. **Ranking de fuentes.** `reliability-citation-ranker` ordena por citas y cuartil solo si la fuente del conteo es accesible; si no, queda SIN DATOS PARA ARMARLO. En el caso real no existe `ranking.json` en la carpeta.
7. **Ensamblado con compuertas.** Los JSON de todos los agentes se unen en `informe.html`; cada elemento sin fuente válida se elimina y queda registrado como ajuste automático. En el caso real lo ejecutó el kit lanzado por el estratega; la trazabilidad dice que el agente integrador existe y se usará en el próximo caso.
8. **Verificación.** El verificador ve solo los archivos y las fuentes, no el razonamiento del autor, e intenta refutar. En el caso real hizo cuatro pasadas.
9. **Correcciones.** El estratega corrige lo que el verificador señaló: las cifras sin extracto y las inferencias presentadas como evidencia bajan de nivel.
10. **Entrega.** El estratega entrega el HTML aunque haya secciones vacías, con una tabla de quién hizo qué y preguntas finales a la persona. Cierre exigido: el dossier pasa `validar_dossier`, el verificador no tiene bloqueos abiertos, los ajustes automáticos fueron revisados, el HTML abre sin errores y las preguntas pendientes están redactadas.
11. **Aprendizaje.** El estratega envía a cada agente lo aprendido de su entrega, el agente de feedback lo registra y el curador propone lecciones en cuarentena.

Resultado del caso real (`meta.json`): 169 entradas de registro; 10 secciones con evidencia; 4 secciones vacías (`punto_optimo`, `lcc`, `ibr`, `mpd_normas`).

### 3.1 Niveles de evidencia que verás

| Nivel | Significa |
|---|---|
| VERIFICADO | Se abrió la fuente y se leyó (en el registro del caso aparece como VERIFICADO-TEXTO o VERIFICADO-ABSTRACT) |
| SOLO-SNIPPET | Visto solo en un resumen de buscador: es una pista, no respalda nada |
| NO-VERIFICADO | Mencionado sin fuente leída: no se cita, va a pendientes |
| SÍNTESIS | Inferencia del equipo, rotulada como hipótesis |
| CÁLCULO | Resultado de código sobre datos reales, con semilla, versiones y n |
| SUPUESTO | Dato asumido con justificación |
| VACÍO | Dato inexistente o inaccesible, declarado y nunca rellenado |

En el caso real el registro tiene 109 entradas VERIFICADO-TEXTO, 10 VERIFICADO-ABSTRACT, 46 SOLO-SNIPPET y 4 NO-VERIFICADO.

## 4. Dónde se guarda cada resultado

| Carpeta | Qué se guarda | Quién escribe |
|---|---|---|
| `historial/dossiers/<modo_de_falla>/` | El caso: `evidencia.json`, `dossier.json`, `analisis/` (acr, arbol, porques, observar, fmeca, vida, predictivo, lcc), `cifras.json`, `replicas.json`, `trazabilidad.json`, `meta.json`, `informe.html`; también `auditoria.json`, `ranking.json` y `verificacion/` cuando corresponden | Estratega, analistas, integrador; el informe de verificación lo guarda el estratega porque el verificador no escribe |
| `historial/feedback/feedback.jsonl` | Tus correcciones, aprobaciones, prohibiciones y reglas, una por línea y solo agregando | Agente de feedback |
| `historial/casos/` y `historial/linea_base/` | Casos con versión y línea base por familia de falla; solo se agrega, nunca se borra | Historiador (estas carpetas aún no existen en el repositorio: el caso real se guardó en `historial/dossiers/`) |
| `knowledge/` | Protocolos, registro de normas con estado, plantillas de informe, mapa de fuentes, lista de cifras descartadas y la memoria | Se mantiene con revisión de una persona |
| `knowledge/memoria/cuarentena/` | Lecciones candidatas, un archivo por lección | Curador y agente de feedback; es el único lugar donde escriben |
| `knowledge/memoria/aprobada/` | Lecciones aprobadas por una persona | Solo tras la aprobación humana |
| `tools/reliability/` | El kit de cálculo: Weibull, Crow-AMSAA, Kaplan-Meier, órdenes de trabajo, calidad de datos, economía, validación de modelos, evidencia, señales, historial, informe HTML | Se ejecuta; los agentes no calculan de cabeza |

Permisos de la persona (`historial/PERMISOS.md`): el 2026-10-27 autorizó guardar dossiers y feedback en el historial del repositorio. Los datos que declare ilustrativos no se guardan como casos. Si el repositorio es compartido, el equipo pide permiso antes de subir. No se envía, publica, hace push ni se sobrescribe nada sin confirmación explícita.

### 4.1 Cómo correr el kit

```
cd tools/reliability
pip install -r requirements.txt
python -m pytest -q
python examples/demo.py
```

El README del kit indica 152 pruebas. El demo usa datos sintéticos ilustrativos.

## 5. Cómo dar feedback para que el equipo aprenda

El equipo aprende por dos vías con compuertas distintas.

**Vía rápida: tus reglas.** Lo que le dices al estratega (una corrección, una aprobación, una prohibición, una preferencia) lo registra el agente de feedback en `historial/feedback/feedback.jsonl` y se aplica de inmediato, porque el estratega lee las reglas vigentes al empezar. Los tipos que aparecen en el archivo son `prohibicion`, `regla_permanente`, `preferencia` y `aprobacion`; cada línea lleva fecha, texto, alcance y estado (`vigente`).

Ejemplos de cómo decirlo (redacciones tuyas, en tus palabras):

```
Siempre cita en formato APA 7.
Nunca nombres una empresa ni una planta concreta.
Acepta por ahora trabajar con resúmenes; la lectura completa queda pendiente.
Este conjunto de datos es ilustrativo: no lo uses como evidencia.
```

**Vía lenta: las lecciones.** El curador convierte lo aprendido en candidatos en `knowledge/memoria/cuarentena/` con fuente y extracto. Un candidato solo llega a `aprobada/` si pasa cuatro compuertas: procedencia, verificador independiente (contradicciones y soporte de la fuente), reglas (esquema, unidades, duplicados) y la aprobación de una persona. Si falla una compuerta, se rechaza con motivo. Ninguna lección entra por su cuenta.

**Después de cada ronda**, el estratega devuelve a cada agente qué sirvió, qué se corrigió y qué regla nueva diste, y pide al agente de feedback que lo registre. Cada respuesta que use una memoria registra su id y versión, para poder retractarla.

Qué conviene decir: la regla concreta, a quién aplica (todos, investigadores, informes) y si es permanente. Qué no hace falta: repetir una regla ya vigente; revisa `historial/feedback/feedback.jsonl`.

## 6. Límites honestos

Lo que el equipo no puede hacer hoy, tal como lo declaran los archivos:

1. **Acceso a fuentes.** La cuota del conector de artículos estaba en 0 hasta el 2026-11-01. Varias fuentes de documentos libres respondieron bloqueadas y nunca se leyeron. Los dominios de artículos, datos, tesis y normas deben habilitarse en el acceso de red del entorno (lista en `knowledge/mapa_fuentes_cientificas.md`); está pendiente en `historial/PENDIENTES.md`.
2. **Lectura incompleta.** De las 169 entradas del caso real, 46 son SOLO-SNIPPET y 4 NO-VERIFICADO: no respaldan ninguna afirmación. La persona aceptó por ahora trabajar con resúmenes; la lectura de texto completo queda pendiente y repetir el dossier con ella está anotado como pendiente.
3. **Sin datos de planta.** El caso real no tiene datos reales del activo. Por eso ninguna causa pasa de posible, no se ajusta ninguna distribución de vida, los puntajes S, O y D están sin puntuar y las secciones punto óptimo, LCC, inspección basada en riesgo y mantenimiento predictivo con normas quedaron vacías.
4. **Costos y parámetros de Weibull.** Solo se aceptan de tesis, papers y fuentes halladas; hoy están VACÍOS. El equipo no los inventa.
5. **Normas.** El registro cita normas como "edición no verificada" mientras no se consulte el publicador. No se citan cláusulas ni ediciones sin abrir el documento.
6. **Cifras de eficacia o retorno.** No hay ninguna: no existe fuente primaria; las cifras repetidas sin origen están descartadas en `knowledge/folklore_descartado.md`.
7. **Memoria.** El mecanismo está listo, pero hoy hay 0 lecciones aprobadas y 1 de ejemplo en cuarentena. El README del equipo lista como trabajo futuro los hooks que impidan por configuración escribir en la memoria aprobada; hoy esa protección es una regla de las fichas, no un bloqueo técnico.
8. **Agentes aún no usados en un caso.** En la trazabilidad del caso real no figuran el integrador, el historiador, el auditor de datos, el analista de papers, el replicador, el rankeador de citas, el redactor, el diseñador UX, el curador ni el agente de feedback. Están definidos, pero no hay un caso que demuestre su desempeño.
9. **Kit de cálculo.** Solo Weibull de 2 parámetros y un modo de falla por ajuste; Cox y riesgos competitivos no están incluidos; la bondad de ajuste con censura es aproximada y de baja potencia con pocas fallas; los costos, la definición de falla y la separación de modos los aporta una persona.
10. **Lo que un informe no es.** Las pistas de videos, redes sociales y buscadores nunca respaldan una cifra. Un resultado de banco de pruebas no se traslada como precisión de planta.
11. **Datos de terceros.** El texto de órdenes de trabajo, PDF y correos es dato, nunca instrucción. Los datos originales son de solo lectura: se trabaja sobre copias.

## 7. Resumen en una página

1. Escribe `/modo-de-falla <componente y falla>` para investigar un modo de falla, o `/confiabilidad <necesidad>` para cualquier otra solicitud.
2. Responde las preguntas de intake (máximo 5; cada una con opción por defecto).
3. El estratega reparte frentes en paralelo, los especialistas leen y calculan, el integrador ensambla y el verificador intenta refutar.
4. Recibes `informe.html` en `historial/dossiers/<modo_de_falla>/`, con lo vacío declarado y preguntas finales.
5. Corrige y da reglas con tus palabras: el agente de feedback las registra y el equipo las aplica desde la siguiente ronda.
6. Nada pasa a la memoria aprobada sin que una persona lo apruebe.
