"""reliability_kit: cálculos de confiabilidad reproducibles.

Principio rector: ninguna función inventa datos. Cada resultado devuelve n, método y
advertencias; lo que no se puede calcular honestamente se rechaza con ValueError.
"""
from .weibull import (WeibullFit, fit_weibull_mle, weibull_beta_ci_lr, weibull_bootstrap_ci,
                      rank_regression, compare_models, compare_models_verdict, aic_support, interpret_beta,
                      weibull_b_life, weibull_b_life_ci_lr, bias_correct_beta, gof_censored_bootstrap)
from .nhpp import (CrowAmsaaFit, MultiCrowAmsaaFit, fit_crow_amsaa, fit_crow_amsaa_multi, laplace_trend_test,
                   laplace_trend_test_multi, unit_heterogeneity_test, crow_amsaa_gof_mc, mean_cumulative_function)
from .survival import kaplan_meier, logrank_test, km_failure_quantile
from .workorders import pareto, bad_actors, chronic_repeaters
from .data_quality import audit, audit_recurrent
from .economics import (age_replacement_cost_rate, optimal_age_replacement, npv, eac,
                        inherent_availability)
from .mlcheck import (temporal_split, group_split, assert_no_overlap, pr_metrics,
                      recall_at_precision, brier_and_calibration, cost_optimal_threshold)

__version__ = "0.1.0"
