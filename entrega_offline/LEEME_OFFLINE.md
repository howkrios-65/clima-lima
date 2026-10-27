# Equipo de confiabilidad: copia completa para uso sin conexión

Fecha de la copia: 2026-10-27. Autor: HOWK RIOS - CONFIABILIDAD.

## Qué hay en este zip
| Carpeta | Contenido |
|---|---|
| `repo/` | El repositorio completo (con `.git` y su historial). Rama de trabajo: `ccr-ab924d1a-kte866`. |
| `repo/.claude/agents/` | Los 20 agentes (cada uno es un archivo de texto con su ficha de ocho bloques). |
| `repo/.claude/commands/` | Los comandos `/confiabilidad` y `/modo-de-falla`. |
| `repo/knowledge/` | Protocolos, registro de normas, referencia de ML y reglas. |
| `repo/tools/reliability/` | El kit de cálculo en Python (Weibull, Kaplan-Meier, Crow-AMSAA, economía, informe HTML) y sus 152 pruebas. |
| `repo/historial/dossiers/` | Los tres casos: `chumacera_polea_faja`, `bomba_centrifuga`, `bomba_prensaestopa_rodamientos` (informe.html, evidencia.json, dossier.json, analisis/*, cifras, normas, abstract, trazabilidad). |
| `repo/historial/feedback/feedback.jsonl` | Reglas y correcciones aprendidas (candidatas en cuarentena). |
| `repo/docs/agentes/` | Mapas interactivos de agentes (HTML), guía de comandos y README. |
| `repo/docs/entregables/` | Las tres presentaciones (.pptx) y los scripts que las generan. |
| `trabajo_intermedio/` | Archivos de trabajo de la sesión: registros de evidencia por frente, análisis de cada versión, scripts de ensamblado de cada caso (`modo_chumacera`, `modo_bomba`, `modo_prensa`), generadores de mapas y presentaciones, capturas de verificación. No incluye las descargas de conjuntos de datos públicos ni `node_modules`. |

## Dónde quedó guardado
1. Este zip: `entrega_offline/clima_lima_offline.zip` dentro del repositorio de la sesión (`/home/user/clima-lima/entrega_offline/`) y subido a la rama `ccr-ab924d1a-kte866` del repositorio `howkrios-65/clima-lima` en GitHub.
2. El repositorio completo, sin el zip, está en esa misma rama de GitHub. Con conexión, `git clone` y `git checkout ccr-ab924d1a-kte866`.
3. El informe del caso de la chumacera y el de la bomba con prensaestopa están publicados como artefactos privados (enlaces en la conversación). Cópialos aparte: dependen de tu cuenta.

## Qué funciona sin conexión
- Abrir cualquier `.html` con el navegador: informes (`repo/historial/dossiers/*/informe.html`) y mapas (`repo/docs/agentes/*.html`). Son un solo archivo. Los informes cargan una fuente de Google Fonts si hay conexión; sin ella usan una de reserva.
- Abrir las presentaciones `.pptx` con PowerPoint o LibreOffice.
- El kit de cálculo:
  ```
  cd repo/tools/reliability
  python -m venv .venv && source .venv/bin/activate      # en Windows: .venv\Scripts\activate
  pip install numpy scipy pandas matplotlib pytest        # una sola vez, requiere conexión; después queda local
  python -m pytest -q                                     # deben pasar 152 pruebas
  ```
  Con tus datos (tabla de rodamientos instalados, fechas, horas, motivo de salida) puedes usar `reliability_kit` desde Python: `fit_weibull_mle`, `kaplan_meier`, `logrank_test`, `fit_crow_amsaa`, `pareto`, `audit`, funciones de `economics.py`. El auditor de datos dejó la plantilla de columnas en el informe del caso de prensaestopa (pestaña Datos).
- Regenerar un informe a partir de sus JSON: los scripts `trabajo_intermedio/modo_*/build_*.py` usan rutas absolutas de la sesión (`/tmp/claude-0/.../scratchpad/` y `/home/user/clima-lima/`). Cambia esas rutas a las de tu equipo (están en las primeras líneas) y ejecútalos con `python`.
- Regenerar las presentaciones: instala Node.js y `npm install pptxgenjs`; los scripts están en `repo/docs/entregables/*_build.js` (hacen falta además las funciones auxiliares de la sesión; para cambios pequeños es más sencillo editar el `.pptx`).

## Qué NO funciona sin conexión ni saldo
- Los agentes son instrucciones en texto que ejecuta un modelo de lenguaje. Sin acceso a un modelo no se pueden lanzar `/confiabilidad` ni `/modo-de-falla`, ni hacer búsquedas bibliográficas.
- Lo que sí puedes hacer: abrir los archivos `.claude/agents/*.md` y `.claude/commands/*.md`, copiarlos a cualquier otro asistente de IA que tengas disponible y pegarle el contexto. No lo he probado con otros modelos y no puedo garantizar que respeten las compuertas de evidencia.
- Las compuertas de evidencia sí son código del kit (`reliability_kit/report_html.py`, `replicas.py`, `dossier.py`): siguen funcionando sin conexión al armar un informe con tus propios JSON.

## Para continuar cuando vuelvas a tener acceso
1. Instala Claude Code y abre la carpeta `repo/` (ya trae `.claude/agents` y `.claude/commands`).
2. Usa `/modo-de-falla <la falla>` para un caso nuevo o `/confiabilidad <solicitud>` para el análisis con tus datos.
3. Lo pendiente de los casos: habilitar el acceso a revistas, repositorios y fabricantes; el cupo de Wiley se renueva el 2026-11-01; aportar PDF de tesis y artículos, el historial de fallas con ajuste del prensaestopa y fuga con fecha, y los costos.

## Estado honesto de lo entregado
- Lo propio del prensaestopa, de la cavitación y de los sellos quedó como SIN DATOS PARA ARMARLO o como pista de buscador, porque no se pudo leer la literatura. Ninguna pista respalda una afirmación.
- Los análisis son de escritorio: sin datos del activo no se confirma ninguna causa ni se puntúa el FMECA.
- Las normas se vieron en resúmenes de buscador: edición no verificada.

## Nota sobre la conversación
El registro completo de la conversación (51 MB) no se incluye en el zip que va a GitHub, porque puede contener rutas, enlaces y datos de la sesión. Si lo quieres, pídelo por separado y se entrega solo a ti.
