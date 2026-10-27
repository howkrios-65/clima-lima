"""Auditoría de calidad de datos (fase 2 del método): la calidad es un hallazgo, no un trámite."""
from __future__ import annotations

import numpy as np
import pandas as pd


def audit(df: pd.DataFrame, *, date_cols: tuple[str, ...] = (), key_cols: tuple[str, ...] = (),
          critical_cols: tuple[str, ...] = ()) -> dict:
    """Perfil de calidad: nulos por campo, duplicados, rango de fechas e inconsistencias de fecha.

    Devuelve {'columns': DataFrame, 'summary': dict, 'flags': [str]}. `flags` lista lo que
    debe reportarse en el informe como limitación (p. ej. >20 % de nulos en un campo crítico).
    """
    n = len(df)
    if n == 0:
        raise ValueError("el DataFrame está vacío")
    cols = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_pct": df.isna().mean() * 100,
        "n_unique": df.nunique(dropna=True),
    })
    summary = {"rows": n, "columns": df.shape[1],
               "duplicate_rows": int(df.duplicated().sum())}
    if key_cols:
        summary["duplicate_keys"] = int(df.duplicated(subset=list(key_cols)).sum())
    flags = []
    for c in date_cols:
        s = pd.to_datetime(df[c], errors="coerce")
        bad = int((s.isna() & df[c].notna()).sum())
        summary[f"{c}_min"], summary[f"{c}_max"] = s.min(), s.max()
        summary[f"{c}_unparseable"] = bad
        if bad:
            flags.append(f"{c}: {bad} valores no interpretables como fecha")
    for a, b in zip(date_cols[::2], date_cols[1::2]):
        sa, sb = pd.to_datetime(df[a], errors="coerce"), pd.to_datetime(df[b], errors="coerce")
        inv = int((sb < sa).sum())
        summary[f"{a}_after_{b}"] = inv
        if inv:
            flags.append(f"{inv} filas con {b} < {a} (fechas invertidas)")
    for c in critical_cols:
        pct = cols.loc[c, "missing_pct"]
        if pct > 20:
            flags.append(f"campo crítico '{c}' con {pct:.0f} % de faltantes: limita la confianza de todo ranking")
    if summary["duplicate_rows"]:
        flags.append(f"{summary['duplicate_rows']} filas duplicadas exactas")
    return {"columns": cols, "summary": summary, "flags": flags}


def audit_recurrent(df: pd.DataFrame, unit: str, time: str, status: str, *, event_value=1, censor_value=0,
                    fence: float = 1.5, ages=None) -> dict:
    """Auditoría de datos de eventos recurrentes (equipos reparables, varias unidades con censura).

    Formato esperado: una fila por evento (status=event_value) y UNA fila de fin de observación por unidad
    (status=censor_value) con el tiempo en que se dejó de observar. Detecta lo que `audit` no ve:
    unidades sin fin de observación o con varios, eventos posteriores al fin, eventos simultáneos
    (mismo tiempo en la misma unidad), códigos de estado ajenos, tiempos no positivos, fines de observación
    atípicos (cerca de la regla de Tukey, convención declarada) y unidades en riesgo por edad.
    Devuelve {'units': DataFrame, 'summary': dict, 'flags': [str], 'at_risk': DataFrame}.
    """
    d = df[[unit, time, status]].dropna().copy()
    if d.empty:
        raise ValueError("no hay filas válidas")
    flags = []
    codes = set(d[status].unique())
    foreign = codes - {event_value, censor_value}
    if foreign:
        flags.append("códigos de estado ajenos: " + str(sorted((c.item() if hasattr(c, "item") else c for c in foreign), key=str)))
    if (d[time] <= 0).any():
        flags.append(f"{int((d[time] <= 0).sum())} filas con tiempo <= 0")
    ev = d[d[status] == event_value]
    ce = d[d[status] == censor_value]
    n_units = d[unit].nunique()
    ncens = ce.groupby(unit).size().reindex(d[unit].unique(), fill_value=0)
    no_end = ncens[ncens == 0].index.tolist()
    multi_end = ncens[ncens > 1].index.tolist()
    if no_end:
        flags.append(f"{len(no_end)} unidades sin fila de fin de observación (no se puede construir T_k): {no_end[:10]}")
    if multi_end:
        flags.append(f"{len(multi_end)} unidades con más de un fin de observación: {multi_end[:10]}")
    end = ce.groupby(unit)[time].max()
    after = ev.join(end.rename("T_k"), on=unit)
    after = after[after["T_k"].notna() & (after[time] > after["T_k"])]
    if len(after):
        flags.append(f"{len(after)} eventos posteriores al fin de observación de su unidad (datos inconsistentes)")
    at_end = ev.join(end.rename("T_k"), on=unit)
    n_at_end = int((at_end["T_k"].notna() & (at_end[time] == at_end["T_k"])).sum())
    sim = ev[ev.duplicated([unit, time], keep=False)]
    n_sim_groups = int(sim.groupby([unit, time]).ngroups) if len(sim) else 0
    if n_sim_groups:
        flags.append(f"{n_sim_groups} grupos de eventos simultáneos ({len(sim)} filas): se conservan como eventos separados; "
                     "haga sensibilidad colapsándolos")
    counts = ev.groupby(unit).size().reindex(d[unit].unique(), fill_value=0)
    units = pd.DataFrame({"n_events": counts, "T_k": end.reindex(counts.index)})
    q1, q3 = units["T_k"].quantile([0.25, 0.75])
    lo, hi = q1 - fence * (q3 - q1), q3 + fence * (q3 - q1)
    units["censura_atipica"] = np.where(units["T_k"] < lo, "temprana", np.where(units["T_k"] > hi, "tardía", ""))
    early = units.index[units["censura_atipica"] == "temprana"].tolist()
    if early:
        flags.append(f"{len(early)} fines de observación atípicamente tempranos (regla de Tukey, convención): {early[:10]}; "
                     "pueden ser salidas por otra causa y no cierre de ventana")
    ages = np.asarray(ages if ages is not None else np.arange(100, units["T_k"].max() + 100, 100), float)
    at_risk = pd.DataFrame({"edad": ages, "unidades_en_riesgo": [(units["T_k"] >= a).sum() for a in ages]})
    summary = {"units": int(n_units), "rows": int(len(d)), "events": int(len(ev)), "units_without_events": int((counts == 0).sum()),
               "max_events_per_unit": int(counts.max()), "mean_events_per_unit": float(counts.mean()),
               "events_at_end_time": n_at_end, "simultaneous_groups": n_sim_groups,
               "T_k_min": float(units["T_k"].min()), "T_k_median": float(units["T_k"].median()),
               "T_k_max": float(units["T_k"].max()), "tukey_fence": (float(lo), float(hi))}
    return {"units": units, "summary": summary, "flags": flags, "at_risk": at_risk}
