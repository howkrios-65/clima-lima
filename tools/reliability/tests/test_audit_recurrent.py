import numpy as np
import pandas as pd
import pytest

from reliability_kit import audit_recurrent


def frame(rows):
    return pd.DataFrame(rows, columns=["u", "t", "s"])


def test_detects_every_recurrent_data_problem_hand_built():
    df = frame([
        ("A", 10, 1), ("A", 20, 1), ("A", 20, 1), ("A", 50, 0),    # eventos simultáneos en A
        ("B", 40, 0),                                               # sin eventos
        ("C", 5, 1), ("C", 60, 0), ("C", 70, 1),                    # evento posterior al fin
        ("D", 3, 1),                                                # sin fin de observación
        ("E", 30, 0), ("E", 35, 0),                                 # dos fines de observación
    ])
    r = audit_recurrent(df, "u", "t", "s", ages=[45])
    text = " | ".join(r["flags"])
    assert "1 unidades sin fila de fin" in text and "'D'" in text
    assert "1 unidades con más de un fin" in text and "'E'" in text
    assert "1 eventos posteriores al fin" in text
    assert "1 grupos de eventos simultáneos (2 filas)" in text
    u = r["units"]
    assert u["n_events"].to_dict() == {"A": 3, "B": 0, "C": 2, "D": 1, "E": 0}
    assert u.loc["A", "T_k"] == 50 and u.loc["E", "T_k"] == 35 and np.isnan(u.loc["D", "T_k"])
    assert r["summary"]["units"] == 5 and r["summary"]["events"] == 6 and r["summary"]["units_without_events"] == 2
    assert r["at_risk"]["unidades_en_riesgo"].tolist() == [2]       # A (50) y C (60) siguen en 45


def test_foreign_codes_and_nonpositive_times():
    r = audit_recurrent(frame([("A", 5, 1), ("A", 9, 0), ("B", 0, 1), ("B", 7, 0), ("C", 3, 9), ("C", 8, 0)]), "u", "t", "s")
    text = " | ".join(r["flags"])
    assert "códigos de estado ajenos: [9]" in text and "tiempo <= 0" in text


def test_clean_data_has_no_flags_and_atypical_censoring_is_marked():
    rng = np.random.default_rng(0)
    rows = []
    for k in range(30):
        T = 600 + rng.integers(-20, 20)
        rows += [(k, int(rng.integers(1, T)), 1) for _ in range(rng.integers(0, 3))] + [(k, int(T), 0)]
    rows.append((99, 150, 0))                                   # salida temprana
    r = audit_recurrent(frame(rows), "u", "t", "s")
    assert r["units"].loc[99, "censura_atipica"] == "temprana"
    assert any("tempranos" in f and "99" in f for f in r["flags"])
    ok = audit_recurrent(frame([(k, 100 + k % 3, 0) for k in range(10)] + [(0, 50, 1)]), "u", "t", "s")
    assert not [f for f in ok["flags"] if "posteriores" in f or "sin fila" in f or "más de un fin" in f]


def test_empty_input_raises():
    with pytest.raises(ValueError):
        audit_recurrent(frame([]), "u", "t", "s")
