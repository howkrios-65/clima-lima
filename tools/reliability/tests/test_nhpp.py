import numpy as np
import pytest

from reliability_kit import nhpp as N


def sim_nhpp(lam, beta, T, rng):
    out, g = [], 0.0
    while True:
        g += rng.exponential(1.0)
        t = (g / lam) ** (1 / beta)
        if t > T:
            return np.array(out)
        out.append(t)


def many(lam, beta, T, reps, seed, min_n=4):
    rng = np.random.default_rng(seed)
    res = []
    while len(res) < reps:
        t = sim_nhpp(lam, beta, T, rng)
        if t.size >= min_n:
            res.append(t)
    return res


def test_time_terminated_hand_example():
    t = [10, 20, 40, 80]
    T = 100
    S = np.log(10) + np.log(5) + np.log(2.5) + np.log(1.25)
    f = N.fit_crow_amsaa(t, T, unbiased=False)
    assert f.beta == pytest.approx(4 / S)
    g = N.fit_crow_amsaa(t, T)
    assert g.beta == pytest.approx(3 / S)
    assert g.lam == pytest.approx(4 / T ** g.beta)
    assert g.expected_failures(T) == pytest.approx(4)


def test_unbiased_beta_is_unbiased_and_mle_is_biased_up():
    reps = many(0.05, 1.5, 100, 600, 1)
    unb = np.mean([N.fit_crow_amsaa(t, 100).beta for t in reps])
    mle = np.mean([N.fit_crow_amsaa(t, 100, unbiased=False).beta for t in reps])
    assert unb == pytest.approx(1.5, abs=0.03)
    assert mle > unb


@pytest.mark.parametrize("terminated", ["time", "failure"])
def test_beta_ci_coverage(terminated):
    reps = many(0.05, 1.5, 100, 500, 2)
    hits = 0
    for t in reps:
        f = N.fit_crow_amsaa(t, 100 if terminated == "time" else None, terminated=terminated)
        hits += f.beta_ci[0] <= 1.5 <= f.beta_ci[1]
    assert 0.92 <= hits / len(reps) <= 0.98


def test_failure_terminated_unbiased():
    reps = many(0.05, 0.7, 100, 600, 3, min_n=5)
    unb = np.mean([N.fit_crow_amsaa(t, terminated="failure").beta for t in reps])
    assert unb == pytest.approx(0.7, abs=0.03)


def test_trend_wording_and_rocof():
    t = np.cumsum(np.linspace(60, 2, 25))   # intervalos decrecientes => deterioro claro
    f = N.fit_crow_amsaa(t, t[-1] + 1)
    assert "deterioro" in f.trend and f.beta_ci[0] > 1
    assert f.rocof(t[-1]) > f.rocof(t[0])
    assert f.instantaneous_mtbf(t[-1]) == pytest.approx(1 / f.rocof(t[-1]))


def test_trend_wording_is_honest_when_ci_contains_one():
    t = np.cumsum(np.linspace(30, 5, 12))   # n=12: el IC de β incluye 1
    f = N.fit_crow_amsaa(t, t[-1] + 1)
    assert f.beta_ci[0] < 1 < f.beta_ci[1]
    assert "sin tendencia distinguible" in f.trend


def test_laplace_detects_trend_and_keeps_size():
    det = many(0.05, 1.6, 100, 100, 4)
    imp = many(0.5, 0.6, 100, 100, 5)
    assert np.mean([N.laplace_trend_test(t, 100)["U"] > 0 for t in det]) > 0.9
    assert np.mean([N.laplace_trend_test(t, 100)["U"] < 0 for t in imp]) > 0.9
    null = many(0.2, 1.0, 100, 600, 6, min_n=6)
    rej = np.mean([N.laplace_trend_test(t, 100)["p_value"] < 0.05 for t in null])
    assert rej < 0.09


def test_laplace_failure_terminated_runs():
    t = many(0.05, 1.6, 100, 1, 7)[0]
    r = N.laplace_trend_test(t, terminated="failure")
    assert "n" in r and np.isfinite(r["U"])


def test_gof_mc_accepts_power_law_rejects_bathtub():
    good = many(0.05, 1.5, 100, 1, 8)[0]
    ok = N.crow_amsaa_gof_mc(good, 100, n_sim=500, seed=1)
    assert ok["p_value"] > 0.05
    bad = np.sort(np.r_[np.linspace(1, 6, 10), np.linspace(94, 99, 10)])   # dos ráfagas, no ley de potencia
    nok = N.crow_amsaa_gof_mc(bad, 100, n_sim=500, seed=1)
    assert nok["p_value"] < 0.05
    assert N.crow_amsaa_gof_mc(good, 100, n_sim=200, seed=3) == N.crow_amsaa_gof_mc(good, 100, n_sim=200, seed=3)


@pytest.mark.parametrize("args", [([1, 2], 10), ([1, 2, 3], 2), ([0, 1, 2], 10), ([1, 2, 3], None)])
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        N.fit_crow_amsaa(*args)


def test_mcf_hand_example():
    r = N.mean_cumulative_function([[2, 5], [3]], [10, 4])
    assert r["time"].tolist() == [2, 3, 5]
    assert r["mcf"].tolist() == [0.5, 1.0, 2.0]


def test_mcf_validates_events_within_observation():
    with pytest.raises(ValueError):
        N.mean_cumulative_function([[5]], [4])
    with pytest.raises(ValueError):
        N.mean_cumulative_function([[]], [4])
