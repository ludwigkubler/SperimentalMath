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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_spectral_gap(A):
    m, n = len(A), len(A[0])
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(m)]
    
    # Compute A^T * A
    AT_A = [[sum(A[i][k] * A[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    
    # Compute eigenvalues of A^T * A using QR algorithm
    max_iter = 1000
    tol = 1e-6
    Q, R = A, I
    for _ in range(max_iter):
        Q, R = matrix_multiply(Q, R), gaussian_elimination(R)
        A = matrix_multiply(R, Q)
        if all(abs(A[i][j]) < tol for i in range(m) for j in range(i + 1, m)):
            break
    
    # Extract eigenvalues from diagonal of R
    eigenvalues = [R[i][i] for i in range(min(m, n))]
    return sorted(eigenvalues, reverse=True)

def compute_polymatroid_spectral_gap(n):
    # Construct the canonical CLIQUE_3 DNF
    M = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
    edge_index = 0
    for i in range(n):
        for j in range(i + 1, n):
            M[edge_index][i * (n - 1) // 2 + j - i - 1] = 1
            edge_index += 1
    
    # Compute the normalized bipartite incidence matrix G_D
    D_r = [sum(row[i] for row in M) for i in range(n * (n - 1) // 2)]
    D_c = [sum(M[i][j] for i in range(n * (n - 1) // 2)) for j in range(n)]
    D_r_inv = [Fraction(1, d) if d != 0 else 0 for d in D_r]
    D_c_inv = [Fraction(1, d) if d != 0 else 0 for d in D_c]
    
    M_normalized = [[M[i][j] * math.sqrt(D_r_inv[i]) * math.sqrt(D_c_inv[j]) for j in range(n)] for i in range(n * (n - 1) // 2)]
    
    # Compute the spectral gap
    eigenvalues = compute_spectral_gap(M_normalized)
    return eigenvalues[0] - eigenvalues[1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 15, 18, 20, 25, 30, 35, 40]
    mu_clique_values = []
    mu_rand_values = []
    
    for n in n_values:
        # Compute µ_CLIQUE(N)
        mu_clique = compute_polymatroid_spectral_gap(n)
        mu_clique_values.append(mu_clique)
        
        # Compute µ_RAND(N)
        M_rand = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        eigenvalues = compute_spectral_gap(M_rand)
        mu_rand = eigenvalues[0] - eigenvalues[1]
        mu_rand_values.append(mu_rand)
    
    # Check submodularity
    submodular = True
    pairs = [(random.choice(n_values), random.choice(n_values)) for _ in range(30)]
    for n1, n2 in pairs:
        M1 = [[random.randint(0, 1) for _ in range(n1)] for _ in range(n1)]
        M2 = [[random.randint(0, 1) for _ in range(n2)] for _ in range(n2)]
        mu_D1 = compute_spectral_gap(M1)
        mu_D2 = compute_spectral_gap(M2)
        mu_D_and_D2 = compute_spectral_gap(matrix_multiply(M1, M2))
        if mu_D_and_D2 > mu_D1 + mu_D2:
            submodular = False
            break
    
    # Check mean and standard deviation of µ_CLIQUE(N) vs √N
    mu_clique_mean = sum(mu_clique_values) / len(mu_clique_values)
    mu_clique_std = math.sqrt(sum((x - mu_clique_mean) ** 2 for x in mu_clique_values) / len(mu_clique_values))
    
    # Check max of µ_RAND/log N
    mu_rand_max = max(mu_rand_values)
    
    return {
        "metric_name": "polymatroid_spectral_gap",
        "metric_value": mu_clique_mean,
        "instances_tested": len(n_values),
        "conjecture_holds": mu_clique_mean >= 0.1 * math.sqrt(15) and mu_rand_max <= 5 and submodular,
        "counterexample": "" if mu_clique_mean >= 0.1 * math.sqrt(15) and mu_rand_max <= 5 and submodular else "submodularity_violation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mu_clique_mean = sum(r["metric_value"] for r in results) / len(results)
    mu_clique_std = math.sqrt(sum((r["metric_value"] - mu_clique_mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mu_clique_mean} std={mu_clique_std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"submodularity_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")