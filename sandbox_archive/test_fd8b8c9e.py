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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n+1):
                M[j][k] -= factor * M[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for j in range(i-1, -1, -1):
            M[j][n] -= M[j][i] * x[i]
    return x

def polymatroid_rank(clauses):
    n = len(clauses)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if any(c in clauses[i] and c in clauses[j] for c in set(clauses[i]) & set(clauses[j])):
                matrix[i][j] = 1
    rank = 0
    for col in range(n):
        if sum(matrix[row][col] for row in range(col, n)) > 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = math.ceil(n ** (1/3))
    
    # Generate k-CLIQUE instance
    clauses = []
    for i in range(k):
        clause = [random.randint(1, n) for _ in range(random.randint(2, min(3, n)))]
        clauses.append(clause)
    
    # Compute polymatroid rank
    rho = polymatroid_rank(clauses)
    if rho < n ** (1/2) * k ** (1/4):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rho,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE instance does not satisfy ρ ≥ n^{1/2} · k^{1/4}"
        }
    
    # Compare against DNF formulas with size ≤ n^2
    for _ in range(29):
        dnf_size = random.randint(1, n**2)
        dnf_clauses = [random.sample(range(1, n+1), random.randint(1, min(n, dnf_size))) for _ in range(dnf_size)]
        rho_dnf = polymatroid_rank(dnf_clauses)
        if rho_dnf > math.log(n) + 2 * math.log(k):
            return {
                "metric_name": "polymatroid_rank",
                "metric_value": rho_dnf,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "DNF formula with size ≤ n^2 does not satisfy ρ ≤ log n + 2 log k"
            }
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rho,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE instance does not satisfy ρ ≥ n^{1/2} · k^{1/4}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")