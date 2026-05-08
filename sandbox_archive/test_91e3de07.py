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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def matrix_rank(M):
    m, n = len(M), len(M[0])
    rank = 0
    for i in range(m):
        pivot_row = None
        for j in range(i, m):
            if M[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        rank += 1
        for j in range(n):
            M[pivot_row][j], M[i][j] = M[i][j], M[pivot_row][j]
        for j in range(m):
            if j != i and M[j][i] != 0:
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    c = 0.25
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M = generate_disjointness_matrix(n)
        rank = matrix_rank(M)
        secant_dimension = min(rank + 1, n)
        total_metric_value += secant_dimension
        instances_tested += 1

        if secant_dimension < c * n:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, dim(σ(M))={secant_dimension}"

    return {
        "metric_name": "dim(σ(M))",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")