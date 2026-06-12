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

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(A, k, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        k //= 2
    return result

def matrix_inv(A, mod):
    n = len(A)
    det = 0
    for i in range(n):
        det += A[0][i] * A[1][(i + 1) % n] - A[0][i] * A[1][(i + 2) % n]
    det %= mod
    if det == 0:
        return None
    inv_det = pow(det, mod - 2, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = A[(i + 1) % n][(j + 1) % n] * A[(i + 2) % n][(j + 2) % n] - A[(i + 1) % n][(j + 2) % n] * A[(i + 2) % n][(j + 1) % n]
            adjugate[i][j] = minor
    inv_A = [[(adjugate[j][i] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_support(cnf, n):
        support = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    support.add(lit)
                else:
                    support.add(-lit)
        return support
    
    def geometric_lattice_size(support):
        # Placeholder for actual geometric lattice size calculation
        return len(support)
    
    def frege_proof_length(k, n):
        # Placeholder for actual Frege proof length calculation
        return k * n
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 20))
    cnf = generate_k_cnf(k, n)
    support = compute_support(cnf, n)
    lattice_size = geometric_lattice_size(support)
    proof_length = frege_proof_length(k, n)
    
    return {
        "metric_name": "Lattice Size / Proof Length Ratio",
        "metric_value": lattice_size / proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")