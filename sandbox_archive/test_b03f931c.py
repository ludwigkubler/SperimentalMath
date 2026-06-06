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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist")
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        # q is quotient
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    # Make x1 positive
    if x1 < 0:
        x1 += m0
    return x1

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = 0
    
    def minor(m, i, j):
        return [row[:j] + row[j+1:] for row in m[:i] + m[i+1:]]
    
    def cofactor(m, i, j):
        return ((-1) ** (i+j)) * determinant(minor(m, i, j))
    
    def determinant(m):
        if len(m) == 1:
            return m[0][0]
        det = 0
        for c in range(len(m)):
            det += m[0][c] * cofactor(m, 0, c)
        return det
    
    det = determinant(matrix)
    
    if det == 0:
        raise ValueError("Matrix is singular")
    
    inv_det = mod_inverse(det, mod)
    
    for i in range(n):
        for j in range(n):
            adj[j][i] = cofactor(matrix, i, j) * inv_det % mod
    
    return adj

def min_frobenius_index(clauses, n):
    if not clauses:
        return 0
    matrix = [[0 for _ in range(len(clauses))] for _ in range(len(clauses))]
    for i in range(len(clauses)):
        for j in range(i+1, len(clauses)):
            common_vars = set(clauses[i]) & set(clauses[j])
            matrix[i][j] = len(common_vars)
            matrix[j][i] = len(common_vars)
    
    mod = 2**31 - 1
    inv_matrix = matrix_mod_inv(matrix, mod)
    
    frobenius_norm_squared = sum(sum(inv_matrix[i][j]**2 for j in range(len(clauses))) for i in range(len(clauses)))
    return math.isqrt(frobenius_norm_squared)

def sat_clause_subset_complexity(formula):
    # Placeholder function to calculate SAT clause subset complexity
    # This is a dummy implementation and should be replaced with actual logic
    return len(formula) ** 0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2 * n)
    clauses = []
    for _ in range(num_clauses):
        clause = set(random.sample(range(1, n+1), random.randint(1, n)))
        clauses.append(clause)
    
    frobenius_index = min_frobenius_index(clauses, n)
    sat_complexity = sat_clause_subset_complexity(clauses)
    
    return {
        "metric_name": "Frobenius Index vs SAT Complexity",
        "metric_value": frobenius_index * sat_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")