"""Análisis Weibull con censura por derecha (IEC 61649).

Solo para ítems NO reparables (o para el primer tiempo a falla). Para sistemas reparables
con tendencia usar `nhpp.py`. Los modos de falla deben venir separados por el llamador.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import gamma, log
from typing import Sequence

import numpy as np
from scipy import optimize, stats


@dataclass
class WeibullFit:
    beta: float
    eta: float
    n: int            # unidades totales
    r: int            # fallas
    loglik: float
    method: str = "MLE"
    warnings: list[str] = field(default_factory=list)

    @property
    def n_suspensions(self) -> int:
        return self.n - self.r

    @property
    def mttf(self) -> float:
        return self.eta * gamma(1.0 + 1.0 / self.beta)

    def b_life(self, p: float) -> float:
        return weibull_b_life(self.beta, self.eta, p)

    def reliability(self, t):
        return np.exp(-(np.asarray(t, float) / self.eta) ** self.beta)

    def hazard(self, t):
        t = np.asarray(t, float)
        return (self.beta / self.eta) * (t / self.eta) ** (self.beta - 1.0)


def weibull_b_life(beta: float, eta: float, p: float) -> float:
    """Tiempo al que ha fallado la fracción p (B10 -> p=0.10)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p debe estar en (0, 1)")
    return eta * (-log(1.0 - p)) ** (1.0 / beta)


def _prepare(times, censored):
    t = np.asarray(times, dtype=float)
    if t.ndim != 1 or t.size == 0:
        raise ValueError("times debe ser un vector no vacío")
    if not np.all(np.isfinite(t)) or np.any(t <= 0):
        raise ValueError("todos los tiempos deben ser finitos y > 0")
    if censored is None:
        d = np.ones_like(t, dtype=bool)
    else:
        c = np.asarray(censored).astype(bool)
        if c.shape != t.shape:
            raise ValueError("censored debe tener la misma longitud que times")
        d = ~c  # True = falla observada
    return t, d


def fit_weibull_mle(times: Sequence[float], censored: Sequence[bool] | None = None) -> WeibullFit:
    """MLE de Weibull 2P con censura por derecha.

    `censored[i]=True` marca una suspensión (la unidad no falló en ese tiempo).
    Exige >= 2 fallas con tiempos no idénticos; con pocas fallas el MLE de β está sesgado
    al alza y el intervalo es muy ancho (se advierte).
    """
    t, d = _prepare(times, censored)
    r = int(d.sum())
    if r < 2:
        raise ValueError("se requieren al menos 2 fallas para estimar un Weibull")
    if np.ptp(t[d]) == 0:
        raise ValueError("los tiempos de falla son idénticos: β no es identificable")

    scale = t.max()
    ts = t / scale
    lts = np.log(ts)
    mean_lt_fail = lts[d].mean()

    def score(b: float) -> float:
        w = ts ** b
        return (w * lts).sum() / w.sum() - 1.0 / b - mean_lt_fail

    lo, hi = 0.02, 200.0
    if score(lo) * score(hi) > 0:
        raise ValueError("no se pudo acotar β; revise los datos")
    beta = optimize.brentq(score, lo, hi, xtol=1e-12, rtol=1e-12, maxiter=500)
    eta_s = ((ts ** beta).sum() / r) ** (1.0 / beta)
    eta = eta_s * scale
    ll = _loglik(beta, eta, t, d)
    warns = []
    if r < 10:
        warns.append(f"solo {r} fallas: resultado exploratorio, MLE de β sesgado al alza e IC amplio")
    if r / t.size < 0.2:
        warns.append("más del 80 % de los datos son suspensiones: el ajuste depende mucho del modelo")
    return WeibullFit(beta=float(beta), eta=float(eta), n=int(t.size), r=r, loglik=float(ll), warnings=warns)


def _loglik(beta: float, eta: float, t: np.ndarray, d: np.ndarray) -> float:
    r = d.sum()
    return float(r * np.log(beta) - r * beta * np.log(eta)
                 + (beta - 1.0) * np.log(t[d]).sum() - ((t / eta) ** beta).sum())


def _profile_ll(beta: float, t: np.ndarray, d: np.ndarray) -> float:
    r = d.sum()
    eta = ((t ** beta).sum() / r) ** (1.0 / beta)
    return _loglik(beta, eta, t, d)


def weibull_beta_ci_lr(times, censored=None, conf: float = 0.95) -> tuple[float, float]:
    """IC de β por razón de verosimilitud perfilada (más fiable que Wald con n pequeño)."""
    t, d = _prepare(times, censored)
    fit = fit_weibull_mle(t, ~d)
    scale = t.max()
    ts = t / scale  # el perfil es invariante a escala en β
    ll_max = _profile_ll(fit.beta, ts, d)
    crit = stats.chi2.ppf(conf, 1)

    def g(b):
        return 2.0 * (ll_max - _profile_ll(b, ts, d)) - crit

    lo = fit.beta / 2.0
    while g(lo) < 0 and lo > 1e-3:
        lo /= 2.0
    hi = fit.beta * 2.0
    while g(hi) < 0 and hi < 1e3:
        hi *= 2.0
    lower = optimize.brentq(g, lo, fit.beta) if g(lo) > 0 else lo
    upper = optimize.brentq(g, fit.beta, hi) if g(hi) > 0 else hi
    return float(lower), float(upper)


