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
    
    def generate_function(n):
        return lambda x: sum(x[i] * (i + 1) for i in range(n)) % 2
    
    def matrix_multiplication(A, B):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            for j in range(i+1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = M[i][n] / M[i][i]
            for j in range(i-1, -1, -1):
                M[j][n] -= M[j][i] * x[i]
        return x
    
    def power_iteration(A, max_iter=1000):
        n = len(A)
        v = [random.random() for _ in range(n)]
        v = [x / sum(v) for x in v]
        for _ in range(max_iter):
            v_next = matrix_multiplication(A, v)
            v_next = [x / sum(v_next) for x in v_next]
            if abs(sum(v[i] * v_next[i] for i in range(n))) > 0.95:
                return max(abs(x) for x in v_next)
        return None
    
    def sos_moment_matrix(f, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for x in itertools.product([0, 1], repeat=n):
            y = f(x)
            for i in range(n + 1):
                for j in range(n + 1):
                    A[i][j] += x[i] * x[j]
            A[n][n] += y
        return A
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    A = sos_moment_matrix(f, n)
    lambda_min = power_iteration(A)
    
    if lambda_min is None:
        return {
            "metric_name": "lambda_min",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "power_iteration_failed"
        }
    
    C = 1
    conjecture_holds = lambda_min >= C / math.sqrt(n)
    counterexample = "" if conjecture_holds else f"lambda_min={lambda_min}, n={n}"
    
    return {
        "metric_name": "lambda_min",
        "metric_value": lambda_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(not r["conjecture_holds"] for r in results) / len(results) >= 0.2:
        print("RESULT: INCONCLUSIVE less_than_80_percent_support")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")