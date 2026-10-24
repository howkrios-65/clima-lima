import numpy as np
import pandas as pd
import pytest

from reliability_kit import economics as E
from reliability_kit import mlcheck as M
from reliability_kit import workorders as P
from reliability_kit.data_quality import audit


# ---------- pareto / bad actors ----------
def wo():
    return pd.DataFrame({
        "asset": list("AAABBC") + ["D"] * 1,
        "cost": [10, 10, 10, 50, 50, 5, 1],
        "down": [1, 1, 1, 2, 2, 20, 0],
        "code": ["x", "x", "x", "y", "z", "q", "q"],
        "date": pd.to_datetime(["2024-01-01", "2024-03-01", "2024-05-01", "2023-01-01", "2024-06-01", "2024-02-01", "2024-02-01"]),
    })


def test_pareto_hand_calc():
    t = P.pareto(wo()[wo().asset.isin(list("ABC"))], "asset")
    assert t["asset"].tolist() == ["A", "B", "C"]
    assert t["share"].tolist() == pytest.approx([0.5, 1 / 3, 1 / 6])
    assert t["cum_share"].tolist() == pytest.approx([0.5, 5 / 6, 1.0])
    assert t["vital_few"].tolist() == [True, True, False]


def test_pareto_value_and_errors():
    t = P.pareto(wo(), "asset", "cost")
    assert t.iloc[0]["asset"] == "B" and t.iloc[0]["total"] == 100
    with pytest.raises(KeyError):
        P.pareto(wo(), "nope")
    with pytest.raises(ValueError):
        P.pareto(wo().assign(cost=0), "asset", "cost")


def test_bad_actors_cross_views():
    r = P.bad_actors(wo(), "asset", cost="cost", downtime="down", threshold=0.5)
    ba = set(r.loc[r.bad_actor, "asset"])
    # B: top costo y 2º en frecuencia; A: top frecuencia (3/7) ; C: top downtime
    assert "B" in ba
    assert r.set_index("asset").loc["D", "bad_actor"] == False  # noqa: E712


def test_chronic_repeaters():
    r = P.chronic_repeaters(wo(), "asset", "code", "date", min_repeats=3, window_days=365)
    assert r[["asset", "code", "max_repeats_in_window"]].values.tolist() == [["A", "x", 3]]
    assert P.chronic_repeaters(wo(), "asset", "code", "date", min_repeats=3, window_days=30).empty


# ---------- data quality ----------
def test_audit_flags():
    df = pd.DataFrame({"id": [1, 1, 2, 3], "start": ["2024-01-05", "2024-01-05", "bad", "2024-02-01"],
                       "end": ["2024-01-04", "2024-01-04", "2024-01-09", "2024-02-02"],
                       "code": [None, None, None, "a"]})
    r = audit(df, date_cols=("start", "end"), key_cols=("id",), critical_cols=("code",))
    s = r["summary"]
    assert s["rows"] == 4 and s["duplicate_rows"] == 1 and s["duplicate_keys"] == 1
    assert s["start_unparseable"] == 1
    assert s["start_after_end"] == 2   # 'end' < 'start' en las 2 filas duplicadas
    assert r["columns"].loc["code", "missing_pct"] == 75
    assert any("campo crítico 'code'" in f for f in r["flags"])
    with pytest.raises(ValueError):
        audit(df.iloc[0:0])


# ---------- economics ----------
def test_npv_eac_hand():
    assert E.npv([100, 100], 0.10) == pytest.approx(190.9090909)
    assert E.eac(1000, 0.10, 5) == pytest.approx(263.7974808)
    assert E.eac(1000, 0.0, 4) == 250
    # EAC inversa: el valor presente de la anualidad vuelve al PV
    assert E.npv([E.eac(1000, 0.1, 5)] * 5, 0.1, t0=1) == pytest.approx(1000)


def test_cost_rate_exponential_closed_form():
    eta, T, cp, cf = 100.0, 50.0, 1.0, 10.0
    q = np.exp(-T / eta)
    expected = (cp * q + cf * (1 - q)) / (eta * (1 - q))
    assert E.age_replacement_cost_rate(T, 1.0, eta, cp, cf) == pytest.approx(expected, rel=1e-6)


