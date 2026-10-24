# reliability_kit

Cálculos de confiabilidad **reproducibles y probados** para el agente `reliability-engineer`
(`.claude/agents/reliability-engineer.md`). Principio: el agente no calcula "de cabeza"; ejecuta
este código y reporta n, método, intervalos y advertencias.

## Instalación y pruebas

```bash
cd tools/reliability
pip install -r requirements.txt
python -m pytest -q          # 64 pruebas
python examples/demo.py      # flujo completo con datos sintéticos (ILUSTRATIVOS)
```

## Módulos

| Módulo | Qué hace | Cuándo (árbol §5.1 del agente) |
|---|---|---|
| `weibull` | MLE 2P con censura por derecha, IC de β por razón de verosimilitud, IC bootstrap (β, η, B-life, MTTF), rangos de Johnson/Bernard + regresión RRX, comparación Weibull/lognormal/exponencial por AIC, `interpret_beta` que respeta el IC | Ítems **no reparables** (un modo de falla por ajuste) |
| `nhpp` | Crow-AMSAA (β insesgado, IC exacto χ²; terminación por tiempo o por falla), prueba de Laplace, GOF Cramér-von Mises con p-valor Monte Carlo, MCF (Nelson) multiunidad con censura | Ítems **reparables** con posible tendencia |
| `survival` | Kaplan-Meier (Greenwood, IC log-log), mediana, log-rank de 2 grupos | Comparar flotas/proveedores; sin supuesto paramétrico |
| `workorders` | Pareto (con *vital few*), bad actors cruzando frecuencia/costo/downtime, crónicos (mismo código repetido en ventana) | Priorización desde CMMS/SAP |
| `data_quality` | Perfil de nulos, duplicados, fechas inválidas/invertidas, banderas de campos críticos | Siempre, **antes** de cualquier número |
| `economics` | Costo por edad de reemplazo (Barlow-Proschan), edad óptima (se **niega** si β≤1 o c_f≤c_p), VPN, CAE/EAC, disponibilidad inherente | Decisiones; los costos son parámetros obligatorios |
| `mlcheck` | Partición temporal y por activo, detector de fuga, AP/PR, recall@precisión, Brier/calibración, umbral por costo | Validación de modelos predictivos |
| `plots` | Probabilidad Weibull, Pareto, Kaplan-Meier (matplotlib, acento + gris, n en el pie) | Entregables |

CLI: `python -m reliability_kit weibull datos.csv --time t --censored c` ·
`crow-amsaa datos.csv --time t --T 5000` · `pareto datos.csv --group activo [--value costo]`.

## Cómo están verificadas

Las pruebas no se limitan a "el código corre":
- **Contra referencias independientes**: MLE completo vs `scipy.stats.weibull_min.fit`; MLE censurado vs maximización directa de la verosimilitud; KM, log-rank, MCF, rangos de Johnson, VPN/CAE y Pareto contra cálculos a mano.
- **Propiedades estadísticas por simulación (semilla fija)**: cobertura del IC de β (LR, Crow-AMSAA, KM) dentro de ~91–99 % para nominal 95 %; insesgamiento del β de Crow-AMSAA y sesgo al alza del MLE; tamaño de la prueba de Laplace; potencia para detectar tendencia.
- **Honestidad**: IC que contiene 1 → no se afirma tendencia; sin mínimo interior → no se inventa una edad óptima; <10 fallas → advertencia de resultado exploratorio.

## Límites conocidos (declarados, no ocultos)

- Weibull 2P solamente (sin γ de 3 parámetros ni mezclas); un modo de falla por ajuste.
- MCF sin intervalos de confianza (falta el estimador de varianza de Lawless-Nadeau).
- Cox PH y riesgos competitivos no incluidos (usar `lifelines`); AIC compara modelos pero no sustituye una prueba de bondad de ajuste formal.
- El kit calcula; **los costos, la definición de falla y la separación de modos los aporta el usuario**. Sin ellos, el resultado correcto es un [VACÍO] declarado.
