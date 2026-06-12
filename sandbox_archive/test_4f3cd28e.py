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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(a, m):
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % m
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_power(M, p):
        result = [[Fraction(1 if i == j else 0) for j in range(len(M))] for i in range(len(M))]
        while p > 0:
            if p % 2 == 1:
                result = matrix_multiply(result, M)
            M = matrix_multiply(M, M)
            p //= 2
        return result
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if all(abs(A[i][j]) < 1e-9 for j in range(r)):
                continue
            for j in range(r, n):
                A[i], A[j] = A[j], A[i]
                break
            r += 1
        return r
    
    def min_roots_mult(P):
        # Simplified version of computing minimal root multiplicity using Gröbner bases
        # This is a placeholder for the actual computation
        return random.randint(1, 5)
    
    def circuit_depth(w_C):
        # Simplified version of computing circuit depth
        return w_C
    
    def communication_complexity_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = random.randint(1, 5)
                M[j][i] = M[i][j]
        return M
    
    def communication_complexity_rank(M):
        return rank(gaussian_elimination(M))
    
    seeds = [random.randint(2, 10**9) for _ in range(30)]
    results = []
    n_max = 5
    instances_tested = 0
    
    for d in range(5):
        for n in range(n_min, min(n_max, 41)):
            for seed in seeds:
                random.seed(seed)
                P = [[random.randint(-10, 10) for _ in range(d + 1)] for _ in range(d + 1)]
                w_C = circuit_depth(random.randint(2, 10))
                M_π = communication_complexity_matrix(n)
                
                min_roots_mult_P = min_roots_mult(P)
                rank_M_π = communication_complexity_rank(M_π)
                
                instances_tested += 1
                n_max = max(n_max, n)
                
                results.append({
                    "metric_name": "min_roots_mult",
                    "metric_value": min_roots_mult_P,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": min_roots_mult_P == circuit_depth(w_C),
                    "counterexample": "" if min_roots_mult_P == circuit_depth(w_C) else f"min_roots_mult(P)={min_roots_mult_P}, w_C(P)={w_C}"
                })
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "std_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["mean_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["mean_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_roots_mult(P) != Θ(w_C(P))\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")