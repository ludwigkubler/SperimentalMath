"""
Extended empirical study of Maslov-dequantized Fourier coefficient
self-convolution doubling law on Z_n.

Building on entry e14f176e4ef1, this script:
  1. tests larger n: [8, 16, 32, 64, 128, 256]
  2. tests larger beta range: [5, 10, 20, 40, 80, 160]
  3. measures the actual scaling of |MinFC(g) - 2*MinFC(f)| as a
     function of (beta, n)
  4. fits a power law log(err) = alpha * log(n) + c at each beta
     to extract the empirical rate
  5. writes a JSON summary for the paper

This is the data-collection script for the standalone paper that
replaces the trivial-refutation framing of the original notebook entry.
"""
import json
import math
import random
import time
from pathlib import Path

# Reuse the proven primitives from the audited test
import sys
sys.path.insert(0, str(Path(__file__).parent))
from test_e14f176e4ef1 import (
    tropical_convolution,
    min_fourier_coeff,
    discrepancy,
)
import cmath


def tropical_fourier_transform(f, beta, n):
    """
    Numerically stabilized Maslov-dequantized TFT magnitude.

    F_β[f](k) = -(1/β) log( Σ_x exp(-β·f[x]) · exp(-2πikx/n) )
              = min(f) - (1/β) log( Σ_x exp(-β·(f[x] - min(f))) · exp(-2πikx/n) )

    The shift by min(f) keeps every exponent ≤ 0 (so weights ∈ (0, 1]),
    avoiding the math range error that plagues naive evaluation at large β.

    Returns list of |F_β[f](k)| for k = 0..n-1.
    """
    fmin = min(f)
    mags = []
    for k in range(n):
        re_s = 0.0
        im_s = 0.0
        for x in range(n):
            w = math.exp(-beta * (f[x] - fmin))   # ∈ (0, 1]
            angle = -2.0 * math.pi * k * x / n
            re_s += w * math.cos(angle)
            im_s += w * math.sin(angle)
        s = complex(re_s, im_s)
        if abs(s) < 1e-290:
            mags.append(float("inf"))
            continue
        log_s = cmath.log(s)
        coeff = fmin - (1.0 / beta) * log_s     # complex coefficient
        mags.append(abs(coeff))
    return mags


def run_one(n, beta, n_polys, seed):
    rng = random.Random(seed)
    errors = []
    for _ in range(n_polys):
        f = [float(rng.randint(-10, 10)) for _ in range(n)]
        g = tropical_convolution(f, n)
        Ff = tropical_fourier_transform(f, beta, n)
        Fg = tropical_fourier_transform(g, beta, n)
        mf = min_fourier_coeff(Ff)
        mg = min_fourier_coeff(Fg)
        if not (math.isfinite(mf) and math.isfinite(mg)):
            continue
        err = abs(mg - 2.0 * mf)
        errors.append(err)
    return errors


def percentile(xs, q):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - k) + xs[hi] * (k - lo)


def main():
    ns = [8, 16, 32, 64, 128, 256]
    betas = [5.0, 10.0, 20.0, 40.0, 80.0, 160.0]
    n_polys = 50
    seed = 17  # different from the audit seeds

    grid = {}  # (n, beta) -> stats

    t0 = time.time()
    for n in ns:
        for beta in betas:
            t_start = time.time()
            errs = run_one(n, beta, n_polys, seed=seed + n + int(beta))
            stats = {
                "n_polys_finite": len(errs),
                "mean": (sum(errs) / len(errs)) if errs else float("nan"),
                "p50": percentile(errs, 0.5),
                "p90": percentile(errs, 0.9),
                "max": max(errs) if errs else float("nan"),
                "elapsed_s": time.time() - t_start,
            }
            grid[(n, beta)] = stats
            print(
                f"n={n:>4} beta={beta:>5.1f}  "
                f"finite={stats['n_polys_finite']:>3}/{n_polys}  "
                f"mean={stats['mean']:.4f}  "
                f"p50={stats['p50']:.4f}  "
                f"p90={stats['p90']:.4f}  "
                f"max={stats['max']:.4f}  "
                f"({stats['elapsed_s']:.1f}s)"
            )

    # Power-law fit at each beta:  log(err_p50) = alpha * log(n) + c
    # alpha < 0 means err -> 0 as n grows (good); alpha > 0 means err grows.
    # The conjecture predicts alpha = -1 (i.e. err = O(1/n)).
    print("\n=== Power-law fit log(p50_err) = alpha * log(n) + c (per beta) ===")
    fits = {}
    for beta in betas:
        xs = [math.log(n) for n in ns]
        ys = [
            math.log(grid[(n, beta)]["p50"])
            if grid[(n, beta)]["p50"] > 0 else float("nan")
            for n in ns
        ]
        valid = [(x, y) for x, y in zip(xs, ys) if math.isfinite(y)]
        if len(valid) < 2:
            continue
        xs2 = [p[0] for p in valid]
        ys2 = [p[1] for p in valid]
        x_bar = sum(xs2) / len(xs2)
        y_bar = sum(ys2) / len(ys2)
        num = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs2, ys2))
        den = sum((x - x_bar) ** 2 for x in xs2)
        alpha = num / den if den != 0 else float("nan")
        c = y_bar - alpha * x_bar
        fits[beta] = {"alpha": alpha, "c": c, "n_points": len(valid)}
        print(
            f"beta={beta:>5.1f}:  alpha = {alpha:+.4f}  "
            f"(conjecture predicts -1.0)   "
            f"c = {c:+.4f}   n_points = {len(valid)}"
        )

    # Save everything to JSON
    out = {
        "experiment": "maslov_doubling_rate_v1",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "params": {
            "ns": ns,
            "betas": betas,
            "n_polys_per_cell": n_polys,
            "coeff_distribution": "uniform integer in [-10, 10]",
            "seed_base": seed,
        },
        "grid": [
            {"n": n, "beta": beta, **stats}
            for (n, beta), stats in grid.items()
        ],
        "power_law_fits": [
            {"beta": beta, **fit}
            for beta, fit in fits.items()
        ],
        "elapsed_total_s": time.time() - t0,
    }
    Path("/tmp/sperimental_audit/maslov_rate_data.json").write_text(
        json.dumps(out, indent=2)
    )
    print(f"\ntotal elapsed: {time.time() - t0:.1f}s")
    print("saved: /tmp/sperimental_audit/maslov_rate_data.json")


if __name__ == "__main__":
    main()
