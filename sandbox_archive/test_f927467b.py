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
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def random_cnf(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def cell_complex_rank(phi):
    n = len(phi)
    A = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(n):
        for j in range(i+1, n):
            if any(var in phi[i] and var in phi[j] for var in variables):
                A[i][j] = 1
                A[j][i] = 1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    rank_sum = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        m = random.randint(n, 2*n)
        phi = random_cnf(n, m)
        rank = cell_complex_rank(phi)
        rank_sum += rank
        instances_tested += 1

    mean_rank = rank_sum / instances_tested
    if abs(mean_rank - n) > 3:
        conjecture_holds = False
        counterexample = f"Mean rank {mean_rank} is too far from expected {n}"

    return {
        "metric_name": "Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")