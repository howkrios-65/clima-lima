# Plantilla: modelo de mantenimiento predictivo

| # | Sección | Regla |
|---|---|---|
| 1 | Decisión y acción | Qué dispara cada alerta y con qué tiempo de reacción |
| 2 | Datos y etiquetado | Definición de falla, horizonte, tratamiento de la censura |
| 3 | Baselines | Umbral, tendencia, supervivencia clásica, bosque aleatorio. Un modelo profundo que no los supere no se recomienda |
| 4 | Partición | Por activo y temporal; preprocesamiento ajustado solo con entrenamiento |
| 5 | Métricas | Varias, con subconjunto, truncado y punto de evaluación; en anomalías por evento y falsas alarmas por activo-mes |
| 6 | Calibración e incertidumbre | Brier y curva de calibración; cobertura empírica de los intervalos por activo |
| 7 | Robustez y deriva | Faltantes, ruido, criterio de reentrenamiento con aprobación humana |
| 8 | Rótulo | "Exploratorio" si las fallas por modo no alcanzan el mínimo; piloto en sombra antes de actuar |
| 9 | Veredicto | Recomendado o no recomendado frente al baseline, con su incertidumbre |
