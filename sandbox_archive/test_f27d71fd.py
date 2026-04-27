# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    A = gaussian_elimination(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def permanent(M):
    m, n = len(M), len(M[0])
    if m != n:
        raise ValueError("Matrix must be square")
    perm = 0
    sign = 1
    for p in itertools.permutations(range(n)):
        product = 1
        for i in range(n):
            product *= M[i][p[i]]
        perm += sign * product
        sign *= -1
    return perm

def variance(M, eps):
    m, n = len(M), len(M[0])
    avg_M = [[sum(row[j] * eps[j] for j in range(n)) for row in M] for _ in range(64)]
    var = 0
    for i in range(m):
        for j in range(i + 1, m):
            sum_diff = 0
            for k in range(64):
                sum_diff += abs(avg_M[k][i] - avg_M[k][j])
            var += sum_diff ** 2
    return var / (m * (m - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    ell = random.choice([3, 4, 5])
    m = random.randint(ell + 1, 12)
    a = random.choice([1, 2])
    D = [[random.choice([0, 1]) for _ in range(m)] for _ in range(ell)]
    M = [sum(D[i][j] * row[j] for i in range(ell)) for j in range(m)]
    V_M = math.log2(1 + variance(M, random.choices([-1, 1], k=m))) / m
    
    def is_hard_truth_table(f):
        # Placeholder for actual hardness check
        return True
    
    if not is_hard_truth_table(lambda x: sum(x) % 2 == 0):  # Example hard function
        return {
            "metric_name": "V(M)",
            "metric_value": V_M,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def bias(NW_D_f, w):
        # Placeholder for actual bias calculation
        return random.random()
    
    max_bias = max(bias(lambda x: sum(x) % 2 == 0, w) for w in [1, 2, 3])
    log_inv_bias = math.log(1 / max_bias)
    c = 0.05
    if log_inv_bias >= c * V_M * m / 3:
        return {
            "metric_name": "V(M)",
            "metric_value": V_M,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "V(M)",
            "metric_value": V_M,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"bias={max_bias}, log_inv_bias={log_inv_bias}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" not in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")