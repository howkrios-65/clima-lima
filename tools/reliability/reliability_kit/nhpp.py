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


def mean_cumulative_function(event_times: Sequence[Sequence[float]], end_times: Sequence[float],
                             conf: float = 0.95) -> dict:
    """MCF no paramétrica (Nelson) para varias unidades reparables con censura, con IC de Lawless-Nadeau.

    event_times[k]: tiempos acumulados de falla de la unidad k (los empates cuentan como eventos
    separados); end_times[k]: fin de observación. MCF(t) = Σ_{t_j<=t} d_j/n_j, n_j = unidades observadas
    en t_j. Varianza robusta (Lawless & Nadeau, 1995):
        Var(t) = Σ_i [ Σ_{t_j<=t} (δ_i(t_j)/n_j)·(dN_i(t_j) − d_j/n_j) ]²
    IC con transformación log (siempre positivo). Con pocas unidades en riesgo (cola) el IC no es fiable:
    'n_at_risk' se devuelve para que se vea.
    """
    if len(event_times) != len(end_times):
        raise ValueError("event_times y end_times deben tener igual longitud")
    ends = np.asarray(end_times, float)
    evs = [np.asarray(ev, float) for ev in event_times]
    for k, ev in enumerate(evs):
        if np.any(ev <= 0) or np.any(ev > ends[k]):
            raise ValueError(f"evento fuera de (0, fin observación] en unidad {k}")
    pooled = np.concatenate(evs) if evs else np.array([])
    if pooled.size == 0:
        raise ValueError("no hay eventos")
    times = np.unique(pooled)
    K = len(evs)
    # contribuciones acumuladas por unidad: matriz K x len(times)
    contrib = np.zeros((K, times.size))
    mcf, at_risk = np.zeros(times.size), np.zeros(times.size, int)
    cum = 0.0
    for j, tj in enumerate(times):
        dN = np.array([np.sum(ev == tj) for ev in evs], float)
        delta = (ends >= tj).astype(float)
        n_j = int(delta.sum())
        d_j = dN.sum()
        cum += d_j / n_j
        mcf[j], at_risk[j] = cum, n_j
        contrib[:, j] = delta / n_j * (dN - d_j / n_j)
    cs = np.cumsum(contrib, axis=1)
    var = np.sum(cs ** 2, axis=0)
    se = np.sqrt(var)
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    with np.errstate(divide="ignore", invalid="ignore"):
        w = np.where(mcf > 0, np.exp(z * se / mcf), np.nan)
    lower, upper = mcf / w, mcf * w
    return {"time": times, "mcf": mcf, "se": se, "lower": lower, "upper": upper, "n_at_risk": at_risk,
            "n_units": K, "conf": conf, "method": "Nelson + varianza Lawless-Nadeau, IC log"}


# ---------- varias unidades reparables con fin de observación distinto ----------

@dataclass
class MultiCrowAmsaaFit:
    beta: float
    beta_mle: float
    beta_ci: tuple[float, float]
    n_events: int
    n_units: int
    n_units_with_events: int
    model: str
    conf: float
    warnings: list[str] = field(default_factory=list)

    @property
    def trend(self) -> str:
        lo, hi = self.beta_ci
        if hi < 1:
            return "mejora (β<1, IC por debajo de 1)"
        if lo > 1:
            return "deterioro (β>1, IC por encima de 1)"
        return "sin tendencia distinguible de 1 (IC contiene 1)"


def _multi_prepare(event_times, end_times):
    if len(event_times) != len(end_times) or len(end_times) == 0:
        raise ValueError("event_times y end_times deben ser listas no vacías de igual longitud")
    ends = np.asarray(end_times, float)
    if np.any(ends <= 0):
        raise ValueError("los fines de observación deben ser > 0")
    evs = []
    for k, ev in enumerate(event_times):
        ev = np.sort(np.asarray(ev, float))
        if np.any(ev <= 0) or np.any(ev > ends[k]):
            raise ValueError(f"evento fuera de (0, T_k] en unidad {k}")
        evs.append(ev)
    return evs, ends


