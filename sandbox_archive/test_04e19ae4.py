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

def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

def frobenius_norm_squared(A):
    return trace(matrix_multiply(A, A))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bp(w, n):
        M = [random.choice([[0]*w for _ in range(w)]) for _ in range(2*n)]
        N = [matrix_subtract(M[j], M[j-1]) for j in range(1, 2*n)]
        return N
    
    def compute_P_v(N, a, b):
        return matrix_multiply(matrix_multiply(N[a], N[b]), N[b])
    
    def compute_rho(P, w):
        max_inner_product = -math.inf
        for u in range(len(P)):
            for v in range(u+1, len(P)):
                inner_product = frobenius_norm_squared(matrix_multiply(P[u], P[v]))
                if inner_product > max_inner_product:
                    max_inner_product = inner_product
        return math.log2(max_inner_product) / (w**2)
    
    n_values = [6, 10, 16, 24, 32, 40]
    w_values = [2, 4, 8]
    results = []
    instances_tested = 0
    
    for n in n_values:
        for w in w_values:
            for _ in range(30):
                N = generate_bp(w, n)
                P_v = [compute_P_v(N, a, b) for a in range(n) for b in range(n)]
                rho = compute_rho(P_v, w)
                instances_tested += 1
                results.append((n, w, rho))
    
    support_fraction = sum(1 for _, _, rho in results if rho <= 2 * math.log2(w) + 2) / len(results)
    lower_bound_met = all(rho >= n / 16 - 4 * math.log2(n) for n, _, rho in results if n in [4, 6, 8, 10])
    
    return {
        "metric_name": "rho(P)",
        "metric_value": sum(rho for _, _, rho in results) / len(results),
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction == 1 and lower_bound_met,
        "counterexample": "" if support_fraction == 1 and lower_bound_met else str(max((n, w, rho) for n, w, rho in results if rho > 2 * math.log2(w) + 2 or (n in [4, 6, 8, 10] and rho < n / 16 - 4 * math.log2(n))))
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")