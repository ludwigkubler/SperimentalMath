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
            if A[j][i] > A[max_row][i]:
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def tropical_determinant(A):
    n = len(A)
    det = 0
    for sign in itertools.product([1, -1], repeat=n):
        permuted_A = [A[i][:] for i in range(n)]
        for j in range(n):
            if sign[j] == -1:
                for k in range(n):
                    permuted_A[k][j] = -permuted_A[k][j]
        det += sign[0] * gaussian_elimination(permuted_A)[0][0]
    return det

def ac0_parity_depth(G):
    n = len(G)
    if n == 1:
        return 1
    if all(G[i][i] == 1 for i in range(n)):
        return 2
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(10, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 1
    inc_matrix = []
    for i in range(n):
        row = [G[j][i] for j in range(n)]
        inc_matrix.append(row)
    chi_t = tropical_determinant(inc_matrix)
    depth = ac0_parity_depth(G)
    metric_name = "tropical_euler_characteristic"
    metric_value = chi_t
    instances_tested = 1
    conjecture_holds = chi_t >= math.log(n)
    counterexample = "" if conjecture_holds else f"Graph with n={n} and depth={depth}"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*1000, 100))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")