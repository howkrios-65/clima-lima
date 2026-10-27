"""Análisis de series de condición (vibración, temperatura, proceso, aceite): línea base robusta, primera alarma,
tendencia, correlación y comparación de periodos.

Todo es descriptivo y retrospectivo. Una sola falla (n=1) NO valida un modelo: las funciones devuelven advertencias
y el informe las muestra. Las series diarias están autocorrelacionadas, por lo que los valores p de tendencia y correlación
son optimistas; se reporta el tamaño del efecto y un intervalo, no solo el p.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

MAD_ESCALA = 1.4826  # MAD -> desviación estándar bajo normalidad


def _x(x) -> np.ndarray:
    a = np.asarray(x, float)
    if a.ndim != 1 or a.size == 0:
        raise ValueError("la serie debe ser un vector no vacío")
    return a


def linea_base(x, n: int) -> dict:
    """Mediana y sigma robusta (MAD) de los primeros n puntos válidos."""
    a = _x(x)
    w = a[:n][np.isfinite(a[:n])]
    if w.size < 5:
        raise ValueError("la ventana de línea base necesita al menos 5 puntos válidos")
    med = float(np.median(w))
    sigma = float(MAD_ESCALA * np.median(np.abs(w - med)))
    if sigma == 0:
        sigma = float(np.std(w, ddof=1)) or 1e-12
    return {"mediana": med, "sigma": sigma, "n": int(w.size)}


def primer_cruce(x, umbral: float, persistencia: int = 1) -> int | None:
    """Índice del primer instante en que la serie supera `umbral` durante `persistencia` puntos seguidos (None si nunca)."""
    a = _x(x)
    run = 0
    for i, v in enumerate(a):
        run = run + 1 if (np.isfinite(v) and v > umbral) else 0
        if run >= persistencia:
            return i - persistencia + 1
    return None


def cusum_primera_alarma(x, mu0: float, sigma: float, k: float = 0.5, h: float = 5.0) -> int | None:
    """CUSUM unilateral superior en unidades de sigma. Devuelve el índice de la primera alarma (None si no hay)."""
    a = _x(x)
    s = 0.0
    for i, v in enumerate(a):
        if not np.isfinite(v):
            continue
        s = max(0.0, s + (v - mu0) / sigma - k)
        if s > h:
            return i
    return None


def mann_kendall(x) -> dict:
    """Prueba de Mann-Kendall con corrección por empates y pendiente de Sen (mediana de pendientes por pares)."""
    a = _x(x)
    a = a[np.isfinite(a)]
    n = a.size
    if n < 8:
        raise ValueError("Mann-Kendall requiere al menos 8 puntos")
    diff = a[None, :] - a[:, None]
    iu = np.triu_indices(n, 1)
    d = diff[iu]
    S = float(np.sum(np.sign(d)))
    _, cnt = np.unique(a, return_counts=True)
    var = (n * (n - 1) * (2 * n + 5) - np.sum(cnt * (cnt - 1) * (2 * cnt + 5))) / 18.0
    z = 0.0 if S == 0 else (S - np.sign(S)) / np.sqrt(var)
    p = float(2 * stats.norm.sf(abs(z)))
    dx = (iu[1] - iu[0]).astype(float)
    sen = float(np.median(d / dx))
    ac1 = float(np.corrcoef(a[:-1], a[1:])[0, 1]) if np.ptp(a) > 0 else 0.0
    aviso = ("serie autocorrelada: el valor p es optimista; use la pendiente y su magnitud" if ac1 > 0.3 else None)
    return {"S": S, "z": float(z), "p_value": p, "tau": float(S / (n * (n - 1) / 2)), "pendiente_sen": sen, "n": int(n),
            "autocorrelacion_lag1": ac1, "aviso": aviso}


def spearman_bootstrap(x, y, n_boot: int = 2000, conf: float = 0.95, seed: int = 0) -> dict:
    """Correlación de Spearman con IC bootstrap por pares (no respeta la dependencia temporal: se declara)."""
    x, y = _x(x), _x(y)
    if x.size != y.size:
        raise ValueError("x e y deben tener la misma longitud")
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if x.size < 10:
        raise ValueError("se requieren al menos 10 pares")
    rho, p = stats.spearmanr(x, y)
    rng = np.random.default_rng(seed)
    r = []
    for _ in range(n_boot):
        i = rng.integers(0, x.size, x.size)
        if np.ptp(x[i]) == 0 or np.ptp(y[i]) == 0:
            continue
        r.append(stats.spearmanr(x[i], y[i])[0])
    a = (1 - conf) / 2
    lo, hi = np.quantile(r, [a, 1 - a])
    return {"rho": float(rho), "p_value": float(p), "ic": (float(lo), float(hi)), "n": int(x.size), "semilla": seed,
            "aviso": "correlación no implica causa; las series diarias están autocorrelacionadas"}


def comparar_periodos(antes, despues, n_boot: int = 2000, seed: int = 0) -> dict:
    """Cambio entre dos periodos: Mann-Whitney, desplazamiento de Hodges-Lehmann, tamaño de efecto (rango biserial) e IC bootstrap."""
    a, b = _x(antes), _x(despues)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if a.size < 5 or b.size < 5:
        raise ValueError("cada periodo necesita al menos 5 puntos")
    u, p = stats.mannwhitneyu(b, a, alternative="two-sided")
    hl = float(np.median((b[:, None] - a[None, :]).ravel()))
    rbc = float(2 * u / (a.size * b.size) - 1)     # >0: 'despues' tiende a ser mayor
    rng = np.random.default_rng(seed)
    d = [np.median(rng.choice(b, b.size)) - np.median(rng.choice(a, a.size)) for _ in range(n_boot)]
    lo, hi = np.quantile(d, [0.025, 0.975])
    return {"mediana_antes": float(np.median(a)), "mediana_despues": float(np.median(b)), "desplazamiento_hl": hl,
            "rango_biserial": rbc, "p_value": float(p), "ic_dif_medianas": (float(lo), float(hi)),
            "n_antes": int(a.size), "n_despues": int(b.size), "semilla": seed}


def deteccion_retrospectiva(fechas, x, n_base: int, k: float, indice_falla: int | None = None, persistencia: int = 2) -> dict:
    """Con qué antelación habría alertado una regla simple. Retrospectivo e in-sample: con un solo evento no valida nada."""
    a = _x(x)
    lb = linea_base(a, n_base)
    umbral = lb["mediana"] + k * lb["sigma"]
    i_u = primer_cruce(a, umbral, persistencia)
    i_c = cusum_primera_alarma(a, lb["mediana"], lb["sigma"])
    fin = indice_falla if indice_falla is not None else a.size - 1
    out = {"linea_base": lb, "umbral": float(umbral), "k": k, "persistencia": persistencia,
           "indice_alarma_umbral": i_u, "indice_alarma_cusum": i_c,
           "fecha_alarma_umbral": None if i_u is None else str(fechas[i_u]),
           "fecha_alarma_cusum": None if i_c is None else str(fechas[i_c]),
           "dias_antelacion_umbral": None if i_u is None else int(fin - i_u),
           "dias_antelacion_cusum": None if i_c is None else int(fin - i_c),
           "advertencia": "análisis retrospectivo con un solo evento: no estima falsas alarmas ni sensibilidad; no valida una regla"}
    return out
