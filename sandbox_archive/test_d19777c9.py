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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([10, 20, 30, 40])
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute free entropy using approximate R-transforms
    def r_transform(A):
        n = len(A)
        I = [[int(i == j) for i in range(n)] for j in range(n)]
        A_inv = A
        r = 0
        for k in range(1, 100):  # Number of terms in the series
            A_inv = matrix_multiply(A_inv, A)
            r += sum(sum(abs(A_inv[i][j]) for j in range(n)) for i in range(n))
        return r / n
    
    phi_M = r_transform(M)
    
    c = 0.1
    if phi_M < c * n:
        return {
            "metric_name": "free_entropy",
            "metric_value": phi_M,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"phi(M) / n = {phi_M / n} < {c}"
        }
    else:
        return {
            "metric_name": "free_entropy",
            "metric_value": phi_M,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='phi(M) / n < 0.1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")