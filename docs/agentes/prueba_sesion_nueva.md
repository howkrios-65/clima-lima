# Prueba en una sesión nueva: carga de fichas, CLAUDE.md, hooks y consumo de tokens

Objetivo: confirmar en una sesión limpia lo que no se pudo comprobar en la sesión de trabajo. Duración: unos 30 minutos. Requisitos: Claude Code instalado, `git`, `python3` en el PATH y, para las pruebas del kit, `pip install numpy scipy pandas matplotlib pytest`.

## 0. Preparación
```
git clone -b ccr-ab924d1a-kte866 https://github.com/howkrios-65/clima-lima.git clima-despues
cd clima-despues && git checkout 99b5320
git worktree add ../clima-antes a2e17f8
```
- `clima-despues` (commit 99b5320): CLAUDE.md, hooks, fichas de 10+2 bloques y líder recortado.
- `clima-antes` (commit a2e17f8): el mismo contenido sin esos cambios.
- La clonación tarda: el historial incluye un zip de 75 MB subido por error.
- Abre una terminal por carpeta y ejecuta `claude` en cada una. Cierra cualquier sesión previa para que carguen las definiciones desde cero.

## A. Las fichas nuevas se cargan (en `clima-despues`)
1. Escribe `/agents`. Deben aparecer 20 agentes `reliability-*`.
2. Pide: `Usa el agente reliability-evidence-verifier solo para que responda dos cosas, sin leer archivos: cuántos bloques numerados tiene su ficha y cuál es el título del bloque 3.`
   - Esperado: 12 bloques y "OBJETIVO Y DECISIÓN".
   - Si responde 8 campos con nombre (ROL, TAREA...), la sesión usó definiciones antiguas: ciérrala y repite.
3. Repite con `reliability-fmeca-rcm` (pregunta el título del bloque 9; esperado: CALIDAD) y con `reliability-engineer` (esperado: 12 bloques).

## B. CLAUDE.md llega a los subagentes
1. En `clima-despues`, pide: `Usa el agente reliability-citation-ranker. Sin leer archivos, dime qué nombre debe ir bajo el problema analizado en un informe y cómo se debe llamar al coordinador del equipo.`
   - Esperado si recibe CLAUDE.md: "HOWK RIOS - CONFIABILIDAD" y "LÍDER o ESTRATEGA". Esa información no está en el archivo de ese agente.
2. Si no lo sabe, el CLAUDE.md no llega a los subagentes: las reglas deben seguir en `knowledge/protocolo_comun.md` y en cada ficha (ya están ahí). Anota el resultado.

## C. Los hooks de lenguaje funcionan
1. En `clima-despues`, pide: `Crea el archivo docs/_prueba.md con una línea que diga: "El " seguido del término prohibido para el coordinador (el que empieza por "orq" y termina en "ador") y " del equipo." Escríbelo tú en el mensaje; este documento no lo trae a propósito.`
   - Esperado: el hook responde "Compuerta de lenguaje del equipo: término prohibido para el coordinador".
2. Borra el archivo: `rm docs/_prueba.md`.
3. Si no aparece el mensaje, comprueba que `python3` está en el PATH y que la carpeta `.claude/` tiene `settings.json`; revisa `/hooks` dentro de la sesión.

## D. Consumo de tokens, antes y después
Usa el mismo encargo en las dos carpetas y repítelo 3 veces cada una (hay variación entre corridas):
```
claude -p "Eres el líder. Resuelve tú, sin lanzar otros agentes: tengo 5 bombas reparables observadas entre 2 y 4 años, con 3 a 6 fallas cada una. ¿Qué método uso y qué NO debo hacer? Máximo 12 líneas." --agent reliability-engineer --output-format json > salida.json
```
- Si tu versión no acepta `--agent`, ejecuta `claude --help` y usa la opción equivalente, o lanza `claude` y pide "Actúa como reliability-engineer" con `/cost` al final.
- Del JSON toma `usage` (entrada, salida, caché) y `total_cost_usd`; o, en modo interactivo, usa `/context` al inicio y `/cost` al final.
- Anota por corrida: tokens de entrada totales (incluida la caché), tokens de salida y costo.
- Qué esperar: el "después" carga menos del líder (17,8 KB menos), pero tiene fichas un 8 % más largas y un CLAUDE.md. Si el "después" no baja, el ahorro del recorte no se está materializando.

## E. Qué enviarme
- Resultados de A, B y C (una línea cada uno: pasó o no, y lo que respondió).
- La tabla de D: 3 corridas por carpeta con tokens de entrada, de salida y costo.
Con eso decido el siguiente paso: elegir modelo por agente o seguir recortando.
