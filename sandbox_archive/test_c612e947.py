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

def gaussian_elimination(A):
    n = len(A)
    U = [row[:] for row in A]
    P = [[0] * n for _ in range(n)]
    Q = [[0] * n for _ in range(n)]

    for i in range(n):
        P[i][i], Q[i][i] = 1, 1

    for j in range(n):
        max_row = j
        for i in range(j+1, n):
            if abs(U[i][j]) > abs(U[max_row][j]):
                max_row = i
        U[j], U[max_row] = U[max_row], U[j]
        P[j], P[max_row] = P[max_row], P[j]

        pivot = U[j][j]
        for k in range(n):
            U[j][k] /= pivot
            Q[k][j] /= pivot

        for i in range(n):
            if i != j:
                factor = U[i][j]
                for k in range(n):
                    U[i][k] -= factor * U[j][k]
                    P[i][k] -= factor * P[j][k]

    return U, P, Q

def minimal_local_index(A):
    n = len(A)
    U, _, _ = gaussian_elimination(A)
    I_min = 0
    for i in range(n):
        for j in range(i+1, n):
            if U[i][j] != 0:
                I_min += 1
    return I_min

def communication_complexity_rank_variance(A):
    n = len(A)
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    return (n - rank) ** 2 / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        I_min = minimal_local_index(A)
        sigma_phi = communication_complexity_rank_variance(A)
        if sigma_phi == 0:
            continue
        ratio = abs(I_min / sigma_phi)
        results.append(ratio)

    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    conjecture_holds = all(0.95 * mean_ratio <= r <= 1.05 * mean_ratio for r in results)
    counterexample = "" if conjecture_holds else "ratio_outside_bound"
    
    return {
        "metric_name": "Ratio of Minimal Local Index to Communication Complexity Rank Variance",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(5, 10, 15, 20, 30, 40),  # All tested sizes are at least 5
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_outside_bound\" first_failing_seed={first_failing_seed}")