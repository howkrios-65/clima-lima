# Plantilla: análisis de vida y confiabilidad estadística

| # | Sección | Regla |
|---|---|---|
| 1 | Pregunta de decisión | Una sola frase |
| 2 | Datos y calidad | n, fallas, porcentaje de censura, empates, unidad de tiempo, nulos |
| 3 | Elección del método | Reparable (MCF, NHPP) o no reparable (Weibull, Kaplan-Meier); varias unidades con fin de observación distinto: modelo multiunidad; modos separados o declarados mezclados |
| 4 | Ajustes | Modelos con AIC y veredicto de empate si ΔAIC < 2; β con intervalo; B-life con intervalo; bondad de ajuste aproximada y su baja potencia |
| 5 | Extrapolación | Prohibido decidir más allá de la mayor edad observada |
| 6 | Conclusión | Si el intervalo de β contiene 1 no se afirma desgaste; sin costos no hay edad óptima de reemplazo |
| 7 | Sensibilidad | Ventanas de observación, eventos duplicados, supuestos |
| 8 | Limitaciones y vacíos | Costos, definición de falla, modos, unidad de uso real |
| 9 | Reproducibilidad | Script, semilla, versiones |
