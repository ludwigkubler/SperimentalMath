# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    n = seed % 10 + 10  # Ensure n is in [10, 22]
    if n not in {10, 14, 18, 22}:
        return {
            "metric_name": "rho_over_kappa",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }

    random.seed((n, seed))
    V = list(range(n))
    E = []
    degree_count = [0] * n

    while len(E) < (n - 1):
        u = random.choice(V)
        v = random.choice([v for v in V if v != u and degree_count[v] < 3])
        if (u, v) not in E and (v, u) not in E:
            E.append((u, v))
            degree_count[u] += 1
            degree_count[v] += 1

    L = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in E:
        L[u][v] = -1 / 3
        L[v][u] = -1 / 3
        L[u][u] += 1 / 3
        L[v][v] += 1 / 3

    def eigh(A):
        n = len(A)
        for _ in range(100):  # Simple power iteration to find the largest eigenvalue and eigenvector
            x = [random.gauss(0, 1) for _ in range(n)]
            x /= math.sqrt(sum(x[i] ** 2 for i in range(n)))
            Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            lambda_max = max(abs(Ax[i]) / abs(x[i]) for i in range(n))
            x = [Ax[i] / lambda_max for i in range(n)]
        return lambda_max, x

    lambda_max, phi = eigh(L)
    phi = [abs(phi[i]) for i in range(n)]

    kappa_G = 2 * (1 - sum(phi) / math.sqrt(n))
    if kappa_G <= 0.01:
        return {
            "metric_name": "rho_over_kappa",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    def max_cut(G):
        n = len(G)
        best_cut = -1
        for mask in range(1, 2 ** n):
            cut_value = sum(G[i][j] if (mask >> i) & 1 and not ((mask >> j) & 1) else 0 for i in range(n) for j in range(i + 1, n))
            best_cut = max(best_cut, cut_value)
        return best_cut

    MC_G = max_cut(E)

    rho_G = (n * lambda_max / 4) / MC_G - 1
    if rho_G > 16 * kappa_G:
        return {
            "metric_name": "rho_over_kappa",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, rho_G={rho_G}, kappa_G={kappa_G}"
        }

    return {
        "metric_name": "rho_over_kappa",
        "metric_value": rho_G / kappa_G,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rho_over_kappa = sum(r["metric_value"] for r in results) / len(results)
        std_rho_over_kappa = math.sqrt(sum((r["metric_value"] - mean_rho_over_kappa) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        max_violation_gap = max(r["counterexample"].split(",")[1] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        support_fraction = sum("conjecture_holds" in r and r["conjecture_holds"] for r in results) / len(results)
        mean_rho_over_kappa = None
        std_rho_over_kappa = None

    print(f"RESULT: {'SUPPORTED' if all('conjecture_holds' in r and r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_rho_over_kappa} std={std_rho_over_kappa} support_fraction={support_fraction}")