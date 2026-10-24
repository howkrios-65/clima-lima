"""Auditoría de calidad de datos (fase 2 del método): la calidad es un hallazgo, no un trámite."""
from __future__ import annotations

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
