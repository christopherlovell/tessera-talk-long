#!/usr/bin/env python3
"""Export component-consumable JSON for the deck.

This is the data pipeline boundary: anything a Vue component plots is
written here as plain JSON into public/data/, so components never touch
simulation outputs directly. Re-run whenever the upstream data changes.

Currently writes hmf_demo.json with TOY analytic (Schechter-like) HMFs
on a (sigma8, omega_m) grid — replace `toy_hmf` with a call to the real
emulator (e.g. load the trained flow and evaluate on the same grid).

Schema consumed by components/HmfSlider.vue:
    {
      "sigma8_grid":  [S floats],
      "omega_m_grid": [O floats],
      "log_m":        [K floats],        # log10 M/Msun bin centres
      "log_dn_range": [lo, hi],          # fixed y-axis range for plotting
      "curves":       [S][O][K] floats   # log10 dn/dlogM
    }
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "data"


def toy_hmf(log_m, sigma8, omega_m):
    """Toy Schechter-like HMF: normalisation ~ omega_m, knee ~ sigma8.

    TODO: replace with real emulator predictions.
    """
    log_mstar = 13.4 + 3.0 * (sigma8 - 0.8)   # sigma8 moves the exponential knee
    log_a = -2.6 + 1.2 * (omega_m - 0.3) / 0.1  # omega_m scales the normalisation
    out = []
    for lm in log_m:
        x = 10 ** (lm - log_mstar)
        val = log_a - 0.9 * (lm - 12.0) - x / math.log(10)
        out.append(round(val, 4))
    return out


def main():
    sigma8_grid = [0.70 + 0.02 * i for i in range(11)]   # 0.70 .. 0.90
    omega_m_grid = [0.20 + 0.02 * i for i in range(11)]  # 0.20 .. 0.40
    log_m = [12.0 + 0.1 * i for i in range(36)]          # 12 .. 15.5

    curves = [[toy_hmf(log_m, s8, om) for om in omega_m_grid] for s8 in sigma8_grid]

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "hmf_demo.json"
    path.write_text(json.dumps({
        "sigma8_grid": [round(v, 3) for v in sigma8_grid],
        "omega_m_grid": [round(v, 3) for v in omega_m_grid],
        "log_m": [round(v, 2) for v in log_m],
        "log_dn_range": [-9.0, -1.5],
        "curves": curves,
    }))
    print(f"wrote {path} ({path.stat().st_size / 1024:.0f} kB)")


if __name__ == "__main__":
    main()