def weibull_bootstrap_ci(times, censored=None, *, stat: str = "beta", p: float = 0.10,
                         n_boot: int = 1000, conf: float = 0.95, seed: int = 0) -> dict:
    """IC bootstrap percentil por remuestreo de casos (tiempo, censura).

    stat: 'beta' | 'eta' | 'b_life' (usa p) | 'mttf'. Devuelve también cuántos
    remuestreos fallaron (menos de 2 fallas) para que no se oculten.
    """
    t, d = _prepare(times, censored)
    rng = np.random.default_rng(seed)
    vals, failed = [], 0
    for _ in range(n_boot):
        idx = rng.integers(0, t.size, t.size)
        try:
            f = fit_weibull_mle(t[idx], ~d[idx])
        except ValueError:
            failed += 1
            continue
        vals.append({"beta": f.beta, "eta": f.eta, "mttf": f.mttf}.get(stat) if stat != "b_life" else f.b_life(p))
    if len(vals) < max(20, n_boot // 2):
        raise ValueError("demasiados remuestreos inválidos; datos insuficientes para bootstrap")
    a = (1 - conf) / 2
    lo, hi = np.quantile(vals, [a, 1 - a])
    point = fit_weibull_mle(t, ~d)
    est = {"beta": point.beta, "eta": point.eta, "mttf": point.mttf}.get(stat) if stat != "b_life" else point.b_life(p)
    return {"estimate": float(est), "lower": float(lo), "upper": float(hi),
            "n_boot_ok": len(vals), "n_boot_failed": failed, "conf": conf}


def johnson_median_ranks(times, censored=None):
    """Rangos medianos (Bernard) con rangos ajustados de Johnson para censura.

    Devuelve (t_fallas, F) listos para el gráfico de probabilidad. Empate falla/suspensión:
    la falla se ordena primero.
    """
    t, d = _prepare(times, censored)
    order = np.lexsort((~d, t))  # por tiempo; a igual tiempo, fallas primero
    t, d = t[order], d[order]
    n = t.size
    prev = 0.0
    tf, F = [], []
    for i in range(n):
        if d[i]:
            reverse_rank = n - i
            prev = prev + (n + 1 - prev) / (1 + reverse_rank)
            tf.append(t[i])
            F.append((prev - 0.3) / (n + 0.4))
    return np.array(tf), np.array(F)


def rank_regression(times, censored=None) -> dict:
    """Regresión por rangos sobre X (RRX): ln t = a + b·ln(-ln(1-F)); β=1/b, η=e^a.

    Devuelve también r² del gráfico de probabilidad (indicador de bondad de ajuste, no
    sustituye una prueba formal).
    """
    tf, F = johnson_median_ranks(times, censored)
    if tf.size < 2:
        raise ValueError("se requieren al menos 2 fallas")
    y = np.log(-np.log(1.0 - F))
    x = np.log(tf)
    b, a = np.polyfit(y, x, 1)
    r2 = float(np.corrcoef(y, x)[0, 1] ** 2)
    return {"beta": float(1.0 / b), "eta": float(np.exp(a)), "r2": r2, "n_failures": int(tf.size),
            "method": "RRX (rangos de Johnson/Bernard)"}


# ---------- comparación de distribuciones (AIC) ----------

def _fit_exponential(t, d):
    r = d.sum()
    lam = r / t.sum()
    ll = r * np.log(lam) - lam * t.sum()
    return {"params": {"lambda": float(lam)}, "loglik": float(ll), "k": 1}


def _fit_lognormal(t, d):
    lt = np.log(t)
    mu0, s0 = lt[d].mean(), max(lt[d].std(), 1e-3)

    def nll(p):
        mu, ls = p
        s = np.exp(ls)
        z = (lt - mu) / s
        ll_f = stats.norm.logpdf(z[d]) - np.log(s) - lt[d]
        ll_c = stats.norm.logsf(z[~d])
        return -(ll_f.sum() + ll_c.sum())

    res = optimize.minimize(nll, [mu0, np.log(s0)], method="Nelder-Mead",
                            options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 5000})
    return {"params": {"mu": float(res.x[0]), "sigma": float(np.exp(res.x[1]))},
            "loglik": float(-res.fun), "k": 2}


def compare_models(times, censored=None) -> list[dict]:
    """Weibull vs lognormal vs exponencial por AIC (menor = mejor). Con censura incluida."""
    t, d = _prepare(times, censored)
    w = fit_weibull_mle(t, ~d)
    out = [
        {"model": "weibull", "params": {"beta": w.beta, "eta": w.eta}, "loglik": w.loglik, "k": 2},
        {"model": "lognormal", **_fit_lognormal(t, d)},
        {"model": "exponential", **_fit_exponential(t, d)},
    ]
    for m in out:
        m["aic"] = 2 * m["k"] - 2 * m["loglik"]
    out.sort(key=lambda m: m["aic"])
    best = out[0]["aic"]
    for m in out:
        m["delta_aic"] = m["aic"] - best
    return out


def interpret_beta(beta: float, ci: tuple[float, float] | None = None) -> str:
    """Lectura de β para la estrategia, respetando la incertidumbre.

    Si el IC contiene 1 no se puede distinguir de falla aleatoria: se dice.
    """
    if ci is not None and ci[0] <= 1.0 <= ci[1]:
        return (f"β={beta:.2f} con IC [{ci[0]:.2f}, {ci[1]:.2f}] que contiene 1: no se distingue de falla "
                "aleatoria; no hay base estadística para un reemplazo por edad.")
    if beta < 1:
        return (f"β={beta:.2f} < 1: mortalidad infantil; atacar instalación/puesta en marcha/calidad, "
                "no fijar un intervalo de reemplazo.")
    if beta <= 1.2 and ci is None:
        return f"β={beta:.2f} ≈ 1: patrón aleatorio; PM por edad poco justificado (sin IC no se puede afirmar más)."
    return (f"β={beta:.2f} > 1: desgaste; una tarea por edad puede ser técnicamente válida "
            "(verificar costos y consecuencias; ver economics.optimal_age_replacement).")
