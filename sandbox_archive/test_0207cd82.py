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

# Define A_5 and its standard 4-dim irreducible representation
A5 = [
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0]
]

alpha = A5
beta = [
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1]
]

def commutator(a, b):
    return matrix_multiply(matrix_multiply(a, b), transpose(b)) - matrix_multiply(matrix_multiply(b, a), transpose(a))

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(M):
    n = len(M)
    T = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            T[j][i] = M[i][j]
    return T

def spectral_norm(M):
    eigenvalues = power_iteration(M, 100)
    return max(abs(eigenvalue) for eigenvalue in eigenvalues)

def power_iteration(matrix, iterations=100):
    n = len(matrix)
    v = [random.random() for _ in range(n)]
    v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    
    for _ in range(iterations):
        w = matrix_multiply(matrix, v)
        w_norm = sum(x**2 for x in w)**0.5
        v = [w[i] / w_norm for i in range(n)]
    
    return v

def sign_matrix_to_block_matrix(M_f, rho_alpha, rho_beta):
    n = len(M_f)
    W_f = [[0 for _ in range(4 * n)] for _ in range(4 * n)]
    for i in range(n):
        for j in range(n):
            if M_f[i][j] == 1:
                W_f[4*i:4*(i+1), 4*j:4*(j+1)] = rho_alpha
            elif M_f[i][j] == -1:
                W_f[4*i:4*(i+1), 4*j:4*(j+1)] = rho_beta
    return W_f

def log2(x):
    return math.log2(x)

# Precompute the 4-dim standard irrep of A_5
rho_alpha = alpha[:4]
rho_beta = beta[:4]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for k in [3, 4, 5, 6]:
        instances_tested = 0
        eta_f_count = 0
        eta_disjk = None
        
        for _ in range(30):
            M_f = [[random.choice([-1, 1]) for _ in range(2**k)] for _ in range(2**k)]
            W_f = sign_matrix_to_block_matrix(M_f, rho_alpha, rho_beta)
            sigma_max_Wf = spectral_norm(W_f)
            eta_f = log2(sigma_max_Wf / (2**k))
            eta_0_f = log2(spectral_norm(M_f) / (2**k))
            
            if eta_f >= 0.5 * eta_0_f - 1:
                eta_f_count += 1
            
            instances_tested += 1
        
        results.append({
            "metric_name": "eta",
            "metric_value": eta_f,
            "instances_tested": instances_tested,
            "conjecture_holds": eta_f >= 0.5 * eta_0_f - 1
        })
        
        if k == 3:
            M_disjk = [[int(i < j) for j in range(2**k)] for i in range(2**k)]
            W_disjk = sign_matrix_to_block_matrix(M_disjk, rho_alpha, rho_beta)
            sigma_max_Wdisjk = spectral_norm(W_disjk)
            eta_disjk = log2(sigma_max_Wdisjk / (2**k))
        
        if eta_disjk is not None and eta_disjk < 0.51 * k:
            return {
                "seed": seed,
                "metric_name": "eta",
                "metric_value": eta_disjk,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"DISJ_{k} with eta={eta_disjk}"
            }
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    eta_values = [res["metric_value"] for res in all_results]
    support_fraction = sum(res["conjecture_holds"] for res in all_results) / len(all_results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(eta_values)/len(eta_values):.4f} std={math.sqrt(sum((x - sum(eta_values)/len(eta_values))**2 for x in eta_values) / len(eta_values)):.4f} support_fraction={support_fraction:.4f}"
    elif any(res["conjecture_holds"] is False for res in all_results):
        counterexample = next(res for res in all_results if not res["conjecture_holds"])["counterexample"]
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={next(res for res in all_results if not res['conjecture_holds'])['seed']}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)