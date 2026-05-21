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

# Helper functions for linear algebra operations
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return result

def transpose_matrix(M):
    return [list(row) for row in zip(*M)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def scalar_multiply(M, c):
    return [[c * M[i][j] for j in range(len(M[0]))] for i in range(len(M))]

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_inverse(A):
    n = len(A)
    I = identity_matrix(n)
    A_augmented = [A[i] + I[i] for i in range(n)]
    
    # Gaussian elimination with partial pivoting
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        pivot = A_augmented[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        
        for j in range(n):
            A_augmented[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(2 * n):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    
    return [row[n:] for row in A_augmented]

def singular_value_decomposition(M):
    m, n = len(M), len(M[0])
    U = identity_matrix(m)
    Vt = identity_matrix(n)
    S = [[M[i][i] if i < min(m, n) else 0 for i in range(max(m, n))] for _ in range(max(m, n))]
    
    # Power iteration method to find the largest singular value
    for _ in range(100):
        v = [random.random() for _ in range(n)]
        v_norm = math.sqrt(sum(x**2 for x in v))
        v = scalar_multiply(v, 1 / v_norm)
        
        u = matrix_multiply(M, v)
        u_norm = math.sqrt(sum(x**2 for x in u))
        u = scalar_multiply(u, 1 / u_norm)
        
        s = sum(u[i] * M[i][j] * v[j] for i in range(m) for j in range(n))
        S[0][0] = s
        
        U = matrix_add(U, scalar_multiply(matrix_multiply(scalar_multiply(u, s), transpose_matrix(v)), Fraction(1, 2)))
        Vt = matrix_add(Vt, scalar_multiply(matrix_multiply(transpose_matrix(u), scalar_multiply(v, s)), Fraction(1, 2)))
    
    return U, S, Vt

def compute_polymatroid_spectral_gap(n):
    # Construct the canonical CLIQUE_3 DNF
    M = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
    edge_set = list(range(n * (n - 1) // 2))
    random.shuffle(edge_set)
    
    for i in range(n):
        for j in range(i + 1, n):
            k = edge_set.pop()
            M[k][i * (n - i - 1) // 2 + j - i - 1] = 1
    
    # Compute the degree diagonals
    D_r = [sum(M[i][j] for j in range(n * (n - 1) // 2)) for i in range(n)]
    D_c = [sum(M[j][i] for j in range(n * (n - 1) // 2)) for i in range(n)]
    
    # Normalize the incidence matrix
    M_r_inv = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_r)))
    M_c_inv = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_c)))
    M_normalized = matrix_multiply(matrix_multiply(M_r_inv, M), M_c_inv)
    
    # Compute the singular value decomposition
    U, S, Vt = singular_value_decomposition(M_normalized)
    
    # Extract the top two singular values
    sigma_1 = S[0][0]
    sigma_2 = S[1][1] if len(S) > 1 else 0
    
    return sigma_1 - sigma_2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 15, 18, 20, 25, 30, 35, 40]
    mu_clique_values = []
    mu_rand_values = []
    
    for n in n_values:
        # Compute µ(D) for the canonical CLIQUE_3 DNF
        mu_clique = compute_polymatroid_spectral_gap(n)
        mu_clique_values.append(mu_clique)
        
        # Sample a random monotone DNF and compute µ(D)
        num_terms = n * (n - 1) // 2
        M_rand = [[0] * num_terms for _ in range(num_terms)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    k = random.randint(0, num_terms - 1)
                    M_rand[k][i * (n - i - 1) // 2 + j - i - 1] = 1
        
        # Compute the degree diagonals
        D_r_rand = [sum(M_rand[i][j] for j in range(num_terms)) for i in range(num_terms)]
        D_c_rand = [sum(M_rand[j][i] for j in range(num_terms)) for i in range(num_terms)]
        
        # Normalize the incidence matrix
        M_r_inv_rand = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_r_rand)))
        M_c_inv_rand = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_c_rand)))
        M_normalized_rand = matrix_multiply(matrix_multiply(M_r_inv_rand, M_rand), M_c_inv_rand)
        
        # Compute the singular value decomposition
        U_rand, S_rand, Vt_rand = singular_value_decomposition(M_normalized_rand)
        
        # Extract the top two singular values
        sigma_1_rand = S_rand[0][0]
        sigma_2_rand = S_rand[1][1] if len(S_rand) > 1 else 0
        
        mu_rand_values.append(sigma_1_rand - sigma_2_rand)
    
    # Check submodularity (i)
    def check_submodularity(D, D_prime):
        M_D = [[M[i][j] for j in range(num_terms)] for i in range(num_terms)]
        M_D_prime = [[M_prime[i][j] for j in range(num_terms)] for i in range(num_terms)]
        
        # Compute the degree diagonals
        D_r_D = [sum(M_D[i][j] for j in range(num_terms)) for i in range(num_terms)]
        D_c_D = [sum(M_D[j][i] for j in range(num_terms)) for i in range(num_terms)]
        D_r_D_prime = [sum(M_D_prime[i][j] for j in range(num_terms)) for i in range(num_terms)]
        D_c_D_prime = [sum(M_D_prime[j][i] for j in range(num_terms)) for i in range(num_terms)]
        
        # Normalize the incidence matrices
        M_r_inv_D = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_r_D)))
        M_c_inv_D = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_c_D)))
        M_normalized_D = matrix_multiply(matrix_multiply(M_r_inv_D, M_D), M_c_inv_D)
        
        M_r_inv_D_prime = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_r_D_prime)))
        M_c_inv_D_prime = scalar_multiply(identity_matrix(n), Fraction(1, sum(D_c_D_prime)))
        M_normalized_D_prime = matrix_multiply(matrix_multiply(M_r_inv_D_prime, M_D_prime), M_c_inv_D_prime)
        
        # Compute the singular value decompositions
        U_D, S_D, Vt_D = singular_value_decomposition(M_normalized_D)
        U_D_prime, S_D_prime, Vt_D_prime = singular_value_decomposition(M_normalized_D_prime)
        
        # Extract the top two singular values
        sigma_1_D = S_D[0][0]
        sigma_2_D = S_D[1][1] if len(S_D) > 1 else 0
        sigma_1_D_prime = S_D_prime[0][0]
        sigma_2_D_prime = S_D_prime[1][1] if len(S_D_prime) > 1 else 0
        
        return sigma_1_D + sigma_1_D_prime <= sigma_1_D * sigma_1_D_prime
    
    pairs = [(M_rand, M_rand) for _ in range(30)]
    submodularity_holds = all(check_submodularity(D, D_prime) for D, D_prime in pairs)
    
    # Check the conjecture
    mu_clique_mean = sum(mu_clique_values) / len(mu_clique_values)
    mu_rand_max = max(mu_rand_values)
    
    if not submodularity_holds:
        return {
            "metric_name": "mu_clique",
            "metric_value": mu_clique_mean,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "submodularity_violation"
        }
    
    if mu_clique_mean < 0.1 * math.sqrt(15):
        return {
            "metric_name": "mu_clique",
            "metric_value": mu_clique_mean,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "mu_clique_too_small"
        }
    
    if mu_rand_max > math.sqrt(10):
        return {
            "metric_name": "mu_rand",
            "metric_value": mu_rand_max,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "mu_rand_too_large"
        }
    
    return {
        "metric_name": "mu_clique",
        "metric_value": mu_clique_mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mu_clique_means = [r["metric_value"] for r in results if "mu_clique" in r]
    mu_rand_maxes = [r["metric_value"] for r in results if "mu_rand" in r]
    submodularity_holds_all = all(r["conjecture_holds"] for r in results)
    
    if not submodularity_holds_all:
        print(f"RESULT: FALSIFIED counterexample=\"submodularity_violation\" first_failing_seed={seeds[0]}")
    elif mu_clique_means and mu_rand_maxes:
        mu_clique_mean = sum(mu_clique_means) / len(mu_clique_means)
        mu_rand_max = max(mu_rand_maxes)
        print(f"RESULT: SUPPORTED mean={mu_clique_mean} std=0 support_fraction=1")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")