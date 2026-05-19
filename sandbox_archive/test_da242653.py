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
    
    def generate_sign_matrix(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def linial_shraibman_gamma(M):
        n = len(M)
        M_T_M = [[sum(M[i][k] * M[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
        v = [1] * n
        for _ in range(20):
            v_next = [M_T_M[i][j] * v[j] for j in range(n)]
            v = [v_next[j] / math.sqrt(sum(v_next[k]**2 for k in range(n))) for j in range(n)]
        return max(abs(v[i]) for i in range(n))
    
    def smith_normal_form(M):
        n = len(M)
        A = M
        U = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        V = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for k in range(n):
            # Find pivot
            max_abs = -1
            pivot_i, pivot_j = -1, -1
            for i in range(k, n):
                for j in range(k, n):
                    if abs(A[i][j]) > max_abs:
                        max_abs = abs(A[i][j])
                        pivot_i, pivot_j = i, j
            # Swap rows and columns to bring the pivot to (k,k)
            A[pivot_i], A[k] = A[k], A[pivot_i]
            U[pivot_i], U[k] = U[k], U[pivot_i]
            A[:, pivot_j], A[:, k] = A[:, k], A[:, pivot_j]
            V[pivot_j], V[k] = V[k], V[pivot_j]
            # Eliminate below and to the right of the pivot
            for i in range(k+1, n):
                factor = A[i][k] / A[k][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                U[i], U[k] = [u - factor * v for u, v in zip(U[i], U[k])]
            for j in range(k+1, n):
                factor = A[k][j] / A[k][k]
                for i in range(k, n):
                    A[i][j] -= factor * A[i][k]
                V[j], V[k] = [v - factor * u for v, u in zip(V[j], V[k])]
        return U, V, A
    
    def two_adic_valuation(x):
        if x == 0:
            return float('inf')
        count = 0
        while x % 2 == 0:
            x //= 2
            count += 1
        return count
    
    n_values = [8, 12, 16, 20, 24, 32, 40]
    instances_tested_family_a = 0
    max_delta_a = float('-inf')
    
    for n in n_values:
        for _ in range(10):  # Sample 10 instances per size
            M = generate_sign_matrix(n)
            g = linial_shraibman_gamma(M)
            U, V, A = smith_normal_form(M)
            det_M = abs(A[0][0] * A[1][1] * A[2][2])
            v_2_det_M = two_adic_valuation(det_M)
            rho_M = v_2_det_M / n
            delta_M = rho_M * math.log2(n) - 4 * math.log2(g)
            instances_tested_family_a += 1
            max_delta_a = max(max_delta_a, delta_M)
    
    conjecture_holds = max_delta_a <= 0
    counterexample = "" if conjecture_holds else f"max_delta={max_delta_a:.5f}"
    
    return {
        "metric_name": "delta_M",
        "metric_value": max_delta_a,
        "instances_tested": instances_tested_family_a,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_delta = math.sqrt(sum((result["metric_value"] - mean_delta) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta:.5f} std={std_delta:.5f} support_fraction={support_fraction:.2f}")
    elif any(result["metric_value"] > 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"max_delta>0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")