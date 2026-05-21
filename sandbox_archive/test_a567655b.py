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
    m = len(A)
    p = len(B)
    n = len(B[0])
    result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return result

def compute_polymatroid_spectral_gap(n):
    M_r = [n - 1] * n
    M_c = [n - 1] * n
    D_r_inv = [[Fraction(1, d) if d != 0 else Fraction(0, 1) for d in M_r]]
    D_c_inv = [[Fraction(1, d) if d != 0 else Fraction(0, 1) for d in M_c]]
    
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    M_normalized = matrix_multiply(matrix_multiply(D_r_inv, M), D_c_inv)
    
    eigenvalues = compute_spectral_gap(M_normalized)
    return eigenvalues[0] - eigenvalues[1]

def compute_spectral_gap(A):
    m = len(A)
    n = len(A[0])
    
    # Compute the matrix A^T * A
    AT_A = [[sum(A[i][k] * A[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    
    # Compute the eigenvalues of A^T * A using power iteration method
    v = [1.0 / math.sqrt(m) for _ in range(m)]
    for _ in range(100):
        v = matrix_multiply(AT_A, v)
        v_norm = sum(x**2 for x in v)**0.5
        v = [x / v_norm for x in v]
    
    eigenvalues = sorted(v)
    return eigenvalues

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 15, 18, 20, 25, 30, 35, 40]
    mu_clique_values = []
    mu_rand_values = []
    
    for n in n_values:
        if n == 1: continue
        if n > 40: break
        
        # Compute µ_CLIQUE(N)
        mu_clique = compute_polymatroid_spectral_gap(n)
        mu_clique_values.append(mu_clique)
        
        # Compute µ_RAND(N)
        for _ in range(30):
            M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            eigenvalues = compute_spectral_gap(M)
            mu_rand_values.append(eigenvalues[0] - eigenvalues[1])
    
    # Check submodularity
    pairs = [(i, j) for i in range(len(mu_clique_values)) for j in range(i + 1, len(mu_clique_values))]
    submodular_holds = all(mu_clique_values[i] + mu_clique_values[j] >= compute_polymatroid_spectral_gap(n_values[i] + n_values[j]) for i, j in pairs)
    
    # Compute mean and std of µ_CLIQUE
    mu_clique_mean = sum(mu_clique_values) / len(mu_clique_values)
    mu_clique_std = (sum((x - mu_clique_mean)**2 for x in mu_clique_values) / len(mu_clique_values))**0.5
    
    # Check if conjecture holds
    conjecture_holds = submodular_holds and mu_clique_mean >= 0.1 * math.sqrt(n_values[-1]) and max(mu_rand_values) <= 5
    
    return {
        "metric_name": "polymatroid_spectral_gap",
        "metric_value": mu_clique_mean,
        "instances_tested": len(mu_clique_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "submodularity_violation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mu_clique_values = [r["metric_value"] for r in results if "metric_value" in r]
    submodular_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mu_clique_mean = sum(mu_clique_values) / len(mu_clique_values)
    mu_clique_std = (sum((x - mu_clique_mean)**2 for x in mu_clique_values) / len(mu_clique_values))**0.5
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if submodular_holds and mu_clique_mean >= 0.1 * math.sqrt(n_values[-1]) and max(mu_rand_values) <= 5:
        print(f"RESULT: SUPPORTED mean={mu_clique_mean} std={mu_clique_std} support_fraction={support_fraction}")
    elif not submodular_holds:
        print("RESULT: FALSIFIED counterexample=\"submodularity_violation\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=suboptimal_metric")