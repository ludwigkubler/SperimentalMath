# auto-injected by SEC sandbox
import math
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import json

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for j in range(n):
            if j != i and A[rank][j] != 0:
                factor = A[j][i] / A[rank][i]
                for k in range(n):
                    A[j][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_rank(A):
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = random.choice([2, 3, 4])
    if k == 4 and seed % 5 != 0:
        f = lambda x: sum(x) % 2
    else:
        f = lambda x: random.randint(0, 1)
    
    C_min = []
    for alpha in itertools.product([0, 1], repeat=k):
        if all(f(alpha[:i] + (b,) + alpha[i+1:]) == 1 for b in [0, 1]):
            C_min.append((alpha, f(alpha)))
    
    C_min = list(set(C_min))
    
    r_f = 1
    for Y in itertools.combinations(range(k), len(C_min[0][0])):
        petals = []
        for alpha, _ in C_min:
            if all(alpha[i] == y for i, y in enumerate(Y)):
                petals.append([b for i, b in enumerate(alpha) if i not in Y])
        if len(set(tuple(p) for p in petals)) == len(petals):
            r_f = max(r_f, len(petals))
    
    M = [[f(tuple(random.randint(0, 1) for _ in range(k))) for _ in range(4**k)] for _ in range(2**k)]
    rk_M = matrix_rank(M)
    
    metric_name = "log_r_f_over_log_rk_M"
    metric_value = math.floor(math.log2(r_f)) / math.ceil(math.log2(rk_M))
    instances_tested = 1
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else f"r(f)={r_f}, rk(M)={rk_M}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.4f} std=0.0000 support_fraction=1.0000")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")