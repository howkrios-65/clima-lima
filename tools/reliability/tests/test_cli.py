import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, "-m", "reliability_kit", *map(str, args)], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def test_cli_weibull_and_pareto_and_crow(tmp_path):
    rng = np.random.default_rng(0)
    life = 100 * rng.weibull(2.0, 60)
    pd.DataFrame({"t": np.minimum(life, 110), "c": (life > 110).astype(int)}).to_csv(tmp_path / "w.csv", index=False)
    out = json.loads(run("weibull", tmp_path / "w.csv", "--time", "t", "--censored", "c"))
    assert 1.4 < out["beta"] < 2.8 and out["beta_ci95_LR"][0] < out["beta"] < out["beta_ci95_LR"][1]
    pd.DataFrame({"a": list("aaabbc")}).to_csv(tmp_path / "p.csv", index=False)
    assert "vital_few" in run("pareto", tmp_path / "p.csv", "--group", "a")
    pd.DataFrame({"t": np.cumsum(np.linspace(20, 3, 15))}).to_csv(tmp_path / "n.csv", index=False)
    out = json.loads(run("crow-amsaa", tmp_path / "n.csv", "--time", "t", "--T", 200))
    assert out["n"] == 15 and "trend" in out
