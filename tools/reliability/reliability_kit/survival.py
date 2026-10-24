"""Supervivencia no paramétrica: Kaplan-Meier (Greenwood, IC log-log) y prueba log-rank."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class KMResult:
    time: np.ndarray
    n_risk: np.ndarray
    n_event: np.ndarray
    survival: np.ndarray
    lower: np.ndarray
    upper: np.ndarray
    conf: float

    def median(self) -> float:
        """Primer tiempo con S(t) <= 0.5; nan si la curva no baja de 0.5 (mediana no alcanzada)."""
        idx = np.where(self.survival <= 0.5)[0]
        return float(self.time[idx[0]]) if idx.size else float("nan")

    def at(self, t: float) -> float:
        idx = np.searchsorted(self.time, t, side="right") - 1
        return 1.0 if idx < 0 else float(self.survival[idx])


def _validate(times, event):
    t = np.asarray(times, float)
    e = np.asarray(event).astype(bool)
    if t.shape != e.shape or t.ndim != 1 or t.size == 0:
        raise ValueError("times y event deben ser vectores de igual longitud, no vacíos")
    if np.any(t < 0) or not np.all(np.isfinite(t)):
        raise ValueError("tiempos negativos o no finitos")
    return t, e


def kaplan_meier(times, event, conf: float = 0.95) -> KMResult:
    """event=True => falla observada; False => censura por derecha."""
    t, e = _validate(times, event)
    ut = np.unique(t[e])
    if ut.size == 0:
        raise ValueError("no hay fallas observadas: la curva KM no está definida")
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    S, gw = 1.0, 0.0
    out = {k: [] for k in ("n", "d", "s", "lo", "hi")}
    for ti in ut:
        n_i = int(np.sum(t >= ti))
        d_i = int(np.sum((t == ti) & e))
        S *= 1.0 - d_i / n_i
        if n_i > d_i:
            gw += d_i / (n_i * (n_i - d_i))
        out["n"].append(n_i); out["d"].append(d_i); out["s"].append(S)
        if 0.0 < S < 1.0 and n_i > d_i:
            se = np.sqrt(gw) / abs(np.log(S))
            lo, hi = S ** np.exp(z * se), S ** np.exp(-z * se)
        else:
            lo = hi = S
        out["lo"].append(lo); out["hi"].append(hi)
    return KMResult(ut, np.array(out["n"]), np.array(out["d"]), np.array(out["s"]),
                    np.array(out["lo"]), np.array(out["hi"]), conf)


def logrank_test(times_a, event_a, times_b, event_b) -> dict:
    """Log-rank de dos grupos (H0: misma curva de supervivencia). Chi² con 1 gl."""
    ta, ea = _validate(times_a, event_a)
    tb, eb = _validate(times_b, event_b)
    t = np.concatenate([ta, tb]); e = np.concatenate([ea, eb])
    g = np.concatenate([np.zeros(ta.size), np.ones(tb.size)])
    O_minus_E, V = 0.0, 0.0
    for ti in np.unique(t[e]):
        at = t >= ti
        n = at.sum(); n1 = (at & (g == 0)).sum()
        d = ((t == ti) & e).sum(); d1 = ((t == ti) & e & (g == 0)).sum()
        O_minus_E += d1 - d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    if V == 0:
        raise ValueError("varianza nula: datos insuficientes para el log-rank")
    chi2 = O_minus_E ** 2 / V
    return {"chi2": float(chi2), "p_value": float(stats.chi2.sf(chi2, 1)), "dof": 1}
