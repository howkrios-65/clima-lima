import numpy as np
import pytest
from scipy import stats

from reliability_kit import signals as S


def test_baseline_is_robust_to_outliers():
    x = np.r_[np.random.default_rng(0).normal(10, 1, 30), 500.0]
    lb = S.linea_base(x, 31)
    assert lb["mediana"] == pytest.approx(10, abs=0.6) and lb["sigma"] < 2          # el valor 500 no la arrastra
    with pytest.raises(ValueError):
        S.linea_base([1, 2, 3], 3)


def test_first_crossing_with_persistence():
    x = [1, 1, 9, 1, 9, 9, 9, 1]
    assert S.primer_cruce(x, 5) == 2 and S.primer_cruce(x, 5, 2) == 4 and S.primer_cruce(x, 99) is None
    assert S.primer_cruce([1, np.nan, 9], 5) == 2


def test_cusum_detects_step_and_stays_quiet_otherwise():
    rng = np.random.default_rng(1)
    quiet = rng.normal(0, 1, 200)
    assert S.cusum_primera_alarma(quiet, 0, 1, k=0.5, h=8) is None
    x = np.r_[rng.normal(0, 1, 60), rng.normal(2, 1, 40)]
    i = S.cusum_primera_alarma(x, 0, 1)
    assert i is not None and 60 <= i <= 75


def test_mann_kendall_matches_scipy_and_sen_slope_exact_on_line():
    rng = np.random.default_rng(2)
    x = np.arange(60) * 0.5 + rng.normal(0, 3, 60)
    r = S.mann_kendall(x)
    tau, p = stats.kendalltau(np.arange(60), x)
    assert r["tau"] == pytest.approx(tau, abs=1e-9)
    assert r["p_value"] == pytest.approx(p, abs=0.01)
    assert S.mann_kendall(np.arange(30) * 2.0)["pendiente_sen"] == pytest.approx(2.0)
    assert S.mann_kendall(np.zeros(20))["p_value"] == 1.0
    assert S.mann_kendall(np.cumsum(rng.normal(size=80)))["aviso"] is not None       # random walk: autocorrelada


def test_mann_kendall_needs_enough_points():
    with pytest.raises(ValueError):
        S.mann_kendall([1, 2, 3])


def test_spearman_bootstrap_matches_scipy_and_ci_brackets():
    rng = np.random.default_rng(3)
    x = rng.normal(size=120)
    y = 0.7 * x + rng.normal(size=120)
    r = S.spearman_bootstrap(x, y, n_boot=1500, seed=9)
    assert r["rho"] == pytest.approx(stats.spearmanr(x, y)[0])
    pearson = 0.7 / np.sqrt(0.7 ** 2 + 1)                 # correlación poblacional del modelo
    spearman_pob = 6 / np.pi * np.arcsin(pearson / 2)       # relación exacta para una normal bivariada
    assert r["ic"][0] < r["rho"] < r["ic"][1] and r["ic"][0] < spearman_pob < r["ic"][1]
    assert S.spearman_bootstrap(x, y, n_boot=300, seed=9) == S.spearman_bootstrap(x, y, n_boot=300, seed=9)
    with pytest.raises(ValueError):
        S.spearman_bootstrap([1, 2], [1, 2])


def test_compare_periods_recovers_shift_and_matches_scipy():
    rng = np.random.default_rng(4)
    a, b = rng.normal(100, 5, 60), rng.normal(110, 5, 40)
    r = S.comparar_periodos(a, b, n_boot=1000)
    assert r["desplazamiento_hl"] == pytest.approx(10, abs=2.5)
    assert r["rango_biserial"] > 0.7 and r["p_value"] < 1e-6
    assert r["p_value"] == pytest.approx(stats.mannwhitneyu(b, a)[1])
    assert r["ic_dif_medianas"][0] < 10 < r["ic_dif_medianas"][1]
    same = S.comparar_periodos(rng.normal(0, 1, 50), rng.normal(0, 1, 50))
    assert abs(same["rango_biserial"]) < 0.35


def test_retrospective_detection_reports_lead_time_and_warning():
    rng = np.random.default_rng(5)
    x = np.r_[rng.normal(5, 0.3, 60), np.linspace(5, 9, 40) + rng.normal(0, 0.3, 40)]
    fechas = [f"d{i}" for i in range(100)]
    r = S.deteccion_retrospectiva(fechas, x, n_base=40, k=3, indice_falla=99)
    assert r["indice_alarma_umbral"] is not None and 60 <= r["indice_alarma_umbral"] < 99
    assert r["dias_antelacion_umbral"] == 99 - r["indice_alarma_umbral"]
    assert "un solo evento" in r["advertencia"]
