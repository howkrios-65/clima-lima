# reliability_kit

Cálculos de confiabilidad **reproducibles y probados** para el agente `reliability-engineer`
(`.claude/agents/reliability-engineer.md`). Principio: el agente no calcula "de cabeza"; ejecuta
este código y reporta n, método, intervalos y advertencias.

## Instalación y pruebas

```bash
cd tools/reliability
pip install -r requirements.txt
python -m pytest -q          # 152 pruebas (~25 s): kit, correcciones y reglas del equipo de agentes
python examples/demo.py      # flujo completo con datos sintéticos (ILUSTRATIVOS)
```

## Módulos

| Módulo | Qué hace | Cuándo (árbol sec. 5.1 de `knowledge/metodos_lider.md`) |
|---|---|---|
| `weibull` | MLE 2P con censura por derecha; IC de β y de **B-life por razón de verosimilitud**; IC bootstrap; **corrección de sesgo de β** (`bias_correct_beta`); rangos de Johnson/Bernard + RRX; Weibull/lognormal/exponencial por AIC con **veredicto de empate** (`compare_models_verdict`); **bondad de ajuste con censura** (`gof_censored_bootstrap`, aproximada); `interpret_beta` que respeta el IC. Avisos de sesgo con r<30 y de censura >50 % | Ítems **no reparables** (un modo de falla por ajuste) |
| `nhpp` | Crow-AMSAA de una unidad (β insesgado, IC exacto χ²) y **multi-unidad con T_k distintos** (`fit_crow_amsaa_multi`: modelo condicional o λ común), Laplace de una unidad y **agrupada**, **prueba de heterogeneidad entre unidades**, GOF Cramér-von Mises MC, **MCF con IC de Lawless-Nadeau** | Ítems **reparables** con posible tendencia |
| `survival` | Kaplan-Meier (Greenwood, IC log-log), mediana, **cuantil de falla B_p con IC** (`km_failure_quantile`), log-rank de 2 grupos | Comparar flotas/proveedores; sin supuesto paramétrico |
| `workorders` | Pareto (con *vital few*), bad actors cruzando frecuencia/costo/downtime, crónicos (mismo código repetido en ventana) | Priorización desde el historial de órdenes de trabajo |
| `data_quality` | `audit`: nulos, duplicados, fechas inválidas, campos críticos. `audit_recurrent`: eventos recurrentes (unidades sin fin de observación, eventos posteriores al fin, eventos simultáneos, censura atípica, unidades en riesgo por edad) | Siempre, **antes** de cualquier número |
| `economics` | Costo por edad de reemplazo (Barlow-Proschan), edad óptima (se **niega** si β≤1 o c_f≤c_p), VPN, CAE/EAC, disponibilidad inherente | Decisiones; los costos son parámetros obligatorios |
| `mlcheck` | Partición temporal y por activo, detector de fuga, AP/PR, recall@precisión, Brier/calibración, umbral por costo | Validación de modelos predictivos |
| `plots` | Probabilidad Weibull, Pareto, Kaplan-Meier (matplotlib, acento + gris, n en el pie) | Entregables |

CLI: `python -m reliability_kit weibull datos.csv --time t --censored c` (incluye IC de B10, corrección de
sesgo si r<30 y veredicto de modelos) · `crow-amsaa datos.csv --time t --T 5000` (una unidad) ·
`crow-amsaa datos.csv --time t --unit motor --end fin_obs` (varias unidades; sin `--unit`, la CLI **advierte**
si el CSV tiene una columna que parece identificar unidades) · `pareto datos.csv --group activo [--value costo]`.

## Cómo están verificadas

Las pruebas no se limitan a "el código corre":
- **Contra referencias independientes**: MLE completo vs `scipy.stats.weibull_min.fit`; MLE censurado vs maximización directa de la verosimilitud; KM, log-rank, MCF, rangos de Johnson, VPN/CAE y Pareto contra cálculos a mano.
- **Propiedades estadísticas por simulación (semilla fija)**: cobertura del IC de β (LR, Crow-AMSAA, KM) dentro de ~91–99 % para nominal 95 %; insesgamiento del β de Crow-AMSAA y sesgo al alza del MLE; tamaño de la prueba de Laplace; potencia para detectar tendencia.
- **Honestidad**: IC que contiene 1 → no se afirma tendencia; sin mínimo interior → no se inventa una edad óptima; <10 fallas → advertencia de resultado exploratorio.

## Límites conocidos (declarados, no ocultos)

- Weibull 2P solamente (sin γ de 3 parámetros ni mezclas); un modo de falla por ajuste.
- `gof_censored_bootstrap` es una prueba **aproximada** (distancia KM–modelo con censura remuestreada) y de
  baja potencia con pocas fallas; un p alto no valida el modelo. `bias_correct_beta` asume un horizonte de
  censura (se devuelve en `assumption`): es indicativa si el diseño real difiere.
- La MCF multiunidad no es fiable en la cola con pocas unidades en riesgo (`n_at_risk` se devuelve para verlo).
- `unit_heterogeneity_test` contrasta tasa común entre unidades (X² de conteos con p Monte Carlo); con β≠1 y
  T_k desiguales puede rechazar por la tendencia y no por heterogeneidad real.
- Cox PH y riesgos competitivos no incluidos (usar `lifelines`); AIC compara modelos pero no valida ninguno.
- El kit calcula; **los costos, la definición de falla y la separación de modos los aporta el usuario**. Sin
  ellos, el resultado correcto es un [VACÍO] declarado.

## Historial de correcciones

Prueba con datos reales (Meeker & Escobar vía R `survival`: `genfan`, `valveSeat`) → el agente tuvo que
improvisar lo siguiente, ahora incluido y probado: Crow-AMSAA multi-unidad (+ CLI con `--unit/--end` y aviso),
IC de la MCF, IC de B10 (LR y Kaplan-Meier), advertencia de sesgo/censura, corrección de sesgo, veredicto de
ΔAIC<2 como empate y bondad de ajuste con censura. Cobertura de los nuevos IC y tamaño de las nuevas pruebas
verificados por simulación en `tests/test_fixes.py`. Un error propio detectado por esas pruebas: las bandas del
cuantil de Kaplan-Meier estaban invertidas (corregido).

## Evidencia, señales, historial e informe HTML
- `evidence`: registro de fuentes (`Ledger`); el nivel se deriva del acceso y exige extracto literal.
- `signals`: línea base robusta, primera alarma, CUSUM, tendencia (Mann-Kendall y Sen), correlación y comparación de periodos.
- `case_store`: historial de casos, recurrencia y líneas base versionadas (`historial/`, fuera de git por defecto).
- `report_html.construir_informe(caso, ledger, salida)`: informe HTML autocontenido con compuertas de evidencia, Weibull en el navegador
  con autoprueba contra este kit, detección retrospectiva con controles y matriz de convergencia que muestra fuentes de información distintas.
- `ensamblar(carpeta)`: arma el informe de un modo de falla desde `evidencia.json`, `dossier.json` y `analisis/*.json` con todas las compuertas.
