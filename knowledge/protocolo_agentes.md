# Protocolo de agentes: estructura, conexión y aprendizaje

Todos los agentes del equipo trabajan para una confiabilidad de clase mundial y comparten la misma estructura de instrucciones. Nada se inventa: lo que no tiene evidencia científica se deja con el comentario **SIN DATOS PARA ARMARLO** y el dato que lo cerraría.

## 1. Estructura de cada agente
La ficha de cada agente tiene **10 bloques fijos y 2 operativos**. Los bloques son los mismos que usa el BRIEF del líder (sección 2), de modo que lo estable vive en el archivo del agente y lo propio de cada caso llega en el BRIEF.
| # | Bloque | Qué contiene en el archivo del agente |
|---|---|---|
| 1 | Rol y nivel | Perfil que asume y profundidad |
| 2 | Contexto | De quién recibe y qué conoce del equipo |
| 3 | Objetivo y decisión | Qué decisión o entrega sirve su trabajo |
| 4 | Insumos | Qué necesita y qué calidad mínima; si falta, lo dice y no rellena |
| 5 | Tarea | Verbos, alcance y lo que queda fuera |
| 6 | Método y estándares | Norma o método, con estado de verificación |
| 7 | Honestidad | Una línea a `protocolo_comun.md` más lo propio del agente |
| 8 | Formato de salida | Archivo, estructura y destinatario |
| 9 | Calidad | Qué autoverifica antes de entregar |
| 10 | Restricciones y dudas | Qué hace ante vacíos: preguntar (máximo 5) o asumir y declarar |
| 11 | Feedback (operativo) | Qué reporta al líder para que el equipo aprenda |
| 12 | Almacenamiento (operativo) | Qué guarda y dónde |

## 2. El brief del líder
El líder no delega con frases sueltas: cada encargo usa esta plantilla, adaptada al caso. Se omite lo que ya dice el archivo del agente y se cita `protocolo_comun.md` en lugar de repetir las reglas.
```
1 ROL Y NIVEL:      perfil y profundidad (solo si cambia respecto del archivo del agente)
2 CONTEXTO:         caso, activo o modo de falla, versión del dossier, qué hicieron los demás agentes
3 OBJETIVO:         qué decisión o entrega sirve esto y quién la usará
4 INSUMOS:          rutas exactas de archivos y su calidad (leídos, solo pista, sin datos); acceso real de red
5 TAREA:            verbos, alcance y lo que queda fuera; rango de ids si aplica
6 MÉTODO:           norma o método; moldes de formato a copiar (ruta)
7 HONESTIDAD:       "reglas de protocolo_comun" + lo específico del caso (por ejemplo, ids que no respaldan)
8 FORMATO:          rutas de salida, archivos JSON y si el agente puede escribir o devuelve el contenido en el mensaje
9 CALIDAD:          qué debe autoverificar (literalidad del extracto, ids existentes, sin cifras sin fuente)
10 RESTRICCIONES:   plazo, confidencialidad y qué hacer si falta información
```
Indica además qué hacen los demás agentes, para que cada uno sepa quién usará su entrega. Una regla práctica: si el agente no tiene la herramienta Write, el campo 8 debe pedir el contenido en el mensaje final.

## 3. Conexión entre agentes
| De | A | Qué entrega |
|---|---|---|
| Historiador | Líder | Casos parecidos y línea base |
| Investigadores y lectores de papers | Replicador, analistas | Entradas de evidencia, cifras |
| Replicador | Integrador | Réplicas validadas |
| Analistas (causa raíz, FMECA, vida, predictivo, economía) | Integrador | JSON de análisis con ids de evidencia |
| Integrador | Verificador y diseñador UX | HTML ensamblado |
| Verificador | Líder | Problemas por severidad |
| Líder | Agente de feedback y curador | Lo aprendido en la ronda |

## 4. Aprendizaje
Después de cada ronda el líder envía a cada agente lo que se aprendió de su entrega y pide al agente de feedback que lo registre. Las reglas de la persona se aplican de inmediato; las lecciones pasan por la cuarentena y solo una persona las aprueba.

## 5. Almacenamiento y memoria
Carpeta del caso: `historial/dossiers/<modo_de_falla>/` (evidencia, dossier, análisis, cifras, réplicas, trazabilidad, informe). Feedback: `historial/feedback/feedback.jsonl`. Lecciones candidatas: `knowledge/memoria/cuarentena/`. Si el repositorio es compartido se pide permiso antes de subir.

## 6. Condiciones de cierre del trabajo
Dossier validado, verificación independiente sin bloqueos, ajustes automáticos revisados, HTML sin errores, enlaces clicables, y preguntas finales a la persona.

## 7. Modelo por agente
Los 16 agentes de juicio (líder, auditor, vida, causa raíz, FMECA, predictivo, economía, verificador, literatura, datos, normas, analista de papers, redactor, integrador, feedback y diseño) heredan el modelo de la sesión. Cuatro agentes mecánicos usan el modelo ligero: historiador, curador de memoria, rankeador de citas y replicador. Pasaron una prueba con errores sembrados (rechazar cifras que no están literales en el extracto, no inventar citas ni cuartiles, no promover memoria sin persona, declarar línea base VACÍO). Es una prueba pequeña, no una medición de tokens ni de calidad en casos reales: se revisa con la prueba en sesión nueva (`docs/agentes/prueba_sesion_nueva.md`), y volver a heredar es cambiar una línea del archivo del agente.
