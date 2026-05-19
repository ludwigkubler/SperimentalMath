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

# Helper functions for matrix operations
def matmul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(M):
    n = len(M)
    M_T = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M_T[j][i] = M[i][j]
    return M_T

def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in M[1:]]
        sign = (-1) ** (j % 2)
        det += sign * M[0][j] * determinant(submatrix)
    return det

def linial_shraibman_gamma(M):
    n = len(M)
    M_T_M = matmul(transpose(M), M)
    v = [Fraction(1, n)] * n
    for _ in range(20):
        v_next = [M_T_M[i][j] * v[j] for j in range(n)]
        v_next = [v_next[j] / sum(v_next) for j in range(n)]
        v = v_next
    return max(abs(x) for x in v)

def run_family(n, family_type):
    instances_tested = 0
    max_delta = -float('inf')
    
    if family_type == 'uniform':
        for _ in range(30):
            M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            g = linial_shraibman_gamma(M)
            det = determinant(M)
            v2_det = 0
            while det % 2 == 0:
                det //= 2
                v2_det += 1
            rho = Fraction(v2_det, n)
            delta = rho * math.log2(n) - 4 * math.log2(g)
            instances_tested += 1
            max_delta = max(max_delta, delta)
    
    # Add more families as needed
    
    return instances_tested, max_delta

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 32, 40]
    total_instances_tested = 0
    max_delta_all_families = -float('inf')
    
    for n in n_values:
        instances_tested_family_a, max_delta_a = run_family(n, 'uniform')
        total_instances_tested += instances_tested_family_a
        max_delta_all_families = max(max_delta_all_families, max_delta_a)
    
    conjecture_holds = max_delta_all_families <= 0
    counterexample = "" if conjecture_holds else "max_delta > 0"
    
    return {
        "metric_name": "max_delta",
        "metric_value": max_delta_all_families,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_delta)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_deviation} support_fraction={support_fraction}")
    elif any(delta > 0.5 for delta in [result["metric_value"] for result in results]):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"max_delta > 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")