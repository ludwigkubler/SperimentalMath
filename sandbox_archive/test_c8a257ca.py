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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def schatten_p_norm(M, p):
    n = len(M)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    M_p_inv = [row[:] for row in M]
    for _ in range(100):  # Simple power iteration to approximate the inverse
        M_p_inv = matrix_multiplication(M_p_inv, M)
    return (trace(matrix_multiplication(M_p_inv, M)) ** (1 / p))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    p_values = [1.5, 1.75, 1.9]
    C_estimates = []
    
    for _ in range(30):  # Sample 30 instances per seed
        M = generate_disjointness_matrix(n)
        norms = [schatten_p_norm(M, p) for p in p_values]
        C_estimates.extend(norms)
    
    if not C_estimates:
        return {
            "metric_name": "Schatten p-norm",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_C = sum(C_estimates) / len(C_estimates)
    std_C = math.sqrt(sum((x - mean_C) ** 2 for x in C_estimates) / len(C_estimates))
    
    conjecture_holds = all(0.8 * mean_C <= norm <= 1.2 * mean_C for norm in C_estimates)
    counterexample = "" if conjecture_holds else "norms outside expected range"
    
    return {
        "metric_name": "Schatten p-norm",
        "metric_value": mean_C,
        "instances_tested": len(C_estimates),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all("counterexample" not in r or r["counterexample"] == "" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norms outside expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")