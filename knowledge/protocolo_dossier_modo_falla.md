# Protocolo del dossier por modo de falla

La persona indica un modo de falla (por ejemplo, la chumacera de la polea de una faja transportadora) y el equipo investiga lo que se sabe
en el mundo sobre ESE modo de falla, con evidencia. Los datos de casos anteriores que la persona declaró ilustrativos no se usan como evidencia.

## Reglas
1. No se publica tabla, valor, referencia ni imagen sin su fuente en el registro de evidencia. Lo que no tiene fuente se declara VACÍO con su motivo.
2. Todo se registra en `Ledger`; las secciones se validan con `reliability_kit.dossier.validar_dossier` antes de entregar.
3. Los cálculos los hace el kit. Un parámetro de Weibull solo sale de datos citables; los costos para el punto óptimo los aporta la persona.
4. Videos, LinkedIn y redes sociales son pistas, nunca respaldo de una cifra. Una clase solo cuenta si se leyó su transcripción.
5. Todo cierre pregunta a la persona qué falta y guarda el caso en el historial si ella lo permite.

## Secciones (catálogo en `dossier.SECCIONES`)
| Sección | Frente que la investiga | Agente |
|---|---|---|
| Mediciones y curvas; Diagnóstico y troubleshooting | monitoreo | `reliability-literature-researcher` |
| Fenómenos físicos; Vida útil y obsolescencia | mecanismo | `reliability-literature-researcher` |
| Top de fallas; FMECA y RCM; Causa raíz | modos | `reliability-literature-researcher` + `reliability-fmeca-rcm` + `reliability-rca-investigator` |
| Confiabilidad (Weibull y vida) | datos | `reliability-dataset-scout` + `reliability-life-analyst` |
| Punto óptimo; Costo-riesgo y LCC | economía | `reliability-economics-kpi` (con costos aportados) |
| Inspección basada en riesgo; Mantenimiento predictivo y normas; Referencias | normas | `reliability-standards-researcher` |
| Modelos de aprendizaje automático y profundo | ml | `reliability-literature-researcher` + `reliability-predictive-analyst` |

## Flujo del orquestador (el líder)
1. Intake y búsqueda de recurrencia en el historial (`reliability-case-historian`).
2. Reparte la cuota del conector por frente y lanza en paralelo un investigador por frente, cada uno con su rango de ids.
3. Integra: especialistas analizan lo hallado (FMECA, Weibull con datos citables, punto óptimo con costos de la persona, predictivo).
4. Arma el dossier y lo valida; el redactor genera el informe HTML (`report_html`) con las secciones; el verificador intenta refutarlo.
5. Historiador guarda; curador propone lecciones; el líder pregunta lo que falte.
