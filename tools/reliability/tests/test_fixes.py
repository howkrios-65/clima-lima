"""Pruebas de las correcciones surgidas de la prueba con datos reales (genfan / valveSeat)."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import optimize, stats

from reliability_kit import nhpp as N
from reliability_kit import survival as S
from reliability_kit import weibull as W

ROOT = Path(__file__).resolve().parents[1]


def sim_w(n, beta, eta, seed, censor_at=None):
    rng = np.random.default_rng(seed)
    t = eta * rng.weibull(beta, n)
    if censor_at is None:
        return t, np.zeros(n, bool)
    c = t > censor_at
    return np.where(c, censor_at, t), c


def sim_nhpp(lam, beta, T, rng):
    out, g = [], 0.0
    while True:
        g += rng.exponential(1.0)
        t = (g / lam) ** (1 / beta)
        if t > T:
            return np.array(out)
        out.append(t)


# ---------- 1. avisos de sesgo ----------
def test_bias_warning_with_12_failures_and_heavy_censoring():
    t, c = sim_w(70, 1.0, 26000, 3, censor_at=11500)      # ~ perfil de genfan
    f = W.fit_weibull_mle(t, c)
    assert 10 <= f.r < 30
    txt = " ".join(f.warnings)
    assert "sesgado al alza" in txt and "bias_correct_beta" in txt
    assert "suspensiones" in txt and "extrapol" in txt


def test_no_bias_warning_with_many_failures_and_little_censoring():
    t, c = sim_w(200, 2.0, 100, 4, censor_at=300)
    assert W.fit_weibull_mle(t, c).warnings == []


# ---------- 2. veredicto de AIC ----------
@pytest.mark.parametrize("d,frag", [(0.0, "empate"), (1.99, "empate"), (2.0, "menor respaldo"),
                                     (10.0, "menor respaldo"), (10.01, "sin respaldo")])
def test_aic_support_thresholds(d, frag):
    assert frag in W.aic_support(d)


def test_compare_models_reports_ties_and_clear_winner():
    rng = np.random.default_rng(11)
    r = W.compare_models_verdict(rng.exponential(100, 300))
    assert "exponential" in r["tied"] and "Empate estadístico" in r["verdict"] and len(r["tied"]) > 1
    assert all("support" in m for m in r["models"])
    t, c = sim_w(400, 4.0, 100, 12)
    r2 = W.compare_models_verdict(t, c)
    assert r2["tied"] == ["weibull"] and "único con respaldo" in r2["verdict"]


# ---------- 3. IC de B-life ----------
def _independent_profile_ll(B, p, t, d):
    k = -np.log(1 - p)
    best = -np.inf
    for lb in np.linspace(np.log(0.2), np.log(30), 4000):       # rejilla de fuerza bruta en β
        b = np.exp(lb)
        best = max(best, W._loglik(b, B / k ** (1 / b), t, d))
    return best


def test_b_life_ci_deviance_at_bounds_matches_brute_force():
    t, c = sim_w(40, 2.0, 100, 5, censor_at=110)
    d = ~c
    ci = W.weibull_b_life_ci_lr(t, c, 0.10)
    f = W.fit_weibull_mle(t, c)
    ll_max = W._loglik(f.beta, f.eta, t, d)
    crit = stats.chi2.ppf(0.95, 1)
    for B in (ci["lower"], ci["upper"]):
        assert 2 * (ll_max - _independent_profile_ll(B, 0.10, t, d)) == pytest.approx(crit, abs=0.02)
    assert ci["lower"] < ci["estimate"] < ci["upper"]
    assert ci["estimate"] == pytest.approx(f.b_life(0.10))


def test_b_life_ci_coverage():
    true_b10 = 100 * (-np.log(0.9)) ** (1 / 2.0)
    hits, N_ = 0, 300
    for s in range(N_):
        t, c = sim_w(40, 2.0, 100, 2000 + s, censor_at=110)
        ci = W.weibull_b_life_ci_lr(t, c, 0.10)
        hits += ci["lower"] <= true_b10 <= ci["upper"]
    assert 0.90 <= hits / N_ <= 0.99


def test_km_failure_quantile_hand_and_open_interval():
    km = S.kaplan_meier(np.arange(1, 11), np.ones(10))
    q = S.km_failure_quantile(km, 0.10)
    assert q["estimate"] == 1.0                      # S(1)=0.9 <= 0.9
    assert q["lower"] <= q["estimate"] <= q["upper"]
    # pocas fallas: la banda inferior nunca baja del objetivo => IC abierto (nan), no inventado
    km2 = S.kaplan_meier([5, 100, 100, 100, 100, 100], [1, 0, 0, 0, 0, 0])
    q2 = S.km_failure_quantile(km2, 0.5)
    assert np.isnan(q2["estimate"]) and np.isnan(q2["upper"])
    with pytest.raises(ValueError):
        S.km_failure_quantile(km, 1.0)


def test_km_quantile_ci_orders_on_random_data():
    for s in range(30):
        rng = np.random.default_rng(s)
        t = rng.exponential(10, 80); c = rng.uniform(0, 25, 80)
        q = S.km_failure_quantile(S.kaplan_meier(np.minimum(t, c), t <= c), 0.2)
        if not np.isnan(q["estimate"]):
            assert q["lower"] <= q["estimate"]
            assert np.isnan(q["upper"]) or q["estimate"] <= q["upper"]


# ---------- 4. corrección de sesgo de β ----------
def test_bias_correction_reduces_bias():
    mle, bc = [], []
    for s in range(80):
        life = 100 * np.random.default_rng(3000 + s).weibull(2.0, 15)
        t, c = np.minimum(life, 130), life > 130
        if (~c).sum() < 4:
            continue
        r = W.bias_correct_beta(t, c, n_boot=100, seed=s)
        mle.append(r["beta_mle"]); bc.append(r["beta_bc"])
    assert np.mean(mle) > 2.1                                    # el MLE sí está sesgado al alza
    assert abs(np.mean(bc) - 2.0) < abs(np.mean(mle) - 2.0) * 0.6
    assert "horizonte de censura" in r["assumption"]


def test_bias_correction_reproducible():
    t, c = sim_w(30, 2.0, 100, 7, censor_at=120)
    assert W.bias_correct_beta(t, c, n_boot=100, seed=1) == W.bias_correct_beta(t, c, n_boot=100, seed=1)


# ---------- 5. bondad de ajuste con censura ----------
def test_gof_size_and_power():
    rej = 0
    for s in range(100):
        t, c = sim_w(60, 2.0, 100, 4000 + s, censor_at=110)
        rej += W.gof_censored_bootstrap(t, c, "weibull", n_boot=100, seed=s)["p_value"] < 0.05
    assert rej / 100 <= 0.12
    t, c = sim_w(150, 4.0, 100, 9)                               # desgaste fuerte
    assert W.gof_censored_bootstrap(t, c, "exponential", n_boot=200, seed=1)["p_value"] < 0.01
    with pytest.raises(ValueError):
        W.gof_censored_bootstrap(t, c, "gamma")


# ---------- 6. MCF con IC (Lawless-Nadeau) ----------
def test_mcf_variance_hand_calc():
    r = N.mean_cumulative_function([[2, 5], [3]], [10, 4])
    assert r["se"][0] ** 2 == pytest.approx(0.125)               # calculado a mano en t=2
    assert r["n_at_risk"].tolist() == [2, 2, 1]
    assert np.all(r["lower"][r["mcf"] > 0] <= r["mcf"][r["mcf"] > 0])


def _hpp_units(K, rate, rng):
    ends = rng.uniform(100, 200, K)
    return [np.sort(rng.uniform(0, e, rng.poisson(rate * e))) for e in ends], ends


def test_mcf_se_matches_unit_bootstrap():
    rng = np.random.default_rng(1)
    ev, ends = _hpp_units(40, 0.02, rng)
    full = N.mean_cumulative_function(ev, ends)
    i = np.searchsorted(full["time"], 80, side="right") - 1
    boots = []
    for b in range(1000):
        idx = rng.integers(0, 40, 40)
        m = N.mean_cumulative_function([ev[k] for k in idx], ends[idx])
        j = np.searchsorted(m["time"], 80, side="right") - 1
        boots.append(m["mcf"][j] if j >= 0 else 0.0)
    assert full["se"][i] == pytest.approx(np.std(boots, ddof=1), rel=0.15)


def test_mcf_ci_coverage():
    rate, t0, hits, reps = 0.01, 80, 0, 300
    for s in range(reps):
        rng = np.random.default_rng(5000 + s)
        ev, ends = _hpp_units(25, rate, rng)
        if sum(e.size for e in ev) == 0:
            continue
        m = N.mean_cumulative_function(ev, ends)
        i = np.searchsorted(m["time"], t0, side="right") - 1
        if i >= 0:
            hits += m["lower"][i] <= rate * m["time"][i] <= m["upper"][i]   # la verdad en el último evento ≤ t0
    assert 0.90 <= hits / reps <= 0.99


# ---------- 7. Crow-AMSAA multi-unidad ----------
def multi_sim(K, beta, rng):
    lam = rng.uniform(0.005, 0.03, K) * 1.0
    ends = rng.uniform(60, 140, K)
    ev = [sim_nhpp(l, beta, T, rng) for l, T in zip(lam, ends)]
    return ev, ends


def test_multi_reduces_to_single_unit():
    t = N.fit_crow_amsaa([10, 20, 40, 80], 100)
    m = N.fit_crow_amsaa_multi([[10, 20, 40, 80]], [100])
    assert m.beta == pytest.approx(t.beta) and m.beta_ci == pytest.approx(t.beta_ci)
    assert N.laplace_trend_test_multi([[10, 20, 40, 80]], [100])["U"] == pytest.approx(
        N.laplace_trend_test([10, 20, 40, 80], 100)["U"])


def test_multi_conditional_unbiased_and_covers_with_unit_heterogeneity():
    rng = np.random.default_rng(1)
    betas, hits, reps = [], 0, 400
    for _ in range(reps):
        ev, ends = multi_sim(30, 1.5, rng)
        if sum(e.size for e in ev) < 5:
            continue
        f = N.fit_crow_amsaa_multi(ev, ends)
        betas.append(f.beta); hits += f.beta_ci[0] <= 1.5 <= f.beta_ci[1]
    assert np.mean(betas) == pytest.approx(1.5, abs=0.03)
    assert 0.92 <= hits / len(betas) <= 0.98


def test_naive_pooling_is_wrong_but_multi_is_right():
    """Con T_k muy distintos, mezclar los tiempos de todas las unidades en una sola (lo que haría el modo
    de una unidad) enmascara la tendencia; el modo multi-unidad la recupera."""
    rng = np.random.default_rng(2)
    ends = np.array([100.0] * 20 + [400.0] * 20)
    ev = [sim_nhpp(0.002 if T == 400 else 0.01, 1.8, T, rng) for T in ends]
    pooled = np.sort(np.concatenate(ev))
    naive = N.fit_crow_amsaa(pooled, ends.max())
    multi = N.fit_crow_amsaa_multi(ev, ends)
    assert abs(multi.beta - 1.8) < abs(naive.beta - 1.8)
    assert multi.beta_ci[0] > 1


def test_multi_common_lambda_matches_direct_maximization_and_homogeneous_truth():
    rng = np.random.default_rng(3)
    ends = rng.uniform(60, 140, 30)
    ev = [sim_nhpp(0.01, 1.4, T, rng) for T in ends]
    f = N.fit_crow_amsaa_multi(ev, ends, model="common", unbiased=False)
    Nn = sum(e.size for e in ev); sl = sum(np.log(e).sum() for e in ev if e.size)

    def nll(lb):
        b = np.exp(lb); lam = Nn / (ends ** b).sum()
        return -(Nn * np.log(lam) + Nn * np.log(b) + (b - 1) * sl - lam * (ends ** b).sum())

    r = optimize.minimize_scalar(nll, bounds=(-3, 3), method="bounded", options={"xatol": 1e-10})
    assert f.beta == pytest.approx(np.exp(r.x), rel=1e-5)
    assert f.beta_ci[0] < f.beta < f.beta_ci[1] and any("homogéneas" in w for w in f.warnings)


def test_multi_errors_and_zero_event_units():
    with pytest.raises(ValueError):
        N.fit_crow_amsaa_multi([[1], [2]], [10, 10])                 # < 3 eventos
    with pytest.raises(ValueError):
        N.fit_crow_amsaa_multi([[1, 2, 30]], [10])                   # evento > T
    with pytest.raises(ValueError):
        N.fit_crow_amsaa_multi([[1, 2, 3]], [10], model="x")
    f = N.fit_crow_amsaa_multi([[1, 2, 3, 4], [], []], [10, 10, 10])
    assert f.n_units == 3 and f.n_units_with_events == 1 and any("sin eventos" in w for w in f.warnings)


def test_laplace_multi_size_and_power():
    rng = np.random.default_rng(4)
    rej = 0
    for _ in range(400):
        ends = rng.uniform(60, 140, 20)
        ev = [sim_nhpp(0.03, 1.0, T, rng) for T in ends]
        rej += N.laplace_trend_test_multi(ev, ends)["p_value"] < 0.05
    assert rej / 400 < 0.09
    ends = rng.uniform(60, 140, 20)
    det = [sim_nhpp(0.002, 1.8, T, rng) for T in ends]
    assert N.laplace_trend_test_multi(det, ends)["U"] > 0


def test_heterogeneity_test_size_and_power():
    rng = np.random.default_rng(5)
    rej = 0
    for s in range(200):
        ends = rng.uniform(60, 140, 15)
        ev = [sim_nhpp(0.03, 1.0, T, rng) for T in ends]
        rej += N.unit_heterogeneity_test(ev, ends, n_sim=500, seed=s)["p_value"] < 0.05
    assert rej / 200 < 0.09
    ends = np.full(15, 100.0)
    het = [sim_nhpp(0.005 if k < 12 else 0.1, 1.0, 100, rng) for k in range(15)]
    assert N.unit_heterogeneity_test(het, ends, n_sim=2000, seed=1)["p_value"] < 0.01


# ---------- 8. CLI ----------
def run(*args, check=True):
    return subprocess.run([sys.executable, "-m", "reliability_kit", *map(str, args)], cwd=ROOT,
                          capture_output=True, text=True, check=check)


def test_cli_multi_unit_and_warning_for_unit_like_column(tmp_path):
    rng = np.random.default_rng(0)
    rows = []
    for k in range(12):
        T = float(rng.uniform(80, 150))
        for x in sim_nhpp(0.02, 1.4, T, rng):
            rows.append({"motor": k, "t": x, "fin": T})
    rows.append({"motor": 99, "t": 5.0, "fin": 120.0})
    pd.DataFrame(rows).to_csv(tmp_path / "m.csv", index=False)
    out = json.loads(run("crow-amsaa", tmp_path / "m.csv", "--time", "t", "--unit", "motor", "--end", "fin").stdout)
    assert out["n_units"] == 13 and "heterogeneity" in out and "laplace_pooled" in out
    r = run("crow-amsaa", tmp_path / "m.csv", "--time", "t", "--T", 150)         # modo una unidad sobre datos multi
    assert "ADVERTENCIA" in r.stderr and "motor" in r.stderr
    bad = run("crow-amsaa", tmp_path / "m.csv", "--time", "t", "--unit", "motor", check=False)
    assert bad.returncode != 0 and "--end" in bad.stderr


def test_cli_weibull_reports_b10_ci_bias_and_verdict(tmp_path):
    t, c = sim_w(60, 1.0, 26000, 3, censor_at=11500)
    pd.DataFrame({"t": t, "c": c.astype(int)}).to_csv(tmp_path / "w.csv", index=False)
    out = json.loads(run("weibull", tmp_path / "w.csv", "--time", "t", "--censored", "c").stdout)
    assert out["B10_ci95_LR"]["lower"] < out["B10"] < out["B10_ci95_LR"]["upper"]
    assert "beta_bias_corrected" in out and out["beta_bias_corrected"]["beta_bc"] < out["beta"]
    assert out["model_comparison"]
