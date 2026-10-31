# Resultado de la prueba en sesión nueva (2026-10-31)

Se abrieron dos sesiones nuevas en la nube con el repositorio recién clonado: DESPUÉS (rama `ccr-ab924d1a-kte866`, commit 99b5320 más la guía de la prueba) y ANTES (commit a2e17f8, sin CLAUDE.md, sin hooks y con el líder largo). Ninguna modificó archivos ni hizo commit, push o PR.

| Prueba | Resultado | Evidencia |
|---|---|---|
| A. Fichas nuevas se cargan | Pasó | El verificador, el FMECA y el líder respondieron 12 bloques; bloque 3 "OBJETIVO Y DECISIÓN", bloque 9 "CALIDAD" |
| B. CLAUDE.md llega a los subagentes | Pasó | El rankeador de citas respondió "HOWK RIOS - CONFIABILIDAD" y "LÍDER o ESTRATEGA" sin leer archivos |
| C. Hook de lenguaje | Pasó | El hook devolvió "Compuerta de lenguaje del equipo: término prohibido para el coordinador"; el mensaje lleva delante el prefijo del arnés "PostToolUse:Write hook blocking error" |
| D. Tokens del líder (3 corridas por sesión) | Bajó | Antes 39.554, 39.653 y 39.651 (media 39.619); después 33.167, 32.956 y 33.024 (media 33.049): 6.570 tokens menos por llamada, 16,6 % |

Límites de D: es una sola tarea simple, tres corridas por sesión (la variación entre corridas fue de 99 tokens antes y de 211 después) y mide el consumo del subagente líder, no el de una sesión de trabajo completa. Los especialistas con ficha de 12 bloques consumieron 8.800 a 10.100 tokens por llamada simple en la sesión DESPUÉS; no se midieron "antes", así que su efecto (fichas unos 500 a 770 bytes más largas) no está cuantificado.

Observaciones: todos los subagentes reportaron 1 uso de herramienta aunque se les pidió no leer archivos (no se identificó cuál); en la sesión ANTES las tres respuestas superaron el máximo de 12 líneas pedido.
