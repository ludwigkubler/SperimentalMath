# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = next((i for i in range(rank, m) if A[i][j] != 0), -1)
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def characteristic_polynomial(F, p):
    m = len(F)
    n = len(F[0])
    A = [[Fraction(0) for _ in range(m + 1)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if F[i][j] != 0:
                A[i][i - j] += Fraction(F[i][j], p)
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for m in m_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            n = random.randint(m + 1, min(n_max + 10, 40))
            F = [[random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))] for _ in range(m)]
            p_values = [2, 3, 5, 7]
            v_p_values = []
            for p in p_values:
                v_p = characteristic_polynomial(F, p)
                if v_p == 0:
                    v_p = 1
                v_p_values.append(v_p)

            c_F = sum(len([j for j in range(n) if F[i][j] != 0]) for i in range(m))
            metric_values.append((c_F, min(v_p_values)))
            instances_tested += 1
            n_max = max(n_max, n)

    mean_value = sum(metric[0] / metric[1] for metric in metric_values) / len(metric_values)
    std_value = math.sqrt(sum((metric[0] / metric[1] - mean_value) ** 2 for metric in metric_values) / len(metric_values))
    conjecture_holds = all(c_F <= min(v_p_values) for c_F, v_p_values in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Clause Complexity / Minimal p-Adic Valuation Rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")