def test_optimal_age_is_a_true_minimum_and_beats_run_to_failure():
    r = E.optimal_age_replacement(3.0, 1000.0, 1.0, 10.0)
    T = r["optimal_age"]
    f = lambda x: E.age_replacement_cost_rate(x, 3.0, 1000.0, 1.0, 10.0)
    assert 0 < T < 1000
    assert f(T) < f(0.8 * T) and f(T) < f(1.25 * T)
    assert r["cost_rate"] < r["cost_rate_run_to_failure"] and r["saving_pct"] > 0
    grid = np.linspace(50, 3000, 600)
    assert f(T) <= min(f(g) for g in grid) + 1e-9


def test_optimal_age_refuses_when_not_justified():
    assert E.optimal_age_replacement(1.0, 100, 1, 10)["optimal_age"] is None
    assert E.optimal_age_replacement(0.8, 100, 1, 10)["optimal_age"] is None
    assert E.optimal_age_replacement(3.0, 100, 10, 10)["optimal_age"] is None
    with pytest.raises(ValueError):
        E.optimal_age_replacement(3.0, 100, 0, 10)


def test_availability():
    assert E.inherent_availability(900, 100) == 0.9
    with pytest.raises(ValueError):
        E.inherent_availability(0, 1)


# ---------- ml validation ----------
def ts_df():
    return pd.DataFrame({"t": pd.date_range("2024-01-01", periods=100), "asset": np.repeat(np.arange(10), 10), "y": np.arange(100) % 2})


def test_temporal_split_no_future_leak():
    tr, te = M.temporal_split(ts_df(), "t", 0.2)
    assert tr.t.max() < te.t.min() and len(te) == 20
    tr2, te2 = M.temporal_split(ts_df(), "t", 0.2, gap=pd.Timedelta(days=5))
    assert tr2.t.max() <= te2.t.min() - pd.Timedelta(days=5)


def test_group_split_disjoint_and_checker():
    tr, te = M.group_split(ts_df(), "asset", 0.3, seed=1)
    M.assert_no_overlap(tr, te, "asset")
    assert set(tr.asset).isdisjoint(te.asset)
    random_split = ts_df().sample(frac=0.5, random_state=0)
    with pytest.raises(AssertionError):
        M.assert_no_overlap(random_split, ts_df().drop(random_split.index), "asset")


def test_pr_metrics():
    y = np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    assert M.pr_metrics(y, np.array([9, 8, 1, 1, 1, 1, 1, 1, 1, 0.5]))["average_precision"] == pytest.approx(1.0)
    rng = np.random.default_rng(0)
    y = (rng.uniform(size=20000) < 0.05).astype(int)
    r = M.pr_metrics(y, rng.uniform(size=20000))
    assert r["average_precision"] == pytest.approx(r["prevalence"], abs=0.015)
    # hand: scores .9(+) .8(-) .7(+) -> AP = 1*0.5 + (2/3)*0.5
    assert M.pr_metrics([1, 0, 1], [0.9, 0.8, 0.7])["average_precision"] == pytest.approx(0.5 + (2 / 3) * 0.5)
    with pytest.raises(ValueError):
        M.pr_metrics([0, 0, 0], [0.1, 0.2, 0.3])


def test_recall_at_precision_and_cost_threshold():
    y = [1, 1, 0, 1, 0, 0]; s = [0.9, 0.8, 0.7, 0.6, 0.3, 0.1]
    r = M.recall_at_precision(y, s, 1.0)
    assert r["recall"] == pytest.approx(2 / 3) and r["threshold"] == 0.8
    assert M.recall_at_precision(y, s, 0.7)["recall"] == 1.0
    c = M.cost_optimal_threshold(y, s, cost_fn=100, cost_fp=1)
    assert c["threshold"] == 0.6 and c["total_cost"] == 1 and c["fn"] == 0
    assert c["cost_never_alert"] == 300


def test_brier_calibration():
    y = [1, 0, 1, 0]
    assert M.brier_and_calibration(y, [1, 0, 1, 0])["brier"] == 0
    r = M.brier_and_calibration(y, [0.5] * 4)
    assert r["brier"] == 0.25 and r["calibration"].iloc[0]["obs_rate"] == 0.5
    with pytest.raises(ValueError):
        M.brier_and_calibration(y, [1.2, 0, 0, 0])
