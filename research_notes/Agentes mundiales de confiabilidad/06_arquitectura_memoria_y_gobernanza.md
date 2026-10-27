# Arquitectura de memoria, aprendizaje seguro, proveniencia y gobernanza para un agente técnico de confiabilidad

**Fecha de acceso:** 2026-10-27 (UTC). **Versión visible de Claude Code:** las páginas de code.claude.com no muestran un número de versión global; la versión más alta citada en las páginas de subagentes/memoria es "Claude Code v2.1.296 or later" (campos `autoCompactWindow`, detección de campos desconocidos). Las páginas cambian rápido: re-verificar antes de implementar.

**Convención de estado:** VERIFICADO = leí el texto en la fuente primaria (o abstract/texto del paper vía espejo) en esta sesión. SOLO-SNIPPET = solo vi el resumen devuelto por el buscador, sin abrir la página. NO-VERIFICADO = no lo vi. **SÍNTESIS** = recomendación de diseño mía, no documentada por la fuente.

**Fallos de acceso (reportados):**
- `WebFetch` → `getaddrinfo ENOTFOUND` para arxiv.org y genai.owasp.org.
- `curl` vía proxy → `CONNECT tunnel failed, response 403` para arxiv.org, export.arxiv.org, alphaxiv, huggingface.co/papers (web), genai.owasp.org, owasp.org, nist.gov, airc.nist.gov, csrc.nist.gov, iso.org, mlflow.org, docs.mem0.ai, docs.letta.com, langchain-ai.github.io, docs.langchain.com, modelcontextprotocol.io, isa.org, api.semanticscholar.org. No se disimuló ni se evadió el proxy.
- `curl` OK (200): code.claude.com/docs/en/{sub-agents,memory,hooks,skills,mcp,permissions} y platform.claude.com/docs/en/{build-with-claude/citations, test-and-evaluate/strengthen-guardrails/reduce-hallucinations}.
- Papers arXiv: leídos vía el conector Hugging Face (`hf://papers/<id>/paper.md`, que replica el texto arXiv). Normas (NIST, ISO, IEC, OWASP), MLflow, Letta, LangGraph, Mem0 docs, Maximo/PI/Power BI: **solo snippets de WebSearch**.
- No se usó ninguna herramienta mcp__github__*.

---

## 1. Documentación oficial de Claude Code: subagentes, skills, hooks, memoria, MCP, permisos

### Takeaway
Claude Code soporta hoy (según la documentación leída) subagentes con frontmatter (tools/disallowedTools/model/permissionMode/skills/mcpServers/hooks/memory), skills con `allowed-tools`/`disallowed-tools`/`context: fork`, hooks de ciclo de vida con decisión `deny` en PreToolUse, auto-memory por proyecto con índice `MEMORY.md`, y MCP con alcances local/proyecto/usuario y aprobación. La propia doc aclara que CLAUDE.md y la memoria son **contexto, no configuración forzada**; lo que se debe garantizar va en hooks/permisos.

### Cited Findings

