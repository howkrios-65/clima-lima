"""Gráficos (matplotlib opcional). Un acento + gris; cada figura lleva n y método en el pie."""
from __future__ import annotations

import numpy as np

ACCENT, GREY = "#C0392B", "#5D6D7E"


def _plt():
    import matplotlib
    import matplotlib.pyplot as plt
    return plt


def weibull_probability_plot(times, censored=None, path: str | None = None, dpi: int = 600):
    from .weibull import fit_weibull_mle, johnson_median_ranks
    plt = _plt()
    fit = fit_weibull_mle(times, censored)
    tf, F = johnson_median_ranks(times, censored)
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter(np.log(tf), np.log(-np.log(1 - F)), color=GREY, s=18, label="Rangos medianos")
    xs = np.linspace(np.log(tf.min()) - 0.2, np.log(tf.max()) + 0.2, 50)
    ax.plot(xs, fit.beta * (xs - np.log(fit.eta)), color=ACCENT, label=f"MLE β={fit.beta:.2f}, η={fit.eta:.0f}")
    ax.set_xlabel("ln(tiempo)"); ax.set_ylabel("ln(-ln(1-F))")
    ax.set_title("Gráfico de probabilidad Weibull")
    ax.legend(frameon=False)
    fig.text(0.01, 0.005, f"n={fit.n}, fallas={fit.r}, suspensiones={fit.n_suspensions}; ajuste MLE", fontsize=7, color=GREY)
    if path:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return fig


def pareto_chart(table, label_col: str, path: str | None = None, dpi: int = 600, top: int = 15):
    plt = _plt()
    t = table.head(top)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(t[label_col].astype(str), t["share"] * 100, color=[ACCENT if v else GREY for v in t["vital_few"]])
    ax.set_ylabel("% del total"); ax.tick_params(axis="x", rotation=60)
    ax2 = ax.twinx(); ax2.plot(t[label_col].astype(str), t["cum_share"] * 100, color="black", marker="o", ms=3)
    ax2.set_ylim(0, 105); ax2.set_ylabel("% acumulado")
    if path:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return fig


def kaplan_meier_plot(km, path: str | None = None, dpi: int = 600):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.step(np.r_[0, km.time], np.r_[1, km.survival], where="post", color=ACCENT)
    ax.fill_between(np.r_[0, km.time], np.r_[1, km.lower], np.r_[1, km.upper], step="post", color=GREY, alpha=0.25)
    ax.set_ylim(0, 1.02); ax.set_xlabel("tiempo"); ax.set_ylabel("S(t)")
    fig.text(0.01, 0.005, f"Kaplan-Meier, IC {int(km.conf*100)} % (log-log)", fontsize=7, color=GREY)
    if path:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return fig
