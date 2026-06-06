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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * (matrix[1][2] - matrix[2][1])
    inv_det = mod_inverse(det, mod)
    adjugate = [[(matrix[(i+1) % n][(j+1) % n] - matrix[(i+1) % n][(j+2) % n]) * (matrix[(i+2) % n][(j+1) % n] - matrix[(i+2) % n][(j+2) % n]) for j in range(n)] for i in range(n)]
    return [[(inv_det * adjugate[i][j]) % mod for j in range(n)] for i in range(n)]

def matmul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def min_frobenius_index(clauses, n):
    mod = 10**9 + 7
    vector_space = [tuple(sorted(c)) for c in clauses]
    vectors = list(set(vector_space))
    matrix = [[0] * len(vectors) for _ in range(len(vectors))]
    for i in range(len(vectors)):
        for j in range(i, len(vectors)):
            if set(vectors[i]) <= set(vectors[j]):
                matrix[i][j] = 1
                matrix[j][i] = 1
    inv_matrix = matrix_mod_inv(matrix, mod)
    rank = sum(1 for row in inv_matrix if any(row))
    return rank

def sat_clause_subset_complexity(clauses):
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        clauses = [[random.randint(1, n) for _ in range(random.randint(2, 4))] for _ in range(n)]
        frobenius_index = min_frobenius_index(clauses, n)
        sat_complexity = sat_clause_subset_complexity(clauses)
        results.append((frobenius_index, sat_complexity))
    if len(results) < 30:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    frobenius_indices = [r[0] for r in results]
    sat_complexities = [r[1] for r in results]
    n = len(frobenius_indices)
    rank_frobenius = sorted(range(n), key=lambda i: frobenius_indices[i])
    rank_sat = sorted(range(n), key=lambda i: sat_complexities[i])
    rho_numerator = sum((rank_frobenius[i] - (n + 1) / 2) * (rank_sat[i] - (n + 1) / 2) for i in range(n))
    rho_denominator = math.sqrt(sum((rank_frobenius[i] - (n + 1) / 2)**2 for i in range(n))) * math.sqrt(sum((rank_sat[i] - (n + 1) / 2)**2 for i in range(n)))
    if rho_denominator == 0:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    rho = rho_numerator / rho_denominator
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": -0.5 <= rho <= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")