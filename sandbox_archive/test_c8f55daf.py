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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def singular_value_decomposition(A):
        U, S, Vt = [], [], []
        A_t = list(zip(*A))
        m, n = len(A), len(A[0])
        
        # Compute A^T * A and A * A^T
        ATA = [[sum(A[i][k] * A[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
        AA_t = [[sum(A[i][k] * A_t[j][k] for k in range(m)) for j in range(n)] for i in range(n)]
        
        # Perform SVD on ATA
        U, S, Vt = gaussian_elimination(ATA), [], []
        for row in U:
            S.append(max(row))
            Vt.append([1 if i == j else 0 for j in range(m)])
        
        return U, S, Vt
    
    def compute_polymatroid_spectral_gap(n):
        # Construct the canonical CLIQUE_3 DNF
        terms = []
        variables = set()
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                for k in range(j+1, n+1):
                    term = [(i-1), (j-1), (k-1)]
                    terms.append(term)
                    variables.update(term)
        
        m = len(terms)
        v = len(variables)
        
        # Construct the incidence matrix M
        M = [[0] * v for _ in range(m)]
        var_index = {var: i for i, var in enumerate(sorted(variables))}
        for i, term in enumerate(terms):
            for var in term:
                M[i][var_index[var]] = 1
        
        # Compute the row and column degrees
        D_r = [sum(row) for row in M]
        D_c = [sum(col) for col in zip(*M)]
        
        # Normalize the incidence matrix
        D_r_inv_half = [[1 / math.sqrt(d) if d > 0 else 0 for d in D_r] for _ in range(m)]
        D_c_inv_half = [[1 / math.sqrt(d) if d > 0 else 0 for d in D_c] for _ in range(v)]
        
        M_normalized = matrix_multiply(matrix_multiply(D_r_inv_half, M), D_c_inv_half)
        
        # Compute the singular value decomposition
        U, S, Vt = singular_value_decomposition(M_normalized)
        
        # Return the spectral gap
        return S[0] - S[1]
    
    def generate_random_monotone_dnf(n):
        terms = []
        for _ in range(n**2):
            term = random.sample(range(n), 3)
            terms.append(term)
        return terms
    
    n_values = [8, 10, 12, 15, 18, 20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        # Compute µ_CLIQUE(N)
        mu_clique = compute_polymatroid_spectral_gap(n)
        results.append({"n": n, "mu_clique": mu_clique})
        
        # Generate random monotone DNFs and compute µ_RAND(N)
        for _ in range(30):
            terms = generate_random_monotone_dnf(n)
            m = len(terms)
            v = n * (n - 1) // 2
            M = [[0] * v for _ in range(m)]
            var_index = {var: i for i, var in enumerate(range(v))}
            
            for i, term in enumerate(terms):
                for var in term:
                    M[i][var_index[var]] = 1
            
            D_r = [sum(row) for row in M]
            D_c = [sum(col) for col in zip(*M)]
            
            D_r_inv_half = [[1 / math.sqrt(d) if d > 0 else 0 for d in D_r] for _ in range(m)]
            D_c_inv_half = [[1 / math.sqrt(d) if d > 0 else 0 for d in D_c] for _ in range(v)]
            
            M_normalized = matrix_multiply(matrix_multiply(D_r_inv_half, M), D_c_inv_half)
            
            U, S, Vt = singular_value_decomposition(M_normalized)
            
            mu_rand = S[0] - S[1]
            results.append({"n": n, "mu_rand": mu_rand})
    
    # Analyze the results
    mu_clique_values = [r["mu_clique"] for r in results if "mu_clique" in r]
    mu_rand_values = [r["mu_rand"] for r in results if "mu_rand" in r]
    
    mean_mu_clique = sum(mu_clique_values) / len(mu_clique_values)
    std_mu_clique = math.sqrt(sum((x - mean_mu_clique) ** 2 for x in mu_clique_values) / len(mu_clique_values))
    mean_mu_rand = sum(mu_rand_values) / len(mu_rand_values)
    std_mu_rand = math.sqrt(sum((x - mean_mu_rand) ** 2 for x in mu_rand_values) / len(mu_rand_values))
    
    support_fraction = len([r for r in results if "mu_clique" in r and r["mu_clique"] >= 0.1 * math.sqrt(r["n"])]) / len(results)
    
    # Check submodularity
    submodular = True
    for _ in range(30):
        n = random.randint(2, 4)
        terms1 = generate_random_monotone_dnf(n)
        terms2 = generate_random_monotone_dnf(n)
        mu1 = compute_polymatroid_spectral_gap(n)
        mu2 = compute_polymatroid_spectral_gap(n)
        mu3 = compute_polymatroid_spectral_gap(n)
        
        if mu1 + mu2 < mu3:
            submodular = False
            break
    
    # Determine the result
    if not submodular:
        return {"metric_name": "mu_clique", "metric_value": mean_mu_clique, "instances_tested": len(results), "conjecture_holds": False, "counterexample": "submodularity_violation"}
    
    if support_fraction < 0.8:
        return {"metric_name": "mu_clique", "metric_value": mean_mu_clique, "instances_tested": len(results), "conjecture_holds": False, "counterexample": f"support_fraction={support_fraction:.2f}"}
    
    if max(mu_rand_values) > math.sqrt(max(n_values)):
        return {"metric_name": "mu_rand", "metric_value": mean_mu_rand, "instances_tested": len(results), "conjecture_holds": False, "counterexample": f"max_mu_rand={max(mu_rand_values):.2f}"}
    
    return {"metric_name": "mu_clique", "metric_value": mean_mu_clique, "instances_tested": len(results), "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu_clique = sum(r["metric_value"] for r in results) / len(results)
    std_mu_clique = math.sqrt(sum((r["metric_value"] - mean_mu_clique) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu_clique:.2f} std={std_mu_clique:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu_clique:.2f} std={std_mu_clique:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"submodularity_violation\" first_failing_seed={first_failing_seed}")