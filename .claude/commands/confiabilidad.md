---
description: Lanza el equipo de confiabilidad (líder y especialistas) sobre tu solicitud
argument-hint: [activo, falla, datos o análisis que necesitas]
---
Atiende esta solicitud con el equipo de confiabilidad. Usa el agente `reliability-engineer` (líder) para clasificarla, hacer las preguntas
de intake que cambien la decisión (máximo 5, con opción por defecto), delegar en los especialistas que correspondan y entregar un informe
verificado por `reliability-evidence-verifier`.

Solicitud: $ARGUMENTS

Si la solicitud está vacía, muestra el catálogo de `docs/agentes/README.md` en una tabla corta (agente, para qué sirve, cuándo usarlo) y
pregunta qué quiere hacer la persona. Reglas del equipo: nunca inventar, nivel de evidencia en cada afirmación, cálculos con el kit
`tools/reliability`, sin nombres de empresas ni de plantas.
