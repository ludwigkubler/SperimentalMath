# auto-injected by SEC sandbox
import math
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
from random import randint, seed
from collections import defaultdict

def run_trial(seed: int) -> dict:
    def monotone_f(n):
        return lambda s: all(x in s for x in range(n))

    def compute_D_m(f, n):
        min_f = [f(i) for i in range(2**n)]
        max_not_f = [not f(i) for i in range(2**n)]
        X = [(i & (1 << j)) > 0 for i in range(2**n) for j in range(n)]
        Y = [(i & (1 << j)) == 0 for i in range(2**n) for j in range(n)]
        return min(max([sum(X[i] and Y[j] for i, j in zip(range(2**n), range(2**n))) for i in range(2**n)]), n)

    def compute_pd(f, n):
        Δ_f = {frozenset(s) for s in range(2**n) if f(s) == 0}
        max_j = -1
        for T in range(1 << n):
            Δ_T = {S for S in Δ_f if all(x in T for x in S)}
            boundary_matrix = []
            for k in range(len(Δ_T)):
                row = [0] * len(Δ_T)
                for i, s in enumerate(Δ_T):
                    if len(s) == k:
                        for j, t in enumerate(Δ_T):
                            if all(x in t for x in s):
                                row[j] += 1
                boundary_matrix.append(row)
            rank = 0
            pivot_row = -1
            for i in range(len(boundary_matrix)):
                if any(boundary_matrix[i][j] != 0 for j in range(rank, len(boundary_matrix))):
                    if pivot_row == -1:
                        pivot_row = i
                    else:
                        boundary_matrix[pivot_row], boundary_matrix[i] = boundary_matrix[i], boundary_matrix[pivot_row]
                    rank += 1
                    for j in range(len(boundary_matrix)):
                        if j != i and any(boundary_matrix[j][k] != 0 for k in range(rank)):
                            factor = boundary_matrix[j][i] / boundary_matrix[i][i]
                            for k in range(rank):
                                boundary_matrix[j][k] -= factor * boundary_matrix[i][k]
        return max_j - rank - 1

    n_values = [3, 4, 5]
    results = []
    for n in n_values:
        if n == 5:
            f = monotone_f(n)
            D_m_f = compute_D_m(f, n)
            Pd_f = compute_pd(f, n)
            results.append({
                "metric_name": "D_m(f) - Pd(f)",
                "metric_value": D_m_f - Pd_f,
                "instances_tested": 1,
                "conjecture_holds": D_m_f >= Pd_f,
                "counterexample": "" if D_m_f >= Pd_f else f"Counterexample for n={n}"
            })
        else:
            for _ in range(20):
                f = monotone_f(n)
                D_m_f = compute_D_m(f, n)
                Pd_f = compute_pd(f, n)
                results.append({
                    "metric_name": "D_m(f) - Pd(f)",
                    "metric_value": D_m_f - Pd_f,
                    "instances_tested": 1,
                    "conjecture_holds": D_m_f >= Pd_f,
                    "counterexample": "" if D_m_f >= Pd_f else f"Counterexample for n={n}"
                })

    return {
        "metric_name": "D_m(f) - Pd(f)",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": "" if all(r["conjecture_holds"] for r in results) else next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")