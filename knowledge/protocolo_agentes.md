# Protocolo de agentes: estructura, conexión y aprendizaje

Todos los agentes del equipo trabajan para una confiabilidad de clase mundial y comparten la misma estructura de instrucciones. Nada se inventa: lo que no tiene evidencia científica se deja con el comentario **SIN DATOS PARA ARMARLO** y el dato que lo cerraría.

## 1. Estructura de cada agente
Cada agente tiene una ficha con ocho bloques: **ROL** (quién es), **TAREA** (qué hace), **CONTEXTO** (qué recibe y de quién), **RAZONAMIENTO** (cómo decide), **CIERRE** (cuándo termina), **FEEDBACK** (qué reporta y a quién), **ALMACENAMIENTO** (qué guarda y dónde, memoria) y **SALIDA** (formato y destinatario).

## 2. El brief del líder
El líder no delega con frases sueltas: envía a cada agente un BRIEF con los mismos ocho campos, adaptados al caso: rol que asume, tarea concreta, archivos y reglas del contexto, razonamiento esperado, condiciones de cierre, a quién y qué reportar, dónde guardar y formato de la salida. Indica además qué hacen los demás agentes, para que cada uno sepa quién usará su entrega.

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
