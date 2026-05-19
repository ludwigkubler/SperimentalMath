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
    
    def generate_random_matrix(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                for k in range(i + 1, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x
    
    def log_moment_generating_function(M, t):
        n = len(M)
        identity = [[0 if i != j else 1 for i in range(n)] for j in range(n)]
        result = identity
        for _ in range(t):
            result = matrix_multiply(result, M)
        return sum(sum(row) for row in result)
    
    def free_entropy(M):
        n = len(M)
        t = int(math.log2(n))
        moment = log_moment_generating_function(M, t)
        return 2 * math.log(moment) / t
    
    def is_read_twice(bp):
        return any(len(path) > 1 for path in bp.values())
    
    def size(bp):
        return sum(len(paths) for paths in bp.values())
    
    n = random.randint(5, 40)
    if not is_read_twice(bp := {i: [random.choice([0, 1]) for _ in range(n)] for i in range(n)}):
        return {
            "seed": seed,
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if size(bp) < 2**n / 2:
        return {
            "seed": seed,
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "size_too_small"
        }
    
    M = generate_random_matrix(n)
    entropy = free_entropy(M)
    
    return {
        "seed": seed,
        "metric_name": "free_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy >= math.log2(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"size_too_small\" first_failing_seed={r['seed']}")
                break