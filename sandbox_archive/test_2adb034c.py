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

def mod_inv(a, m):
    if gcd(a, m) != 1:
        return None
    u, v, s, t = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(m, a)
        m, a = a, r
        u, s = s - q * u, u
        v, t = t - q * v, v
    return s % m

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= mod
    return C

def matrix_pow(A, p, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        p //= 2
    return result

def det(A, mod):
    n = len(A)
    if n == 1:
        return A[0][0]
    det_val = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det_val += (-1) ** j * A[0][j] * det(submatrix, mod)
    return det_val % mod

def matrix_inv(A, mod):
    n = len(A)
    det_A = det(A, mod)
    if det_A == 0:
        return None
    inv_det_A = mod_inv(det_A, mod)
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [[A[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
            minor = det(submatrix, mod)
            adjoint[i][j] = (-1) ** (i + j) * minor
    inv_A = matrix_mul(adjoint, [[inv_det_A]] * n, mod)
    return inv_A

def xor_matrix(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] ^ B[i][j]
    return C

def is_trivial_matrix(M):
    n = len(M)
    for i in range(n):
        for j in range(n):
            if M[i][j]:
                return False
    return True

def clause_entanglement_complexity(F):
    literals = set()
    for clause in F:
        literals.update(clause)
    n = len(literals)
    xor_gates = 0
    while not is_trivial_matrix(F):
        new_clause = []
        for i in range(n):
            if any(F[j][i] for j in range(len(F))):
                new_clause.append(i)
                break
        if not new_clause:
            return float('inf')
        xor_gates += 1
        F = xor_matrix(F, [[0 if i != j else 1 for j in range(n)] for i in new_clause])
    return xor_gates

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        F = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        dual_code = xor_matrix(F, [[0 if i != j else 1 for j in range(n)] for i in range(n)])
        
        UEA_rank = det(dual_code, 2)
        entanglement_complexity = clause_entanglement_complexity(dual_code)
        
        results.append({
            "n": n,
            "UEA_rank": UEA_rank,
            "entanglement_complexity": entanglement_complexity
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    UEA_ranks = [r["UEA_rank"] for r in results]
    entanglement_complexities = [r["entanglement_complexity"] for r in results]
    
    mean_rank = sum(UEA_ranks) / len(UEA_ranks)
    mean_complexity = sum(entanglement_complexities) / len(entanglement_complexities)
    
    if any(c > math.log2(n) + 3 for n, c in zip(n_values, entanglement_complexities)):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"complexity_exceeds_log2_n_plus_3"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "correlation",
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='complexity_exceeds_log2_n_plus_3' first_failing_seed={first_failing_seed}")