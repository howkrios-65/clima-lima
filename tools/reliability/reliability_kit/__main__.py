"""CLI: python -m reliability_kit {weibull,crow-amsaa,pareto} archivo.csv ...  (salida JSON/tabla)."""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from . import fit_crow_amsaa, fit_weibull_mle, interpret_beta, laplace_trend_test, pareto, weibull_beta_ci_lr


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reliability_kit", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("weibull", help="Weibull MLE con censura + IC de β por razón de verosimilitud")
    w.add_argument("csv"); w.add_argument("--time", required=True)
    w.add_argument("--censored", help="columna booleana/0-1: 1 = suspensión")
    c = sub.add_parser("crow-amsaa", help="Crow-AMSAA de una unidad reparable (tiempos acumulados)")
    c.add_argument("csv"); c.add_argument("--time", required=True)
    c.add_argument("--T", type=float, required=True, help="fin de observación (terminación por tiempo)")
    p = sub.add_parser("pareto", help="Pareto por activo (cuenta eventos o suma una columna)")
    p.add_argument("csv"); p.add_argument("--group", required=True); p.add_argument("--value")
    a = ap.parse_args(argv)
    df = pd.read_csv(a.csv)
    if a.cmd == "weibull":
        cens = df[a.censored].astype(bool).to_numpy() if a.censored else None
        f = fit_weibull_mle(df[a.time].to_numpy(), cens)
        ci = weibull_beta_ci_lr(df[a.time].to_numpy(), cens)
        print(json.dumps({"beta": f.beta, "beta_ci95_LR": ci, "eta": f.eta, "n": f.n, "failures": f.r,
                          "suspensions": f.n_suspensions, "B10": f.b_life(0.10), "MTTF": f.mttf,
                          "reading": interpret_beta(f.beta, ci), "warnings": f.warnings}, indent=2, ensure_ascii=False))
    elif a.cmd == "crow-amsaa":
        t = df[a.time].to_numpy()
        f = fit_crow_amsaa(t, a.T)
        print(json.dumps({"beta_unbiased": f.beta, "beta_ci95": f.beta_ci, "lambda": f.lam, "n": f.n,
                          "trend": f.trend, "laplace": laplace_trend_test(t, a.T), "warnings": f.warnings},
                         indent=2, ensure_ascii=False))
    else:
        print(pareto(df, a.group, a.value).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
