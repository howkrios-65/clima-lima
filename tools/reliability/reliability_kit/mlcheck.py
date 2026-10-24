"""Utilidades de validación para modelos predictivos: particiones sin fuga y métricas para clases raras."""
from __future__ import annotations

import numpy as np
import pandas as pd


def temporal_split(df: pd.DataFrame, time_col: str, test_frac: float = 0.2, gap: pd.Timedelta | None = None):
    """Partición out-of-time: el test es SIEMPRE posterior al entrenamiento (opcionalmente con hueco `gap`
    para evitar que ventanas de predicción solapen la frontera)."""
    if not 0 < test_frac < 1:
        raise ValueError("test_frac en (0,1)")
    d = df.sort_values(time_col)
    cut = d[time_col].iloc[int(len(d) * (1 - test_frac))]
    train = d[d[time_col] < (cut - gap if gap is not None else cut)]
    test = d[d[time_col] >= cut]
    if train.empty or test.empty:
        raise ValueError("partición vacía; revise test_frac/gap")
    return train, test


def group_split(df: pd.DataFrame, group_col: str, test_frac: float = 0.2, seed: int = 0):
    """Partición por activo/sesión: ninguna unidad aparece en ambos conjuntos (evalúa generalización a unidades no vistas)."""
    groups = df[group_col].dropna().unique()
    if groups.size < 2:
        raise ValueError("se requieren >= 2 grupos")
    rng = np.random.default_rng(seed)
    rng.shuffle(groups)
    k = max(1, int(round(groups.size * test_frac)))
    test_g = set(groups[:k])
    mask = df[group_col].isin(test_g)
    return df[~mask], df[mask]


def assert_no_overlap(train: pd.DataFrame, test: pd.DataFrame, col: str) -> None:
    """Falla si algún valor de `col` (id de activo, id de ventana…) está en train y test."""
    common = set(train[col].dropna()) & set(test[col].dropna())
    if common:
        raise AssertionError(f"fuga: {len(common)} valores de '{col}' aparecen en train y test")


def _check(y, s):
    y = np.asarray(y).astype(int); s = np.asarray(s, float)
    if y.shape != s.shape or y.ndim != 1:
        raise ValueError("y_true y score deben ser vectores iguales")
    if y.sum() == 0 or y.sum() == y.size:
        raise ValueError("se necesitan ambas clases en y_true")
    return y, s


def pr_metrics(y_true, y_score) -> dict:
    """Precisión-recall: AP (PR-AUC como precisión media), línea base = prevalencia. No usar accuracy en clases raras."""
    y, s = _check(y_true, y_score)
    order = np.argsort(-s, kind="stable")
    y_o = y[order]
    tp = np.cumsum(y_o); fp = np.cumsum(1 - y_o)
    precision = tp / (tp + fp)
    recall = tp / y.sum()
    # AP = Σ (R_k - R_{k-1}) P_k; los empates de score se tratan en bloque
    s_o = s[order]
    last = np.r_[s_o[1:] != s_o[:-1], True]
    p, r = precision[last], recall[last]
    ap = float(np.sum(np.diff(np.r_[0.0, r]) * p))
    return {"average_precision": ap, "prevalence": float(y.mean()), "n": int(y.size), "n_positive": int(y.sum())}


def recall_at_precision(y_true, y_score, min_precision: float) -> dict:
    """Mayor recall alcanzable con precisión >= min_precision y el umbral que lo logra."""
    y, s = _check(y_true, y_score)
    best = {"recall": 0.0, "threshold": None, "precision": None}
    for th in np.unique(s)[::-1]:
        pred = s >= th
        tp = int((pred & (y == 1)).sum())
        prec = tp / pred.sum()
        rec = tp / y.sum()
        if prec >= min_precision and rec > best["recall"]:
            best = {"recall": float(rec), "threshold": float(th), "precision": float(prec)}
    return best


def brier_and_calibration(y_true, prob, n_bins: int = 10) -> dict:
    """Brier y tabla de calibración (prob. media predicha vs. frecuencia observada por bin)."""
    y, p = _check(y_true, prob)
    if p.min() < 0 or p.max() > 1:
        raise ValueError("prob debe estar en [0,1]")
    bins = np.clip((p * n_bins).astype(int), 0, n_bins - 1)
    rows = []
    for b in range(n_bins):
        m = bins == b
        if m.any():
            rows.append({"bin": b, "n": int(m.sum()), "mean_pred": float(p[m].mean()), "obs_rate": float(y[m].mean())})
    return {"brier": float(np.mean((p - y) ** 2)), "calibration": pd.DataFrame(rows)}


def cost_optimal_threshold(y_true, y_score, cost_fn: float, cost_fp: float) -> dict:
    """Umbral que minimiza el costo total FN·cost_fn + FP·cost_fp. Los costos son obligatorios (vacío si no existen)."""
    if cost_fn < 0 or cost_fp < 0:
        raise ValueError("costos no negativos")
    y, s = _check(y_true, y_score)
    best = None
    for th in np.unique(s):
        pred = s >= th
        fn = int(((~pred) & (y == 1)).sum()); fp = int((pred & (y == 0)).sum())
        c = fn * cost_fn + fp * cost_fp
        if best is None or c < best["total_cost"]:
            best = {"threshold": float(th), "total_cost": float(c), "fn": fn, "fp": fp}
    # alternativa "no alertar nunca"
    never = float(y.sum() * cost_fn)
    best["cost_never_alert"] = never
    return best
