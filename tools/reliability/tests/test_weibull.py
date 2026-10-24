import numpy as np
import pytest
from scipy import optimize, stats

from reliability_kit import weibull as W


def sim(n, beta, eta, seed, censor_at=None):
    rng = np.random.default_rng(seed)
    t = eta * rng.weibull(beta, n)
    if censor_at is None:
        return t, np.zeros(n, bool)
    c = t > censor_at
    return np.where(c, censor_at, t), c


def test_complete_matches_scipy():
    t, c = sim(500, 2.5, 500, 1)
    f = W.fit_weibull_mle(t, c)
    shape, loc, scale = stats.weibull_min.fit(t, floc=0)
    assert f.beta == pytest.approx(shape, rel=1e-4)
    assert f.eta == pytest.approx(scale, rel=1e-4)


def test_recovers_parameters_large_sample():
    t, c = sim(5000, 2.5, 500, 2)
    f = W.fit_weibull_mle(t, c)
    assert f.beta == pytest.approx(2.5, rel=0.04)
    assert f.eta == pytest.approx(500, rel=0.02)
    assert f.warnings == []


def test_censored_matches_direct_likelihood_maximization():
    t, c = sim(300, 1.8, 200, 3, censor_at=220)
    f = W.fit_weibull_mle(t, c)
    d = ~c

    def nll(p):
        b, e = np.exp(p)
        return -W._loglik(b, e, t, d)

    res = optimize.minimize(nll, [0, np.log(200)], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12})
    assert f.beta == pytest.approx(np.exp(res.x[0]), rel=1e-4)
    assert f.eta == pytest.approx(np.exp(res.x[1]), rel=1e-4)
    assert f.loglik == pytest.approx(-res.fun, abs=1e-5)
    assert f.n_suspensions == c.sum() and f.r == d.sum()


def test_scale_invariance():
    t, c = sim(100, 2.0, 50, 4, censor_at=60)
    a = W.fit_weibull_mle(t, c)
    b = W.fit_weibull_mle(t * 1000, c)
    assert a.beta == pytest.approx(b.beta, rel=1e-9)
    assert a.eta * 1000 == pytest.approx(b.eta, rel=1e-9)


def test_b_life_mttf_reliability():
    f = W.WeibullFit(beta=2.0, eta=100.0, n=10, r=10, loglik=0.0)
    assert f.b_life(0.10) == pytest.approx(100 * np.sqrt(-np.log(0.9)))
    assert f.reliability(f.b_life(0.10)) == pytest.approx(0.90)
    assert f.mttf == pytest.approx(100 * 0.5 * np.sqrt(np.pi))
    assert f.hazard(100.0) == pytest.approx(2 / 100)
    with pytest.raises(ValueError):
        f.b_life(1.0)


def test_small_sample_warns():
    f = W.fit_weibull_mle([10, 20, 30, 45, 60])
    assert any("exploratorio" in w for w in f.warnings)


@pytest.mark.parametrize("times,cens", [([5.0], None), ([5, 5, 5], None), ([1, 2, 0], None),
                                         ([1, 2, 3], [True, True, False]), ([], None), ([1, -2, 3], None)])
def test_invalid_inputs_raise(times, cens):
    with pytest.raises(ValueError):
        W.fit_weibull_mle(times, cens)


def test_lr_ci_coverage():
    hits, N = 0, 300
    for s in range(N):
        t, c = sim(30, 2.0, 100, 1000 + s, censor_at=120)
        lo, hi = W.weibull_beta_ci_lr(t, c)
        hits += lo <= 2.0 <= hi
    assert 0.90 <= hits / N <= 0.99


def test_lr_ci_brackets_estimate_and_widens_with_confidence():
    t, c = sim(40, 2.0, 100, 7)
    f = W.fit_weibull_mle(t, c)
    lo95, hi95 = W.weibull_beta_ci_lr(t, c, 0.95)
    lo80, hi80 = W.weibull_beta_ci_lr(t, c, 0.80)
    assert lo95 < f.beta < hi95
    assert lo95 < lo80 < f.beta < hi80 < hi95


def test_bootstrap_ci_reproducible_and_reports_failures():
    t, c = sim(60, 2.0, 100, 8, censor_at=110)
    a = W.weibull_bootstrap_ci(t, c, stat="b_life", p=0.1, n_boot=200, seed=5)
    b = W.weibull_bootstrap_ci(t, c, stat="b_life", p=0.1, n_boot=200, seed=5)
    assert a == b
    assert a["lower"] < a["estimate"] < a["upper"]
    assert a["n_boot_ok"] + a["n_boot_failed"] == 200


def test_johnson_ranks_complete_equals_bernard():
    tf, F = W.johnson_median_ranks([10, 20, 30, 40, 50])
    assert F == pytest.approx((np.arange(1, 6) - 0.3) / 5.4)


def test_johnson_ranks_with_suspension_hand_calc():
    # tiempos 10 F, 20 S, 30 F, 40 F (n=4)
    tf, F = W.johnson_median_ranks([10, 20, 30, 40], [False, True, False, False])
    # rango1: inc=(5-0)/(1+4)=1 -> 1 ; rango 30: rev=2, inc=(5-1)/(1+2)=4/3 -> 7/3 ; 40: rev=1 inc=(5-7/3)/2=4/3 -> 11/3
    adj = np.array([1, 7 / 3, 11 / 3])
    assert tf.tolist() == [10, 30, 40]
    assert F == pytest.approx((adj - 0.3) / 4.4)


def test_rank_regression_close_to_truth():
    t, c = sim(2000, 2.0, 300, 9, censor_at=400)
    rr = W.rank_regression(t, c)
    assert rr["beta"] == pytest.approx(2.0, rel=0.08)
    assert rr["eta"] == pytest.approx(300, rel=0.05)
    assert rr["r2"] > 0.98


def test_compare_models_selects_weibull_for_wearout():
    t, c = sim(400, 3.5, 100, 10)
    m = W.compare_models(t, c)
    assert m[0]["model"] == "weibull"
    assert m[0]["delta_aic"] == 0 and all(x["delta_aic"] >= 0 for x in m)


def test_compare_models_exponential_not_rejected_for_random_failures():
    rng = np.random.default_rng(11)
    t = rng.exponential(100, 300)
    m = {x["model"]: x for x in W.compare_models(t)}
    assert m["exponential"]["delta_aic"] < 3
    assert m["exponential"]["params"]["lambda"] == pytest.approx(1 / t.mean())


def test_compare_models_handles_censoring():
    t, c = sim(200, 2.0, 100, 12, censor_at=90)
    m = W.compare_models(t, c)
    assert {x["model"] for x in m} == {"weibull", "lognormal", "exponential"}
    assert all(np.isfinite(x["aic"]) for x in m)


def test_interpret_beta_respects_uncertainty():
    assert "no se distingue" in W.interpret_beta(1.3, (0.8, 1.9))
    assert "mortalidad infantil" in W.interpret_beta(0.6, (0.5, 0.7))
    assert "desgaste" in W.interpret_beta(2.5, (2.0, 3.1))
    assert "aleatorio" in W.interpret_beta(1.05)
