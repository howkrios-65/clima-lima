import numpy as np
import pandas as pd

from reliability_kit import plots
from reliability_kit.workorders import pareto
from reliability_kit.survival import kaplan_meier


def test_plots_write_files(tmp_path):
    rng = np.random.default_rng(0)
    t = 100 * rng.weibull(2.0, 40)
    plots.weibull_probability_plot(t, path=str(tmp_path / "w.png"), dpi=80)
    plots.pareto_chart(pareto(pd.DataFrame({"a": list("aabbbc")}), "a"), "a", path=str(tmp_path / "p.png"), dpi=80)
    plots.kaplan_meier_plot(kaplan_meier(t, np.ones(40)), path=str(tmp_path / "k.png"), dpi=80)
    assert all((tmp_path / f).stat().st_size > 1000 for f in ("w.png", "p.png", "k.png"))
