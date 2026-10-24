"""Sistemas reparables: Crow-AMSAA / NHPP de ley de potencia (IEC 61164, MIL-HDBK-189),
prueba de Laplace y función media acumulada (MCF) para varias unidades con censura.

Los tiempos son ACUMULADOS de operación de una misma unidad (no tiempos entre fallas).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np
from scipy import stats


@dataclass
class CrowAmsaaFit:
    beta: float            # estimador usado (insesgado si unbiased=True)
    beta_mle: float
    lam: float
    n: int
    T: float
    terminated: str
    beta_ci: tuple[float, float]
    conf: float
    warnings: list[str] = field(default_factory=list)

    def expected_failures(self, t):
        return self.lam * np.asarray(t, float) ** self.beta

    def rocof(self, t):
        return self.lam * self.beta * np.asarray(t, float) ** (self.beta - 1.0)

    def instantaneous_mtbf(self, t):
        return 1.0 / self.rocof(t)

    @property
    def trend(self) -> str:
        lo, hi = self.beta_ci
        if hi < 1:
            return "mejora (β<1, IC por debajo de 1)"
        if lo > 1:
            return "deterioro (β>1, IC por encima de 1)"
        return "sin tendencia distinguible de 1 (IC contiene 1)"


def _clean(times, T, terminated):
    t = np.sort(np.asarray(times, dtype=float))
    if t.size < 3:
        raise ValueError("se requieren al menos 3 fallas")
    if np.any(t <= 0) or not np.all(np.isfinite(t)):
        raise ValueError("los tiempos deben ser > 0 y finitos")
    if terminated not in ("time", "failure"):
        raise ValueError("terminated debe ser 'time' o 'failure'")
    if terminated == "time":
        if T is None:
            raise ValueError("para terminación por tiempo se debe dar T (fin de observación)")
        if T < t[-1]:
            raise ValueError("T no puede ser menor que la última falla")
        return t, float(T)
    return t, float(t[-1])


def fit_crow_amsaa(times: Sequence[float], T: float | None = None, *, terminated: str = "time",
                   unbiased: bool = True, conf: float = 0.95) -> CrowAmsaaFit:
    """Ajuste Crow-AMSAA de una unidad. IC de β exacto por chi-cuadrado.

    Con terminación por tiempo: S=Σln(T/t_i) ~ Gamma(n, β) => 2βS ~ χ²(2n).
    Con terminación por falla:  S=Σ_{i<n}ln(t_n/t_i) ~ Gamma(n-1, β) => 2βS ~ χ²(2(n-1)).
    """
    t, T = _clean(times, T, terminated)
    n = t.size
    if terminated == "time":
        S = float(np.log(T / t).sum())
        dof = 2 * n
        beta_mle = n / S
        beta_unb = (n - 1) / S
    else:
        S = float(np.log(T / t[:-1]).sum())
        dof = 2 * (n - 1)
        beta_mle = n / S
        beta_unb = (n - 2) / S
    a = (1 - conf) / 2
    ci = (float(stats.chi2.ppf(a, dof) / (2 * S)), float(stats.chi2.ppf(1 - a, dof) / (2 * S)))
    beta = beta_unb if unbiased else beta_mle
    lam = n / T ** beta
    warns = []
    if n < 10:
        warns.append(f"solo {n} fallas: exploratorio; el IC de β es amplio")
    return CrowAmsaaFit(beta=float(beta), beta_mle=float(beta_mle), lam=float(lam), n=n, T=T,
                        terminated=terminated, beta_ci=ci, conf=conf, warnings=warns)


def laplace_trend_test(times: Sequence[float], T: float | None = None, *, terminated: str = "time") -> dict:
    """Prueba de Laplace. U>0 sugiere deterioro (fallas cada vez más frecuentes); U<0 mejora.

    H0: proceso de Poisson homogéneo (sin tendencia). p-valor bilateral (normal asintótica;
    razonable desde ~4 fallas).
    """
    t, T = _clean(times, T, terminated)
    n = t.size
    if terminated == "time":
        u = (t.sum() / n - T / 2.0) / (T * np.sqrt(1.0 / (12.0 * n)))
    else:
        m = n - 1
        u = (t[:-1].sum() / m - T / 2.0) / (T * np.sqrt(1.0 / (12.0 * m)))
    p = float(2 * stats.norm.sf(abs(u)))
    verdict = "deterioro" if u > 0 else "mejora"
    return {"U": float(u), "p_value": p, "n": n,
            "reading": f"tendencia de {verdict} (p={p:.3f})" if p < 0.05 else f"sin tendencia significativa (p={p:.3f})"}


def _cvm_stat(t: np.ndarray, T: float, beta_bar: float) -> float:
    n = t.size
    i = np.arange(1, n + 1)
    return float(1.0 / (12.0 * n) + np.sum((((t / T) ** beta_bar) - (2 * i - 1) / (2.0 * n)) ** 2))


def crow_amsaa_gof_mc(times: Sequence[float], T: float, *, n_sim: int = 2000, seed: int = 0) -> dict:
    """Bondad de ajuste Cramér-von Mises (terminación por tiempo) con p-valor por Monte Carlo.

    Se usa simulación bajo H0 en vez de tablas: con β estimado, (t_i/T)^β son estadísticos de
    orden uniformes y la distribución del estadístico no depende del β verdadero.
    p pequeño => el modelo de ley de potencia no describe bien los datos.
    """
    t, T = _clean(times, T, "time")
    n = t.size
    S = np.log(T / t).sum()
    obs = _cvm_stat(t, T, (n - 1) / S)
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n_sim):
        u = np.sort(rng.uniform(size=n))
        ts = T * u  # HPP (β0=1) condicionado a n eventos en (0,T]
        Ss = np.log(T / ts).sum()
        if _cvm_stat(ts, T, (n - 1) / Ss) >= obs:
            count += 1
    return {"statistic": obs, "p_value": (count + 1) / (n_sim + 1), "n_sim": n_sim, "seed": seed}


def mean_cumulative_function(event_times: Sequence[Sequence[float]], end_times: Sequence[float]) -> dict:
    """MCF no paramétrica (Nelson) para varias unidades reparables con censura.

    event_times[k]: tiempos acumulados de falla de la unidad k; end_times[k]: fin de observación.
    MCF(t) = Σ_{t_j<=t} 1/n_j, con n_j = unidades aún observadas en t_j.
    Sin IC aquí (requiere estimador de varianza de Lawless-Nadeau; no se inventa uno).
    """
    if len(event_times) != len(end_times):
        raise ValueError("event_times y end_times deben tener igual longitud")
    ends = np.asarray(end_times, float)
    pairs = []
    for k, ev in enumerate(event_times):
        for x in ev:
            if x <= 0 or x > ends[k]:
                raise ValueError(f"evento {x} fuera de (0, fin observación] en unidad {k}")
            pairs.append(x)
    if not pairs:
        raise ValueError("no hay eventos")
    times = np.unique(pairs)
    mcf, cum = [], 0.0
    for tj in times:
        d_j = sum(int(np.sum(np.asarray(ev) == tj)) for ev in event_times)
        at_risk = int(np.sum(ends >= tj))
        cum += d_j / at_risk
        mcf.append(cum)
    return {"time": times, "mcf": np.array(mcf), "n_units": len(end_times)}
