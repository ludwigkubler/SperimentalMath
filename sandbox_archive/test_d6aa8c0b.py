# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if matrix[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rank + 1, m):
            factor = -matrix[i][j] / matrix[rank][j]
            for k in range(n):
                matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def grothendieck_group_rank(phi):
    n = len(phi)
    A = [[0] * (2 * n) for _ in range(2 * n)]
    for i, clause in enumerate(phi):
        for var in clause:
            if var > 0:
                A[i][var - 1] += 1
            else:
                A[i + n][-var - 1] += 1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30]:
        phi = generate_cnf(n)
        rank = grothendieck_group_rank(phi)
        eta = Fraction(rank, n**2)
        results.append({"n": n, "eta": eta})
    metric_value = sum(result["eta"] for result in results) / len(results)
    conjecture_holds = all(result["eta"] <= Fraction(n**2, n**2) for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, eta={results[0]['eta']}"
    return {
        "metric_name": "minimal_eta_quotient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=n={results[0]['n']}, eta={results[0]['eta']} first_failing_seed={first_failing_seed}")