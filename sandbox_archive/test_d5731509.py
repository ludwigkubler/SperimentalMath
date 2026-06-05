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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if A[rank][i] == 0:
            for j in range(rank + 1, n):
                if A[j][i] != 0:
                    A[rank], A[j] = A[j], A[rank]
                    break
            else:
                continue
        pivot = Fraction(A[rank][i])
        for j in range(i, n):
            A[rank][j] /= pivot
        for j in range(rank + 1, n):
            factor = -A[j][i]
            for k in range(i, n):
                A[j][k] += factor * A[rank][k]
        rank += 1
    return rank

def lnd(M):
    B = [row[:] for row in M]
    return gaussian_elimination(B)

def generate_kcnf(n, k):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(k):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 2 * n
    instances_tested = 30
    lnd_values = []
    rank_values = []

    for _ in range(instances_tested):
        phi = generate_kcnf(n, k)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in phi:
            for x in clause:
                if x > 0:
                    M[x][x] += 1
                else:
                    M[-x][-x] += 1
        lnd_value = lnd(M)
        rank_value = len(phi)
        lnd_values.append(lnd_value)
        rank_values.append(rank_value)

    mean_lnd = sum(lnd_values) / instances_tested
    std_lnd = math.sqrt(sum((x - mean_lnd) ** 2 for x in lnd_values) / instances_tested)
    ratio_mean = mean_lnd / sum(rank_values) * len(rank_values)
    ratio_std = std_lnd / sum(rank_values) * len(rank_values)

    conjecture_holds = all(abs(ratio_mean - r) <= 0.1 for r in [x / y for x, y in zip(lnd_values, rank_values)])
    counterexample = "" if conjecture_holds else "lnd/rank ratio out of bounds"

    return {
        "metric_name": "lnd/rank_ratio",
        "metric_value": ratio_mean,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lnd/rank ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")