def fit_crow_amsaa_multi(event_times, end_times, *, model: str = "conditional", unbiased: bool = True,
                         conf: float = 0.95) -> MultiCrowAmsaaFit:
    """Crow-AMSAA para K unidades con T_k distintos.

    model='conditional' (recomendado): cada unidad tiene su propia tasa base (libre) y β común. Condicionando
    en N_k, u=t/T_k son iid con CDF u^β ⇒ 2βS ~ χ²(2N), S=Σln(T_k/t), IC exacto y robusto a diferencias de
    nivel entre unidades. Las unidades sin eventos no aportan (se declara).
    model='common': λ común (MIL-HDBK-189 multi-sistema), IC por razón de verosimilitud; supone unidades
    homogéneas (ver unit_heterogeneity_test).
    """
    evs, ends = _multi_prepare(event_times, end_times)
    N = int(sum(ev.size for ev in evs))
    if N < 3:
        raise ValueError("se requieren al menos 3 eventos en total")
    with_ev = int(sum(ev.size > 0 for ev in evs))
    warns = [f"{len(evs) - with_ev} de {len(evs)} unidades sin eventos"] if with_ev < len(evs) and model == "conditional" else []
    if N < 10:
        warns.append(f"solo {N} eventos: exploratorio")
    if model == "conditional":
        S = float(sum(np.log(ends[k] / ev).sum() for k, ev in enumerate(evs) if ev.size))
        if S <= 0:
            raise ValueError("S=0: todos los eventos coinciden con el fin de observación")
        beta_mle = N / S
        beta = (N - 1) / S if unbiased else beta_mle
        a = (1 - conf) / 2
        ci = (float(stats.chi2.ppf(a, 2 * N) / (2 * S)), float(stats.chi2.ppf(1 - a, 2 * N) / (2 * S)))
        return MultiCrowAmsaaFit(float(beta), float(beta_mle), ci, N, len(evs), with_ev, "conditional", conf, warns)
    if model != "common":
        raise ValueError("model debe ser 'conditional' o 'common'")
    sum_ln_t = float(sum(np.log(ev).sum() for ev in evs))
    lnT = np.log(ends)

    def score(b):
        w = ends ** b
        return N / b + sum_ln_t - N * (w * lnT).sum() / w.sum()

    from scipy import optimize
    beta_mle = float(optimize.brentq(score, 0.05, 20.0, xtol=1e-12))

    def prof(b):
        w = (ends ** b).sum()
        return N * np.log(N / w) + N * np.log(b) + (b - 1) * sum_ln_t - N

    ll_max = prof(beta_mle)
    crit = stats.chi2.ppf(conf, 1)
    g = lambda b: 2 * (ll_max - prof(b)) - crit
    lo, hi = beta_mle / 2, beta_mle * 2
    for _ in range(40):
        if g(lo) > 0: break
        lo /= 2
    for _ in range(40):
        if g(hi) > 0: break
        hi *= 2
    ci = (float(optimize.brentq(g, lo, beta_mle)), float(optimize.brentq(g, beta_mle, hi)))
    warns.append("λ común: supone unidades homogéneas; contraste con model='conditional'")
    beta = beta_mle * (N - 1) / N if unbiased else beta_mle  # corrección aproximada, declarada
    return MultiCrowAmsaaFit(float(beta), beta_mle, ci, N, len(evs), with_ev, "common", conf, warns)


def laplace_trend_test_multi(event_times, end_times) -> dict:
    """Laplace agrupada: bajo HPP, u=t/T_k ~ U(0,1) condicional ⇒ U=Σ(u−½)/√(N/12) ~ N(0,1).
    U>0 deterioro, U<0 mejora. Aproximación normal razonable desde ~10 eventos totales."""
    evs, ends = _multi_prepare(event_times, end_times)
    u = np.concatenate([ev / ends[k] for k, ev in enumerate(evs) if ev.size])
    N = u.size
    if N < 4:
        raise ValueError("se requieren al menos 4 eventos")
    U = float((u - 0.5).sum() / np.sqrt(N / 12.0))
    p = float(2 * stats.norm.sf(abs(U)))
    return {"U": U, "p_value": p, "n_events": int(N),
            "reading": ("deterioro" if U > 0 else "mejora") + f" (p={p:.3f})" if p < 0.05 else f"sin tendencia significativa (p={p:.3f})"}


def unit_heterogeneity_test(event_times, end_times, *, n_sim: int = 5000, seed: int = 0) -> dict:
    """¿Las unidades tienen la misma tasa? X² de Pearson de conteos por unidad vs. esperado ∝ T_k,
    con p por Monte Carlo (multinomial condicional al total). p pequeño ⇒ heterogeneidad (o tendencia
    fuerte con T_k desiguales); entonces el modelo 'common' no es defendible."""
    evs, ends = _multi_prepare(event_times, end_times)
    counts = np.array([ev.size for ev in evs], float)
    N = int(counts.sum())
    if N < 3:
        raise ValueError("se requieren al menos 3 eventos")
    prob = ends / ends.sum()
    expected = N * prob
    stat = float(np.sum((counts - expected) ** 2 / expected))
    rng = np.random.default_rng(seed)
    sims = rng.multinomial(N, prob, size=n_sim)
    sim_stat = np.sum((sims - expected) ** 2 / expected, axis=1)
    return {"statistic": stat, "p_value": float((np.sum(sim_stat >= stat) + 1) / (n_sim + 1)),
            "dispersion_index": float(counts.var(ddof=1) / counts.mean()) if counts.mean() > 0 else float("nan"),
            "n_sim": n_sim}