**Subagentes** (https://code.claude.com/docs/en/sub-agents, VERIFICADO)
| Campo | Qué dice la doc | Estado |
|---|---|---|
| `name`, `description` | Únicos obligatorios; `name` ≤256 caracteres, sin `:` | VERIFICADO |
| `tools` / `disallowedTools` | Lista separada por comas o YAML; si se omite `tools`, hereda todas las herramientas; `disallowedTools` se resta | VERIFICADO |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, ID completo (p. ej. `claude-opus-5-5`) o `inherit`. Orden de resolución: parámetro por invocación → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → modelo de la conversación principal | VERIFICADO |
| `permissionMode` | `default, acceptEdits, auto, dontAsk, bypassPermissions, plan, manual`; ignorado en subagentes de plugin | VERIFICADO |
| `maxTurns`, `autoCompactWindow`, `effort`, `isolation: worktree`, `background`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental.cacheTtl` | Descritos en la tabla de frontmatter | VERIFICADO |
| `skills` | Precarga el contenido completo de skills al inicio del subagente | VERIFICADO |
| `mcpServers`, `hooks` | Servidores MCP y hooks con alcance al subagente; ignorados en subagentes de plugin | VERIFICADO |
| `memory` | `user` → `~/.claude/agent-memory/<nombre>/`; `project` → `.claude/agent-memory/<nombre>/`; `local` → `.claude/agent-memory-local/<nombre>/`. Activa Read/Write/Edit automáticamente e inyecta las primeras 200 líneas o 25 KB de `MEMORY.md`. Si auto-memory está desactivada, el campo no tiene efecto. La doc recomienda `project` como alcance por defecto | VERIFICADO |
| Campos desconocidos | Se ignoran sin error; `claude --debug` los reporta (v2.1.296+) | VERIFICADO |
| Archivos omitidos | Sin `name`, sin `description` o YAML inválido → el archivo se omite silenciosamente | VERIFICADO |

**Memoria** (https://code.claude.com/docs/en/memory, VERIFICADO)
- Dos sistemas: CLAUDE.md (instrucciones que escribes) y auto-memory (notas que Claude escribe). "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."
- Auto-memory guarda cuatro tipos en el frontmatter (`type`): `user`, `feedback`, `project`, `reference`. Omite lo derivable del código/git.
- Activada por defecto en sesiones locales; se desactiva con `autoMemoryEnabled: false` o `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; directorio configurable con `autoMemoryDirectory`.
- Ubicación: `~/.claude/projects/<proyecto>/memory/` con `MEMORY.md` (índice) + un archivo por memoria; es **local a la máquina**, compartida entre worktrees del mismo repo; se carga al inicio el máximo de 200 líneas o 25 KB de `MEMORY.md`; los archivos de tema se leen bajo demanda; se excluyen de la limpieza por `cleanupPeriodDays`.
- Son markdown plano editable; `/memory` permite explorarlas/editarlas. La memoria principal NO se carga en subagentes (salvo fork).
- CLAUDE.md gestionado por la organización existe; "use settings for technical enforcement and CLAUDE.md for behavioral guidance".

**Hooks** (https://code.claude.com/docs/en/hooks, VERIFICADO)
- Eventos listados en el índice: SessionStart, InstructionsLoaded, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, PermissionDenied, Notification, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, PostToolBatch, ConfigChange, FileChanged (entre otros).
- Tipos de handler: `command`, `http`, `mcp_tool`, `prompt` y `agent` (este último marcado "experimental and may change").
- PreToolUse puede devolver `permissionDecision: "deny"` con `permissionDecisionReason` (ejemplo oficial de bloqueo de `rm -rf`). Exit code 2 tiene comportamiento de bloqueo por evento.
- Los hooks `mcp_tool` no corren en SessionStart al lanzamiento (no hay cliente MCP aún); usar `command`.

**Skills** (https://code.claude.com/docs/en/skills, VERIFICADO)
- Frontmatter: `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `context: fork` + `agent`, `background`, `hooks`, `paths`.
- `allowed-tools` pre-aprueba herramientas solo durante el turno que invoca la skill; "a skill can grant itself broad tool access" y el grant de un skill de proyecto aplica incluso sin confianza de workspace (aviso de seguridad en la misma página).
- Las skills con `disable-model-invocation: true` no se pueden precargar en subagentes.

**MCP** (https://code.claude.com/docs/en/mcp, VERIFICADO)
- Alcances: local (por defecto, `~/.claude.json`), proyecto (`.mcp.json` versionado, requiere aprobación; un repo clonado no puede auto-aprobar sus servidores) y usuario.
- Advertencia oficial: "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk."
- Control corporativo: `managed-mcp.json`, `managedMcpServers`, `allowedMcpServers`, `deniedMcpServers`; `--strict-mcp-config`.

**Permisos** (https://code.claude.com/docs/en/permissions, VERIFICADO): reglas evaluadas en orden deny → ask → allow; un deny amplio no se puede exceptuar con un allow más específico; modo `plan` = solo lectura/exploración; `permissions.disableBypassPermissionsMode`/`disableAutoMode` en settings gestionados.

**Grounding con la API de Claude** (VERIFICADO)
- Citations: devuelve pasajes exactos; "citations are guaranteed to contain valid pointers to the provided documents"; la doc afirma (evaluaciones propias de Anthropic) que es "significantly more likely" citar las citas más relevantes que con prompting puro — https://platform.claude.com/docs/en/build-with-claude/citations
- Guía de alucinaciones: permitir "No sé", extraer citas literales primero (>20k tokens), exigir cita por afirmación y retractarla si no hay cita de respaldo — https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

### Inferences (SÍNTESIS)
- Para un agente de confiabilidad: definir subagentes con `tools` mínimos (Read/Grep + herramientas MCP de solo lectura), `disallowedTools` para Write/Bash en los agentes de análisis, `memory: project` solo en un agente "curador", y un hook `PreToolUse` que bloquee cualquier tool MCP de escritura. La regla de oro de la doc (CLAUDE.md = contexto, hooks = garantía) implica que las políticas de "no escribir en CMMS" deben ir en permisos/hooks, no solo en el prompt.
- Auto-memory es local a la máquina y sin revisión: para memoria de equipo con validación, usar un directorio versionado (p. ej. `memory: project` o `autoMemoryDirectory` en repo) y revisión por pull request.

### Gaps
- No leí la documentación del Claude Agent SDK (platform.claude.com/docs ... agent-sdk) ni confirmé paridad de campos con el SDK. NO-VERIFICADO.
- No verifiqué la página de "settings" completa ni el esquema de `managed-mcp.json`.
- No hay (que yo haya visto) una "memory tool" de la API verificada en esta sesión: NO-VERIFICADO.

---

## 2. Patrones de memoria de agentes y riesgos (memory poisoning, deriva, obsolescencia)

### Takeaway
Hay base publicada para memoria jerárquica (MemGPT), extracción/consolidación (Mem0), memoria de eventos+reflexión (Generative Agents), taxonomía episódica/semántica/procedimental (CoALA, LangGraph). El riesgo está documentado empíricamente: AgentPoison logra ≥80 % de éxito con <0,1 % de envenenamiento; MINJA inyecta memoria solo con consultas normales. Las defensas con evidencia son validación por consenso, memoria dual de "lecciones" y saneamiento con confianza/decaimiento temporal; ninguna es una solución cerrada.

### Cited Findings
| Patrón | Qué resuelve | Riesgo | Fuente URL | Estado |
|---|---|---|---|---|
| Contexto virtual / memoria por niveles (MemGPT) | Contexto limitado: pagina entre contexto principal y almacenamiento externo; agentes conversacionales con memoria multi-sesión | Dependencia de decisiones del LLM para gestionar memoria (crítica de trabajos posteriores, solo snippet) | https://arxiv.org/abs/2310.08560 (texto leído vía espejo HF) | VERIFICADO (abstract); críticas SOLO-SNIPPET |
| Extracción-consolidación-recuperación (Mem0) y variante con grafo | Consistencia en diálogos largos; −91 % latencia p95 y >90 % menos tokens vs. contexto completo; +26 % relativo en LLM-as-judge vs. OpenAI (benchmark LOCOMO) | Cifras reportadas por los autores del producto y medidas con LLM-as-judge (sesgos, ver sec. 3) | https://arxiv.org/abs/2504.19413 | VERIFICADO (abstract) |
| Flujo de memoria + reflexión + recuperación (Generative Agents) | Almacena experiencias en lenguaje natural, las sintetiza en reflexiones de nivel superior, las recupera para planificar | Reflexiones sin verificación pueden fijar errores (inferencia mía) | https://arxiv.org/abs/2304.03442 | VERIFICADO (abstract) |
| CoALA: módulos de memoria modulares + espacio de acciones estructurado | Marco para organizar agentes; separa memoria de trabajo y memorias de largo plazo | Es un marco conceptual, no una política de seguridad | https://arxiv.org/abs/2309.02427 | VERIFICADO (abstract) |
| Taxonomía semántica/episódica/procedimental en LangGraph; memoria en JSON bajo namespace+key; escritura "on the hot path" o en segundo plano; `InMemoryStore` solo desarrollo | Aislamiento por namespace (usuario/org); cross-thread | Escritura en la ruta crítica = el agente decide qué recordar sin revisión | https://docs.langchain.com/oss/python/concepts/memory | SOLO-SNIPPET |
| Letta: bloques de memoria editables siempre en contexto (<50k caracteres, <20 bloques recomendados) + memoria de archivo con búsqueda semántica (`archival_memory_insert/search`) | Separar hechos críticos pequeños de repositorios grandes | Bloques pueden quedar obsoletos (nota de Letta: pueden deprecarse en v1 API) | https://docs.letta.com/guides/core-concepts/memory/context-hierarchy/ ; https://docs.letta.com/guides/core-concepts/memory/archival-memory/ | SOLO-SNIPPET |
| Reflexion (retroalimentación verbal guardada en memoria episódica) | Aprender de intentos fallidos sin reentrenar | Si el evaluador es falible, se memoriza una "lección" errónea (inferencia mía) | https://arxiv.org/abs/2303.11366 | VERIFICADO (solo título/estructura leídos; abstract no capturado) |
| Auto-memory de Claude Code (4 tipos, índice MEMORY.md, local) | Persistencia simple, editable, auditable en markdown | Sin validación automática; local a la máquina | https://code.claude.com/docs/en/memory | VERIFICADO |

**Riesgos documentados**
| Riesgo | Evidencia | Fuente URL | Estado |
|---|---|---|---|
| Backdoor por envenenamiento de memoria/KB (AgentPoison) | Éxito medio ≥80 %, impacto en rendimiento benigno ≤1 %, tasa de veneno <0,1 %; probado en agente de conducción, QA y EHRAgent (salud) | https://arxiv.org/abs/2407.12784 | VERIFICADO |
| Inyección de memoria solo vía consultas (MINJA) | Un usuario cualquiera puede introducir registros maliciosos que luego se recuperan para otras consultas | https://arxiv.org/abs/2503.03704 | VERIFICADO (abstract) |
| MINJA en condiciones realistas | Reporta >95 % de inyección y 70 % de éxito de ataque en condiciones ideales; con memorias legítimas preexistentes la eficacia cae drásticamente; defensas propuestas: moderación E/S con puntuación de confianza compuesta y saneamiento de memoria con recuperación ponderada por confianza y decaimiento temporal | https://arxiv.org/abs/2601.05504 | VERIFICADO (abstract; la página dice "texto completo no disponible", versión resumida) |
| Ciclo de error auto-reforzante: el resultado corrupto se guarda como precedente y baja el umbral para ataques futuros; el efecto solo se activa en contexto específico, difícil de detectar auditando entradas aisladas | A-MemGuard: validación por consenso (compara rutas de razonamiento de varias memorias relacionadas) + memoria dual donde los fallos se destilan en "lecciones" separadas consultadas antes de actuar | https://arxiv.org/abs/2510.02373 | VERIFICADO (abstract) |
| Otros ataques/defensas recientes (MemoryGraft 2512.16962, Zombie Agents 2602.15654, DREAM 2610.13267, MemAdapter 2610.05162) | Solo títulos y descripción de una línea | https://arxiv.org/abs/2512.16962 ; https://arxiv.org/abs/2602.15654 ; https://arxiv.org/abs/2610.13267 | SOLO-SNIPPET |
| Inyección indirecta de prompt (datos recuperados como instrucciones) | Difumina la línea entre datos e instrucciones; permite robo de datos, "worming", contaminación del ecosistema de información | https://arxiv.org/abs/2302.12173 | VERIFICADO (abstract) |
| Patrones de diseño con resistencia demostrable a prompt injection (trade-offs utilidad/seguridad) | Marco de patrones para agentes con acceso a herramientas | https://arxiv.org/abs/2506.08837 | VERIFICADO (abstract; patrones específicos no leídos) |

**Política de "escritura a memoria con verificación" sostenida por evidencia** (lo que la evidencia respalda, sin ser una receta única):
- Validación cruzada (consenso) y memoria separada de lecciones: A-MemGuard (arriba).
- Puntuación de confianza + decaimiento temporal en recuperación: 2601.05504.
- Memorias legítimas preexistentes diluyen el ataque (2601.05504): un corpus curado grande es defensivo, hallazgo en EHR agents, no generalizable sin pruebas propias.
- Ninguna fuente leída prueba que una política concreta elimine el riesgo.

### Inferences (SÍNTESIS)
- Ciclo de aprendizaje con compuertas (propuesta mía, no documentada como estándar):
  1. **Captura:** el agente propone un "candidato de memoria" (nunca escribe directo a memoria productiva) con: enunciado, tipo (semántico/episódico/procedimental), `source_id`+pasaje citado, fecha del hecho, activo/ámbito (equipo, planta), autor (agente/humano), confianza.
  2. **Compuerta 1 – Procedencia:** rechazo automático si falta cita verificable a documento/OT/registro CMMS con identificador; el contenido proveniente de herramientas o documentos se trata como datos no confiables (anti inyección indirecta).
  3. **Compuerta 2 – Verificación independiente:** otra instancia/verificador (sin ver el razonamiento original) comprueba cada afirmación contra la fuente (CoVe-style) y revisa conflicto con memoria existente (consenso a la A-MemGuard).
  4. **Compuerta 3 – Reglas deterministas:** esquema, rangos físicos plausibles, unidades, ID de activo existente en la jerarquía, detección de duplicados/contradicciones.
  5. **Compuerta 4 – Humano:** aprobación por ingeniero de confiabilidad para memorias que cambien criterios de decisión (procedimental) o afecten acciones de mantenimiento; auto-aprobación solo para hechos de bajo riesgo con cita literal.
  6. **Cuarentena y versionado:** las memorias entran como `estado=propuesta` en un área separada; al aprobarse, se versionan (git/commit o registro inmutable con hash, autor, fecha, fuente); nunca se sobrescribe, solo se supersede.
  7. **Vigencia:** `valid_from/valid_to`, `revisar_antes_de`, decaimiento de confianza; las memorias sobre estado de equipos expiran rápido.
  8. **Reversión y auditoría:** cada respuesta registra qué memorias usó (IDs/versiones) para poder retractarlas y re-evaluar respuestas afectadas; "lecciones" derivadas de fallos van a una memoria aparte (A-MemGuard).
  9. **Regresión:** cualquier cambio de memoria procedimental ejecuta el conjunto de evaluación (sec. 5) antes de pasar a producción.
- Mapeo a Claude Code: `memory: project` en repositorio versionado + revisión por PR = Compuerta 4 y versionado; hook `PostToolUse`/`PreToolUse` sobre Write en el directorio de memoria para forzar el esquema y bloquear escrituras directas en la carpeta "aprobada" (mecanismo SÍNTESIS apoyado en hooks VERIFICADOS).

### Gaps
- No pude abrir las páginas de docs de Mem0, Letta ni LangGraph (403); sus afirmaciones están a nivel de snippet.
- No encontré evidencia que cuantifique el efecto de una política "verificar antes de escribir" en agentes de mantenimiento; la evidencia es de dominios EHR/QA/conducción.
- No leí el texto completo de Generative Agents sobre recencia/importancia/relevancia (solo el abstract).

---

## 3. Reducción de alucinaciones, citas obligatorias, abstención y evaluación

### Takeaway
Las técnicas con fuente son: permitir abstención y exigir citas literales (guía de Anthropic), generación con citas y su evaluación (ALCE), verificación por preguntas independientes (CoVe), recuperación adaptativa con autocrítica (Self-RAG) y detección por consistencia (SelfCheckGPT). ALCE muestra que incluso los mejores modelos carecen de soporte completo de citas ~50 % de las veces en ELI5, por lo que la verificación fuente por fuente sigue siendo necesaria. LLM-as-judge es útil (>80 % de acuerdo con humanos en MT-bench) pero tiene sesgos documentados.

### Cited Findings
| Patrón | Qué resuelve | Riesgo | Fuente URL | Estado |
|---|---|---|---|---|
| Permiso explícito de "no sé" + citas literales + retractar afirmaciones sin cita | Reducción de afirmaciones sin sustento (guía oficial) | Es guía de prompting, sin cifras en la página | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | VERIFICADO |
| API de Citations (`citations: {enabled: true}`) | Punteros válidos a documentos fuente, `cited_text` extraído | Cita lo que se le entrega: si el documento es erróneo/obsoleto, la cita es "válida" pero incorrecta (inferencia mía) | https://platform.claude.com/docs/en/build-with-claude/citations | VERIFICADO |
| ALCE: benchmark de generación con citas (fluidez, corrección, calidad de citas) | Medición reproducible de verificabilidad | Mejores modelos sin soporte completo de citas ~50 % en ELI5 | https://arxiv.org/abs/2305.14627 | VERIFICADO |
| Chain-of-Verification (borrador → preguntas de verificación → respuestas independientes → respuesta final) | Reduce alucinaciones en listas Wikidata, MultiSpanQA, texto largo | Costo extra de inferencia | https://arxiv.org/abs/2309.11495 | VERIFICADO |
| Self-RAG (tokens de reflexión, recuperación bajo demanda) | Mejora factualidad y exactitud de citas en generación larga | Requiere entrenar el modelo; no aplicable directamente a un LLM comercial por API | https://arxiv.org/abs/2310.11511 | VERIFICADO (abstract) |
| SelfCheckGPT (muestreo y consistencia) | Detección sin recursos externos; caja negra | Detecta inconsistencia, no verdad (un error consistente pasa) | https://arxiv.org/abs/2303.08896 | VERIFICADO (abstract) |
| Abstención (survey, conformal abstention, [IDK] token, TruthRL) | Reducir alucinaciones con rechazo calibrado | Solo títulos/descripciones vistos | https://arxiv.org/abs/2407.18418 ; https://arxiv.org/abs/2405.01563 ; https://arxiv.org/abs/2509.25760 | SOLO-SNIPPET |
| LLM-as-a-judge | >80 % de acuerdo con preferencias humanas (igual que entre humanos); sesgos de posición, verbosidad, autopreferencia y razonamiento limitado | Sesgos | https://arxiv.org/abs/2306.05685 | VERIFICADO |
| Sesgo de orden del evaluador | Un modelo puede "ganar" 66 de 80 consultas solo cambiando el orden; calibración: evidencia múltiple, posición balanceada, humano en el lazo | Ranking manipulable | https://arxiv.org/abs/2305.17926 | VERIFICADO |
| Otros estudios de sesgo en jueces (CALM 2410.02736; posición 2406.07791; survey 2411.15594) | Cuantifican sesgos | Solo snippet | https://arxiv.org/abs/2410.02736 | SOLO-SNIPPET |
| τ-bench: interacción herramienta-agente-usuario con reglas de dominio; compara estado final de la base de datos con el objetivo; métrica pass^k de consistencia | Evalúa fiabilidad y cumplimiento de políticas; gpt-4o <50 % de tareas y pass^8 <25 % (retail) en el momento del paper | Modelos desactualizados (cifras de 2024) | https://arxiv.org/abs/2406.12045 | VERIFICADO |
| MLflow GenAI evaluation: `mlflow.genai.evaluate()`, jueces LLM integrados y personalizados, scorers de código, datasets de evaluación (requieren backend SQL), evaluación de trazas incluyendo trayectoria de herramientas y recall de documentos recuperados; el monitoreo automático de producción solo admite jueces LLM (no scorers de código) | Evaluación continua y regresión | Las páginas muestran modelos por defecto distintos (gpt-4o-mini vs gpt-4.1-mini): documentación inconsistente | https://mlflow.org/docs/latest/genai/eval-monitor/ | SOLO-SNIPPET |

### Inferences (SÍNTESIS)
- Regla de citas para reportes técnicos: cada afirmación numérica/causal lleva `source_id` + extracto literal + localizador (página/campo/OT); un verificador separado comprueba que el extracto soporta la afirmación; si no, se elimina o se marca "sin evidencia". Abstención obligatoria cuando faltan datos (p. ej. historial de fallas insuficiente para Weibull).
- Evaluación: conjunto dorado versionado de casos reales de confiabilidad (con respuesta esperada y fuentes), métricas deterministas (cita válida, ID de activo existente, unidades) + juez LLM calibrado con muestras humanas y orden aleatorizado, tests de regresión ante cada cambio de prompt/skill/memoria; usar pass^k para medir consistencia (τ-bench).
- Un juez del mismo modelo que el agente introduce autopreferencia (sesgo documentado en 2306.05685): usar otro modelo o humano para auditar una muestra.

### Gaps
- No pude abrir la documentación de MLflow (403); no verifico APIs exactas ni versión.
- No encontré benchmark específico de mantenimiento/confiabilidad industrial para agentes LLM en la búsqueda HF (resultados fueron legal, GUI, etc.): NO-VERIFICADO que exista.
- No localicé la fuente primaria del trabajo de OpenAI sobre incentivos de evaluación que premian adivinar; no lo cito.

---

## 4. Integración con sistemas industriales (CMMS, historians, Power BI) y ciberseguridad OT

### Takeaway
Existen servidores MCP de comunidad para Maximo y PI (no oficiales de proveedor, según la búsqueda) y Microsoft publica servidores MCP de Power BI (remoto en preview, y de modelado local). No encontré servidor MCP para SAP PM. Los principios OT (zonas y conduits de IEC 62443; guía NIST SP 800-82r3) respaldan un diseño de solo lectura, segmentado y con aprobaciones, pero las citas normativas de esta sección están a nivel de snippet.

### Cited Findings
| Sistema | Qué existe | Riesgo / nota | Fuente URL | Estado |
|---|---|---|---|---|
| IBM Maximo | Servidores MCP de comunidad (p. ej. "Maximo Enterprise MCP" en PyPI, con herramientas de escritura deshabilitadas por defecto; otro que espera API key con permiso de lectura) | No oficiales; revisar licencia, código y alcance de escritura | https://socket.dev/pypi/package/maximo-enterprise-mcp ; https://glama.ai/mcp/servers/MaxisTechnology-Dev/Maximo-MCP | SOLO-SNIPPET |
| AVEVA PI System | Servidor MCP listado en directorio comunitario; soporta escrituras a archivos de series de tiempo y AF; indica verificación TLS y controles de escritura | No es solo lectura por diseño: verificar que la escritura se pueda deshabilitar | https://mcpmarket.com/server/aveva-pi-system | SOLO-SNIPPET |
| SAP PM | No hallé servidor MCP; solo referencia de integración vía NetWeaver Gateway en otro producto | Probable wrapper propio | https://docs.hexagonppm.com/r/en-US/j5-Interoperability-Reference/Version-30/1075964 | SOLO-SNIPPET |
| Power BI | Servidor MCP remoto (esquemas, generar y ejecutar DAX; requiere licencia Copilot; en preview) y servidor de modelado local (ejecuta y valida DAX; pide aprobación antes del primer cambio de modelo y primera consulta salvo configuración) | Preview; el LLM puede producir resultados inesperados o cambios no deseados (advertencia citada por el buscador desde la doc) | https://learn.microsoft.com/en-in/power-bi/developer/mcp/mcp-servers-overview ; https://learn.microsoft.com/et-ee/power-bi/developer/mcp/remote-mcp-server-tools | SOLO-SNIPPET |
| NIST SP 800-82 Rev. 3 (Guía de seguridad OT), final 2023-09-28; incluye overlay OT de SP 800-53 Rev.5 (Apéndice F) | Principios para seguridad OT considerando desempeño, confiabilidad y seguridad | El listado de CSRC muestra también un borrador de Rev. 4 (fecha indicada 2026-09-21): no verificado, confirmar vigencia | https://www.nist.gov/news-events/news/2023/09/nist-publishes-guide-operational-technology-ot-security ; https://csrc.nist.gov/Projects/operational-technology-security/publications | SOLO-SNIPPET |
| IEC 62443: siete requisitos fundamentales (identificación/autenticación, control de uso, integridad del sistema, confidencialidad, flujo de datos restringido, respuesta oportuna a eventos, disponibilidad de recursos); zonas y conduits; niveles de seguridad SL 1–4 con objetivo por zona (62443-3-2) | Segmentación y controles en los límites de zona | Los resúmenes proceden de ISA/IEC-blogs secundarios; verificar con la norma | https://gca.isa.org/blog/how-to-define-zones-and-conduits ; https://syc-se.iec.ch/deliveries/cybersecurity-guidelines/security-standards-and-best-practices/iec-62443/ | SOLO-SNIPPET |
| Claude Code: control del acceso MCP | `allowedMcpServers`/`deniedMcpServers`/`managed-mcp.json`; reglas deny/ask/allow; hooks PreToolUse; modo plan | Reglas deny con paréntesis para herramientas MCP se omiten en settings (usar `--disallowedTools`) según la doc de permisos | https://code.claude.com/docs/en/mcp ; https://code.claude.com/docs/en/permissions | VERIFICADO |

### Inferences (SÍNTESIS)
- Arquitectura mínima: el agente vive en la capa IT/analítica (réplica o capa de datos), **sin conexión directa a PLC/DCS**; lectura de historian vía réplica/API de solo lectura con cuenta de servicio de mínimo privilegio; CMMS con credencial de solo lectura; cualquier orden de trabajo se crea como **borrador** que un humano aprueba en el CMMS (no escritura autónoma).
- Aplicar a nivel de herramienta: lista blanca de tools MCP de lectura; deny para escrituras; hook PreToolUse que registre y bloquee métodos HTTP no GET en el servidor MCP; registro de cada consulta (quién, qué, cuándo).
- Nota de seguridad: la doc de Claude Code advierte inyección por servidores que traen contenido externo; los textos libres de OT (descripciones de OT en CMMS, comentarios de operadores) deben tratarse como datos no confiables.

### Gaps
- No pude verificar la guía de NIST SP 800-82r3, IEC 62443 ni las páginas de Microsoft en su fuente (403/ENOTFOUND); todo es snippet.
- No hay evidencia revisada de servidores MCP oficiales de IBM, SAP u OSIsoft/AVEVA; solo comunidad.
- Los directorios (mcpmarket, glama) son agregadores: no prueban la calidad ni la seguridad de los servidores.

---

## 5. Gobernanza de IA: NIST AI RMF, ISO/IEC 42001, OWASP Top 10 LLM

### Takeaway
OWASP Top 10 for LLM Applications 2025 incluye directamente los riesgos relevantes para un agente que recomienda mantenimiento: Prompt Injection, Excessive Agency, Misinformation, Data and Model Poisoning, Vector and Embedding Weaknesses. NIST AI RMF (GOVERN/MAP/MEASURE/MANAGE) y su Perfil GenAI (NIST AI 600-1) y ISO/IEC 42001 proveen la estructura de gestión. Todas estas fuentes quedaron SOLO-SNIPPET.

### Cited Findings
- OWASP Top 10 LLM 2025 (lista): LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM03 Supply Chain; LLM04 Data and Model Poisoning; LLM05 Improper Output Handling; LLM06 Excessive Agency; LLM07 System Prompt Leakage; LLM08 Vector and Embedding Weaknesses; LLM09 Misinformation; LLM10 Unbounded Consumption. LLM07 y LLM08 son novedades de 2025 — [resultado de búsqueda sobre genai.owasp.org](https://genai.owasp.org/llm-top-10/) (SOLO-SNIPPET; la página no pudo abrirse; ENOTFOUND). Mitigaciones típicas citadas por blogs: privilegio mínimo y aprobación humana para acciones de alto riesgo (fuente secundaria: https://kitemetric.com/blogs/owasp-top-10-llm-vulnerabilities-2025, NO usar como autoridad).
- NIST AI 600-1 (Perfil GenAI del AI RMF), publicado 2024-07-26 según un resumen secundario; mapea acciones a las funciones con prefijos GV, MP, MS, MG; cubre riesgos como confabulación, privacidad y ciberseguridad — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf (SOLO-SNIPPET; "doce áreas de riesgo y más de doscientas acciones" proviene de un artículo secundario, NO-VERIFICADO).
- ISO/IEC 42001:2023: requisitos para establecer, implementar, mantener y mejorar un sistema de gestión de IA; sigue la estructura armonizada ISO; Anexo A de controles — https://www.iso.org/standard/42001 (SOLO-SNIPPET). El conteo "38 controles en 9 objetivos" viene de una fuente académica secundaria: NO-VERIFICADO.

**Tabla riesgo → control → fuente** (los controles son síntesis mía salvo donde se indica documentación)
| Riesgo | Control propuesto | Fuente de respaldo | Estado de la fuente |
|---|---|---|---|
| Prompt injection directa/indirecta vía OT del CMMS, PDFs, correos | Tratar contenido recuperado como datos; separar planificador de ejecutor; allowlist de herramientas; sin ruta de datos no confiables hacia acciones privilegiadas | OWASP LLM01; patrones de diseño https://arxiv.org/abs/2506.08837; ataque https://arxiv.org/abs/2302.12173 | SOLO-SNIPPET (OWASP); VERIFICADO (papers) |
| Excessive Agency (el agente crea/cierra OT o cambia parámetros) | Herramientas de solo lectura por defecto; escritura solo como borrador; aprobación humana; deny/hook | OWASP LLM06; permisos y hooks https://code.claude.com/docs/en/permissions , /hooks | SOLO-SNIPPET (OWASP); VERIFICADO (Claude Code) |
| Misinformation / alucinación de causa raíz o intervalos | Citas obligatorias, verificación por fuente, abstención, juez + humano | OWASP LLM09; https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations ; ALCE; CoVe | SOLO-SNIPPET (OWASP); VERIFICADO (resto) |
| Data/Model Poisoning y memoria envenenada | Cuarentena, consenso, confianza + decaimiento, versionado y reversión de memoria | OWASP LLM04/LLM08; AgentPoison; MINJA; A-MemGuard; 2601.05504 | SOLO-SNIPPET (OWASP); VERIFICADO (papers) |
| Fuga de información sensible (datos de planta, contratos) | Mínimo privilegio de datos, filtrado de salida, retención definida de memoria | OWASP LLM02 | SOLO-SNIPPET |
| Cadena de suministro (servidores MCP/skills de terceros) | Aprobación de servidores, `allowedMcpServers`, revisión de código de MCP comunitarios, fijar versiones | OWASP LLM03; aviso de confianza en https://code.claude.com/docs/en/mcp ; aviso de skills en /skills | SOLO-SNIPPET (OWASP); VERIFICADO (Claude Code) |
| Consumo no acotado | `maxTurns`, cuotas, timeouts | OWASP LLM10; campo `maxTurns` en /sub-agents | SOLO-SNIPPET; VERIFICADO |
| Gobernanza del ciclo de vida de IA (roles, evaluación, mejora continua) | Mapear a GOVERN/MAP/MEASURE/MANAGE y a cláusulas de un AIMS | NIST AI RMF/AI 600-1; ISO/IEC 42001 | SOLO-SNIPPET |
| Riesgo OT: ruta IT→OT | Segmentación en zonas/conduits, sin acceso directo a control, cuentas de servicio mínimas | IEC 62443; NIST SP 800-82r3 | SOLO-SNIPPET |
| Acciones de mantenimiento con consecuencia de seguridad | Compuerta humana obligatoria con evidencia citada; clasificación de criticidad que fuerza revisión | Síntesis (no encontré norma que lo prescriba específicamente para agentes) | NO-VERIFICADO |

### Inferences (SÍNTESIS)
- Mantener un registro de riesgos del agente (MAP), métricas y pruebas continuas (MEASURE), políticas de aprobación y retiro/rollback (MANAGE) y roles (GOVERN) es consistente con las funciones del AI RMF; no afirmo cumplimiento de ISO 42001 por hacerlo.

### Gaps
- Textos normativos (OWASP descripciones, NIST AI 600-1, ISO 42001 cláusulas, IEC 62443 requisitos) no abiertos en fuente primaria. Las "versiones vigentes" a octubre de 2026 no se verificaron más allá del snippet: confirmar si OWASP publicó una edición posterior a 2025.
- Sin acceso al contenido de las acciones específicas de AI 600-1 aplicables a confabulación.

---

## 6. Intake: preguntas de aclaración, preguntar vs. asumir

### Takeaway
La literatura reciente encontrada (solo snippets) indica que los LLM reconocen ambigüedad pero rara vez preguntan, y que preguntar tiene un costo de seguridad (más superficie de inyección). No encontré fuente de ingeniería de requisitos leída; la política de intake propuesta es síntesis.

### Cited Findings
- Los modelos pueden reconocer ambigüedad cuando se les pide, pero con frecuencia responden directamente en vez de preguntar; el contexto recuperado agrava la brecha — https://arxiv.org/abs/2605.25284 (SOLO-SNIPPET).
- Diseño experimental bayesiano para elegir preguntas que reducen la ambigüedad — https://arxiv.org/abs/2502.04485 (SOLO-SNIPPET).
- Incertidumbre-consciente "preguntar o asumir" en agentes de código — https://arxiv.org/abs/2603.26233 (SOLO-SNIPPET).
- Buscar aclaración puede amplificar la vulnerabilidad a prompt injection (ASPI) — https://arxiv.org/abs/2605.17324 (SOLO-SNIPPET).
- τ-bench exige que el agente reúna información del usuario de forma incremental y siga reglas de dominio — https://arxiv.org/abs/2406.12045 (VERIFICADO).

### Inferences (SÍNTESIS, no documentada)
- Preguntar cuando: (a) faltan datos que cambian la decisión (activo/ubicación, modo de falla, condición de operación, ventana de datos, objetivo: RCA vs. intervalo vs. repuestos), (b) la acción propuesta es irreversible o tiene implicación de seguridad, (c) hay conflicto entre fuentes. Asumir (y declarar la suposición explícita en el reporte) cuando el costo del error es bajo y reversible.
- Preguntas de más valor (hipótesis a validar con usuarios): alcance y decisión que se tomará; activo y jerarquía exacta; periodo y calidad de datos (censura, reemplazos preventivos); definición de falla funcional; criterios de criticidad; restricciones (paradas, repuestos); nivel de evidencia requerido; destinatario del reporte.
- Limitar a 3–5 preguntas por turno, con opciones por defecto, y registrar las respuestas como datos del caso (no como memoria permanente hasta pasar compuertas).
- Dado ASPI, las respuestas del usuario y cualquier texto cargado deben pasar por el mismo tratamiento de datos no confiables.

### Gaps
- No leí fuentes de ingeniería de requisitos (p. ej. ISO/IEC/IEEE 29148, técnicas de entrevista de elicitación). NO-VERIFICADO.
- Los resultados de HF son títulos+resumen; no leí los papers.

---

## 7. Reportes técnicos de falla/confiabilidad, dashboards y reproducibilidad

### Takeaway
No pude verificar normas de reporte ACR/RCA ni guías de visualización de datos de ingeniería en esta sesión; lo único con fuente directa es la API de citas (Claude) y los principios de evaluación basada en trazas (MLflow, snippet). La estructura y reproducibilidad abajo es síntesis.

### Cited Findings
- Citations permite anclar cada afirmación del reporte a pasajes exactos — https://platform.claude.com/docs/en/build-with-claude/citations (VERIFICADO).
- MLflow permite evaluar trazas y datasets de evaluación versionados para pruebas repetibles — https://mlflow.org/docs/latest/genai/eval-monitor/ (SOLO-SNIPPET).
- ALCE define métricas de calidad de citas aplicables a reportes — https://arxiv.org/abs/2305.14627 (VERIFICADO).

### Inferences (SÍNTESIS)
- Estructura de reporte de falla: resumen ejecutivo; alcance y pregunta; descripción del evento y activo; línea de tiempo; datos y calidad (con censura declarada); análisis (modo de falla, causa raíz con método y nivel de evidencia); alternativas y recomendación con incertidumbre; acciones, responsables y fechas; limitaciones y suposiciones; anexo de fuentes (cada afirmación enlazada a `source_id`).
- Reproducibilidad: congelar versiones de datos (hash/snapshot de la consulta CMMS/historian con fecha), versión de código/prompt/skill (commit), versión de modelo, semillas para cualquier muestreo/bootstrapping, parámetros de ajuste (p. ej. Weibull), entorno (lockfile) y guardar la traza del agente; el reporte incluye un pie con estos identificadores. Los resultados numéricos deben calcularse con código determinista, no con el LLM.
- Dashboards: cada KPI con definición, fórmula, fuente y fecha de corte; el agente sugiere, el dashboard lo calcula con consultas versionadas.

### Gaps
- No encontré/verifiqué: estándar ACR (Análisis de Causa Raíz) formal, ISO 14224 (datos de confiabilidad), ISO 55000, ni guías de visualización. NO-VERIFICADO.
- No verifiqué guías de reproducibilidad de ML (p. ej. model cards, datasheets).

---

## Lista consolidada de lo no verificado

1. Fuentes primarias de normas: NIST AI RMF/AI 600-1 (texto), ISO/IEC 42001 (cláusulas y número de controles), IEC 62443 (requisitos), NIST SP 800-82r3 y existencia/estado de Rev. 4 draft (fecha 2026-09-21 solo en snippet), OWASP Top 10 LLM descripciones y posible edición posterior a 2025.
2. Documentación de MLflow, Mem0, Letta y LangGraph en su fuente (solo snippets).
3. Claude Agent SDK (docs) y herramienta de memoria de la API: no revisados.
4. Servidores MCP de Maximo/PI/Power BI: solo snippets de directorios comunitarios y de Microsoft; no se probó ninguno; SAP PM: no hay servidor encontrado.
5. Críticas a MemGPT (latencia, FIFO) y papers 2025–2026 de memoria (MemoryGraft, Zombie Agents, DREAM, MemAdapter, ASPI, abstención): solo títulos/resúmenes de una línea.
6. Fuentes de ingeniería de requisitos (preguntas de aclaración) y normas de reporte ACR/RCA y visualización: no consultadas.
7. Cualquier benchmark específico de agentes LLM en mantenimiento/confiabilidad: no hallado.
8. La eficacia de la política de compuertas propuesta (sec. 2) no está demostrada en la literatura leída: es hipótesis de diseño.
