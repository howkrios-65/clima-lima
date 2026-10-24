"""Pareto, bad actors y crónicos a partir de un historial de OTs (DataFrame de pandas)."""
from __future__ import annotations

import pandas as pd


def pareto(df: pd.DataFrame, group: str, value: str | None = None, threshold: float = 0.8) -> pd.DataFrame:
    """Tabla de Pareto. value=None cuenta eventos. 'vital_few' incluye el elemento que cruza el umbral."""
    if group not in df.columns:
        raise KeyError(group)
    if value is None:
        g = df.groupby(group).size().astype(float)
    else:
        if value not in df.columns:
            raise KeyError(value)
        g = df.groupby(group)[value].sum(min_count=1).dropna().astype(float)
    g = g.sort_values(ascending=False)
    total = g.sum()
    if total <= 0:
        raise ValueError("el total es cero; no hay Pareto")
    out = pd.DataFrame({"total": g})
    out["share"] = out["total"] / total
    out["cum_share"] = out["share"].cumsum()
    out["vital_few"] = (out["cum_share"] - out["share"]) < threshold
    return out.reset_index()


def bad_actors(df: pd.DataFrame, asset: str, *, cost: str | None = None, downtime: str | None = None,
               threshold: float = 0.8, min_views: int | None = None) -> pd.DataFrame:
    """Cruza Paretos de frecuencia, costo y downtime. Bad actor = vital few en >= min_views vistas.

    Por defecto min_views = 2 (o 1 si solo hay una vista). El resultado prioriza para RCA; no
    declara causas raíz.
    """
    views = {"freq": pareto(df, asset, None, threshold)}
    if cost:
        views["cost"] = pareto(df, asset, cost, threshold)
    if downtime:
        views["downtime"] = pareto(df, asset, downtime, threshold)
    if min_views is None:
        min_views = min(2, len(views))
    res = None
    for name, p in views.items():
        p = p[[asset, "total", "share", "vital_few"]].rename(
            columns={"total": f"{name}_total", "share": f"{name}_share", "vital_few": f"{name}_vital"})
        res = p if res is None else res.merge(p, on=asset, how="outer")
    vital_cols = [c for c in res.columns if c.endswith("_vital")]
    res[vital_cols] = res[vital_cols].fillna(False).astype(bool)
    res["n_views"] = res[vital_cols].sum(axis=1)
    res["bad_actor"] = res["n_views"] >= min_views
    return res.sort_values(["n_views", "freq_total"], ascending=False).reset_index(drop=True)


def chronic_repeaters(df: pd.DataFrame, asset: str, code: str, date: str, *, min_repeats: int = 3,
                      window_days: int = 365) -> pd.DataFrame:
    """Activos con >= min_repeats fallas del MISMO código dentro de una ventana móvil (crónico vs. único)."""
    d = df[[asset, code, date]].dropna().copy()
    d[date] = pd.to_datetime(d[date])
    rows = []
    for (a, c), g in d.groupby([asset, code]):
        ts = g[date].sort_values().to_list()
        best = 0
        j = 0
        for i in range(len(ts)):
            while (ts[i] - ts[j]).days > window_days:
                j += 1
            best = max(best, i - j + 1)
        if best >= min_repeats:
            rows.append({asset: a, code: c, "max_repeats_in_window": best, "total_events": len(ts)})
    cols = [asset, code, "max_repeats_in_window", "total_events"]
    return pd.DataFrame(rows, columns=cols).sort_values("max_repeats_in_window", ascending=False).reset_index(drop=True)
