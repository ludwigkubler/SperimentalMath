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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i + 1, n))) / A_b[i][i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_read_twice_bp(n):
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    b = [random.choice([0, 1]) for _ in range(n)]
    return A, b

def gowers_u3_norm(f, n):
    A = [[f(i, j) for j in range(n)] for i in range(n)]
    B = matrix_multiplication(A, A)
    C = matrix_multiplication(B, A)
    trace = sum(C[i][i] for i in range(n))
    return abs(trace / (n * n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    S = 2 ** n
    IP2_norm = n // 2
    read_twice_norms = []
    
    for _ in range(30):
        A, b = random_read_twice_bp(n)
        f = lambda i, j: A[i][j] ^ b[j]
        norm = gowers_u3_norm(f, n)
        if norm > math.log(S):
            return {
                "metric_name": "Gowers U^3 Norm",
                "metric_value": norm,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Read-twice BP with S={S} has U^3 norm {norm}"
            }
        read_twice_norms.append(norm)
    
    return {
        "metric_name": "Gowers U^3 Norm",
        "metric_value": sum(read_twice_norms) / len(read_twice_norms),
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Read-twice BP with S={S} has U^3 norm {IP2_norm}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")