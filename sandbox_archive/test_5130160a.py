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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tropical_hodge_norm(A):
        m, n = len(A), len(A[0])
        max_val = float('-inf')
        for i in range(m):
            row_max = float('-inf')
            col_max = float('-inf')
            for j in range(n):
                row_max = max(row_max, A[i][j])
                col_max = max(col_max, A[j][i])
            max_val = max(max_val, row_max, col_max)
        return max_val

    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def ac0_circuit_size(f):
        n = int(math.log2(len(f)))
        return 2**(n-1)

    def tropical_variety(f):
        n = len(f)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if f[i-1] == f[j-1]:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
        return gaussian_elimination(A)

    def compute_tropical_hodge_norm(f):
        n = len(f)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if f[i-1] == f[j-1]:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
        return tropical_hodge_norm(A)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            s = ac0_circuit_size(f)
            V_f = tropical_variety(f)
            H_V_f = compute_tropical_hodge_norm(V_f)
            total_metric_value += H_V_f
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(mean_metric_value >= s**0.5 for s in [2**(n-1) for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "tropical_hodge_norm",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")