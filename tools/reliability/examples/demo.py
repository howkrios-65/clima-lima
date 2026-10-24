"""Demo con datos SINTÉTICOS (ILUSTRATIVOS, no medidos): muestra el flujo completo del kit.
Ejecutar desde tools/reliability:  python examples/demo.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reliability_kit import (compare_models, fit_weibull_mle, interpret_beta, kaplan_meier,
                             weibull_beta_ci_lr, weibull_bootstrap_ci)
from reliability_kit.economics import optimal_age_replacement

rng = np.random.default_rng(42)
life = 800 * rng.weibull(2.2, 40)          # vida verdadera simulada
stop = 900.0                               # fin de estudio => suspensiones
t, cens = np.minimum(life, stop), life > stop

fit = fit_weibull_mle(t, cens)
ci = weibull_beta_ci_lr(t, cens)
print(f"n={fit.n} fallas={fit.r} susp={fit.n_suspensions}  β={fit.beta:.2f} IC95%{tuple(round(x,2) for x in ci)}  η={fit.eta:.0f}")
print(interpret_beta(fit.beta, ci))
print("B10 con IC bootstrap:", {k: round(v, 2) if isinstance(v, float) else v
                                for k, v in weibull_bootstrap_ci(t, cens, stat="b_life", n_boot=500).items()})
print("AIC:", [(m["model"], round(m["delta_aic"], 1)) for m in compare_models(t, cens)])
print("KM mediana:", kaplan_meier(t, ~cens).median())
# Costos ILUSTRATIVOS: en un caso real son datos del usuario o un [VACÍO] declarado.
print(optimal_age_replacement(fit.beta, fit.eta, c_preventive=1.0, c_failure=8.0))
