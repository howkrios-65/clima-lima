"""CLI: python -m reliability_kit {weibull,crow-amsaa,pareto} archivo.csv ...  (salida JSON/tabla)."""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from . import (bias_correct_beta, compare_models_verdict, fit_crow_amsaa, fit_crow_amsaa_multi, fit_weibull_mle,
               interpret_beta, laplace_trend_test, laplace_trend_test_multi, pareto, unit_heterogeneity_test,
               weibull_b_life_ci_lr, weibull_beta_ci_lr)

_UNIT_HINTS = ("id", "unit", "unidad", "motor", "equipo", "equip", "asset", "activo", "tag", "engine", "serial")


def _warn(msg: str) -> None:
    print(f"ADVERTENCIA: {msg}", file=sys.stderr)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reliability_kit", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("weibull", help="Weibull MLE con censura, IC de β y B10, comparación de modelos")
    w.add_argument("csv"); w.add_argument("--time", required=True)
    w.add_argument("--censored", help="columna booleana/0-1: 1 = suspensión")
    c = sub.add_parser("crow-amsaa", help="Crow-AMSAA: una unidad (--T) o varias (--unit y --end)")
    c.add_argument("csv"); c.add_argument("--time", required=True)
    c.add_argument("--T", type=float, help="fin de observación común (una sola unidad)")
    c.add_argument("--unit", help="columna con el identificador de la unidad (modo multi-unidad)")
    c.add_argument("--end", help="columna con el fin de observación de la unidad (modo multi-unidad)")
    p = sub.add_parser("pareto", help="Pareto por activo (cuenta eventos o suma una columna)")
    p.add_argument("csv"); p.add_argument("--group", required=True); p.add_argument("--value")
    a = ap.parse_args(argv)
    df = pd.read_csv(a.csv)
    if a.cmd == "weibull":
        t = df[a.time].to_numpy()
        cens = df[a.censored].astype(bool).to_numpy() if a.censored else None
        f = fit_weibull_mle(t, cens)
        ci = weibull_beta_ci_lr(t, cens)
        out = {"beta": f.beta, "beta_ci95_LR": ci, "eta": f.eta, "n": f.n, "failures": f.r,
               "suspensions": f.n_suspensions, "B10": f.b_life(0.10), "B10_ci95_LR": weibull_b_life_ci_lr(t, cens, 0.10),
               "MTTF": f.mttf, "reading": interpret_beta(f.beta, ci), "warnings": f.warnings}
        if f.r < 30:
            out["beta_bias_corrected"] = bias_correct_beta(t, cens)
        out["model_comparison"] = compare_models_verdict(t, cens)["verdict"]
        print(json.dumps(out, indent=2, ensure_ascii=False, default=float))
    elif a.cmd == "crow-amsaa":
        if a.unit:
            if not a.end:
                ap.error("--unit requiere --end (fin de observación por unidad)")
            ev, ends = [], []
            for _, g in df.groupby(a.unit):
                ends.append(float(g[a.end].iloc[0]))
                if g[a.end].nunique() != 1:
                    _warn(f"unidad con más de un valor de --end; se usó el primero ({ends[-1]})")
                ev.append(g[a.time].dropna().to_numpy())
            f = fit_crow_amsaa_multi(ev, ends)
            out = {"model": f.model, "beta_unbiased": f.beta, "beta_ci95": f.beta_ci, "n_events": f.n_events,
                   "n_units": f.n_units, "trend": f.trend, "laplace_pooled": laplace_trend_test_multi(ev, ends),
                   "heterogeneity": unit_heterogeneity_test(ev, ends), "warnings": f.warnings}
        else:
            if a.T is None:
                ap.error("modo una unidad: se requiere --T (o use --unit y --end para varias unidades)")
            hint = [col for col in df.columns if col != a.time and any(h in col.lower() for h in _UNIT_HINTS)]
            if hint:
                _warn(f"el CSV tiene columna(s) {hint} que parecen identificar unidades; este modo asume UNA sola "
                      "unidad y mezclar varias da una tendencia engañosa. Use --unit y --end.")
            t = df[a.time].to_numpy()
            f = fit_crow_amsaa(t, a.T)
            out = {"beta_unbiased": f.beta, "beta_ci95": f.beta_ci, "lambda": f.lam, "n": f.n, "trend": f.trend,
                   "laplace": laplace_trend_test(t, a.T), "warnings": f.warnings}
        print(json.dumps(out, indent=2, ensure_ascii=False, default=float))
    else:
        print(pareto(df, a.group, a.value).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
