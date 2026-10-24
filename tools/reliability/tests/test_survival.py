import numpy as np
import pytest

from reliability_kit.survival import kaplan_meier, logrank_test


def test_km_no_censoring():
    km = kaplan_meier([1, 2, 3, 4], [1, 1, 1, 1])
    assert km.survival.tolist() == [0.75, 0.5, 0.25, 0.0]
    assert km.median() == 2
    assert km.at(0.5) == 1.0 and km.at(2.5) == 0.5


def test_km_with_censoring_hand_calc():
    km = kaplan_meier([1, 2, 3, 4], [1, 0, 1, 1])
    assert km.survival == pytest.approx([0.75, 0.375, 0.0])
    assert km.n_risk.tolist() == [4, 2, 1]


def test_km_ties():
    km = kaplan_meier([2, 2, 3, 5], [1, 1, 1, 0])
    assert km.survival == pytest.approx([0.5, 0.25])
    assert km.n_event.tolist() == [2, 1]


def test_km_median_not_reached():
    assert np.isnan(kaplan_meier([1, 5, 6, 7], [1, 0, 0, 0]).median())


def test_km_ci_bounds_valid_and_ordered():
    rng = np.random.default_rng(1)
    t = rng.exponential(10, 80)
    c = rng.uniform(0, 25, 80)
    obs = np.minimum(t, c); e = t <= c
    km = kaplan_meier(obs, e)
    inside = (km.survival > 0)
    assert np.all(km.lower[inside] <= km.survival[inside]) and np.all(km.survival[inside] <= km.upper[inside])
    assert np.all((km.lower >= 0) & (km.upper <= 1))
    assert np.all(np.diff(km.survival) <= 1e-12)


def test_km_ci_coverage_at_fixed_time():
    hits, N, true = 0, 400, np.exp(-10 / 10)
    for s in range(N):
        rng = np.random.default_rng(s)
        t = rng.exponential(10, 60); c = rng.uniform(0, 30, 60)
        km = kaplan_meier(np.minimum(t, c), t <= c)
        i = np.searchsorted(km.time, 10, side="right") - 1
        hits += km.lower[i] <= true <= km.upper[i]
    assert 0.91 <= hits / N <= 0.99


def test_km_requires_events():
    with pytest.raises(ValueError):
        kaplan_meier([1, 2, 3], [0, 0, 0])


def test_logrank_identical_vs_separated():
    rng = np.random.default_rng(2)
    a = rng.exponential(10, 60); b = rng.exponential(10, 60); c = rng.exponential(3, 60)
    ones = np.ones(60, bool)
    assert logrank_test(a, ones, b, ones)["p_value"] > 0.05
    assert logrank_test(a, ones, c, ones)["p_value"] < 0.001


def test_logrank_hand_example():
    # A: 1,3 ; B: 2,4 (todos eventos). Tiempos 1..4
    r = logrank_test([1, 3], [1, 1], [2, 4], [1, 1])
    # t=1: n=4 n1=2 d=1 -> O-E=1-0.5 ; V=(2/4)(2/4)=.25
    # t=2: n=3 n1=1 d=1 -> 0-1/3 ; V=(1/3)(2/3)=2/9 ; t=3: n=2 n1=1 d=1 -> 1-.5 ; V=.25 ; t=4: n=1 n1=0 -> 0, V=0 (n=1)
    oe = 0.5 - 1 / 3 + 0.5
    v = 0.25 + 2 / 9 + 0.25
    assert r["chi2"] == pytest.approx(oe ** 2 / v)
