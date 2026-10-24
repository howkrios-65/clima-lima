"""Economía de confiabilidad. Los costos NO se inventan: son parámetros obligatorios del llamador."""
from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy import integrate, optimize


def age_replacement_cost_rate(T: float, beta: float, eta: float, c_preventive: float, c_failure: float) -> float:
    """Costo esperado por unidad de tiempo con reemplazo a edad T (o a la falla, lo que ocurra antes).

    C(T) = [c_p·R(T) + c_f·F(T)] / ∫0^T R(t) dt   (Barlow-Proschan)
    """
    if T <= 0:
        raise ValueError("T debe ser > 0")
    R = lambda t: np.exp(-(t / eta) ** beta)
    mean_cycle, _ = integrate.quad(R, 0, T)
    return float((c_preventive * R(T) + c_failure * (1 - R(T))) / mean_cycle)


def optimal_age_replacement(beta: float, eta: float, c_preventive: float, c_failure: float) -> dict:
    """Edad de reemplazo óptima. Solo existe mínimo interior si β>1 y c_f > c_p.

    Si no, devuelve optimal_age=None con la razón: reemplazo por edad no se justifica, no se
    fuerza un número.
    """
    if c_preventive <= 0 or c_failure <= 0:
        raise ValueError("los costos deben ser > 0 (si no los tiene, es un vacío: no calcular)")
    if beta <= 1:
        return {"optimal_age": None, "reason": f"β={beta:.2f} ≤ 1: riesgo no creciente; el reemplazo por edad no reduce costo."}
    if c_failure <= c_preventive:
        return {"optimal_age": None, "reason": "c_failure ≤ c_preventive: esperar a la falla es igual o más barato."}
    f = lambda T: age_replacement_cost_rate(T, beta, eta, c_preventive, c_failure)
    res = optimize.minimize_scalar(f, bounds=(1e-6 * eta, 10 * eta), method="bounded",
                                   options={"xatol": 1e-9 * eta})
    run_to_failure = c_failure / (eta * _gamma1(beta))  # costo/tiempo si nunca se previene
    return {"optimal_age": float(res.x), "cost_rate": float(res.fun),
            "cost_rate_run_to_failure": float(run_to_failure),
            "saving_pct": float(100 * (1 - res.fun / run_to_failure)), "reason": "mínimo interior de C(T)"}


def _gamma1(beta: float) -> float:
    from math import gamma
    return gamma(1 + 1 / beta)


def npv(cashflows: Sequence[float], rate: float, t0: int = 0) -> float:
    """VPN de flujos anuales (flujo[k] ocurre en el año t0+k). Costos como valores positivos o negativos, a criterio del llamador."""
    if rate <= -1:
        raise ValueError("tasa inválida")
    cf = np.asarray(cashflows, float)
    return float(np.sum(cf / (1 + rate) ** (t0 + np.arange(cf.size))))


def eac(present_value: float, rate: float, years: int) -> float:
    """Costo anual equivalente (CAE/EAC) de un VPN a `years` años: PV·r/(1-(1+r)^-n)."""
    if years <= 0:
        raise ValueError("years debe ser > 0")
    if rate == 0:
        return present_value / years
    return float(present_value * rate / (1 - (1 + rate) ** (-years)))


def inherent_availability(mtbf: float, mttr: float) -> float:
    """A_i = MTBF/(MTBF+MTTR). Excluye demoras logísticas y mantenimiento preventivo."""
    if mtbf <= 0 or mttr < 0:
        raise ValueError("MTBF > 0 y MTTR ≥ 0")
    return mtbf / (mtbf + mttr)
