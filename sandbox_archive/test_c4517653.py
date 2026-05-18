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

def matrix_multiply(A, B):
    if not A or not B:
        return []
    
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
                
    return result

def power_iteration(B, max_iter=50):
    n = len(B)
    x = [[random.choice([1, -1]) for _ in range(n)] for _ in range(1)]
    
    for _ in range(max_iter):
        x_new = matrix_multiply(B, x)
        norm_x_new = sum(x_new[i][j] ** 2 for i in range(n) for j in range(n)) ** 0.5
        if norm_x_new == 0:
            break
        x = [[x_new[i][j] / norm_x_new for j in range(n)] for i in range(n)]
        
    max_eigenvalue = sum(x[i][j] * B[i][j] for i in range(n) for j in range(n)) ** 0.5
    return max_eigenvalue, x

def spectral_norm(B):
    if not B or not B[0]:
        return 0
    
    n = len(B)
    max_eigenvalue, _ = power_iteration(B)
    return max_eigenvalue

def free_cumulants(M):
    N = len(M)
    B = matrix_multiply(M, M)
    s1 = sum(sum(M[i][j] for j in range(N)) for i in range(N)) / (N ** 2)
    s2 = spectral_norm(B) ** 2 / (N ** 3)
    s3 = sum(sum(B[i][j] * B[k][l] for l in range(N)) for k in range(N) for j in range(N)) / (N ** 4)
    s4 = spectral_norm(matrix_multiply(B, B)) ** 2 / (N ** 5)
    
    κ2 = s2 - s1 ** 2
    κ4 = s4 - 4 * s1 * s3 - 2 * s2 ** 2 + 10 * s1 ** 2 * s2 - 5 * s1 ** 4
    
    return κ2, κ4

def bridge_invariant(M):
    N = len(M)
    B = matrix_multiply(M, M)
    max_eigenvalue, _ = power_iteration(B)
    
    if max_eigenvalue == 0:
        return float('-inf')
    
    κ2, κ4 = free_cumulants(M)
    term1 = math.log2(1 + abs(κ4 / (κ2 ** 2 + N ** -2)))
    term2 = math.log2(max_eigenvalue ** 2 / N ** 2)
    
    return min(term1, term2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        N = 2 ** (n - 1)
        
        # M_{DISJ_n}
        M_disj = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        tau_disj = bridge_invariant(M_disj)
        results.append({
            "metric_name": "tau_disj",
            "metric_value": tau_disj,
            "instances_tested": 1,
            "conjecture_holds": tau_disj >= 0.15 * n,
            "counterexample": ""
        })
        
        # Random ±1 sign matrices
        for _ in range(30):
            M_random = [[random.choice([1, -1]) for _ in range(N)] for _ in range(N)]
            tau_random = bridge_invariant(M_random)
            results.append({
                "metric_name": "tau_random",
                "metric_value": tau_random,
                "instances_tested": 1,
                "conjecture_holds": tau_random >= 0.15 * n,
                "counterexample": ""
            })
        
        # Low-rank decoys
        for k in [1, 2, 4, 8, 16, 32]:
            M_decoy = [[random.choice([1, -1]) for _ in range(k)] for _ in range(N)]
            U, _, Vt = matrix_decomposition(M_decoy)
            M_decoy = matrix_multiply(U, Vt)
            tau_decoy = bridge_invariant(M_decoy)
            results.append({
                "metric_name": "tau_decoy",
                "metric_value": tau_decoy,
                "instances_tested": 1,
                "conjecture_holds": tau_decoy >= 0.15 * n,
                "counterexample": ""
            })
        
        # Hadamard/IP_2 matrices
        if N in [16, 64, 256]:
            M_hadamard = hadamard_matrix(N)
            tau_hadamard = bridge_invariant(M_hadamard)
            results.append({
                "metric_name": "tau_hadamard",
                "metric_value": tau_hadamard,
                "instances_tested": 1,
                "conjecture_holds": tau_hadamard >= 0.15 * n,
                "counterexample": ""
            })
    
    mean_tau = sum(result["metric_value"] for result in results) / len(results)
    std_tau = (sum((result["metric_value"] - mean_tau) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "mean": mean_tau,
        "std": std_tau,
        "support_fraction": support_fraction
    }

def matrix_decomposition(M):
    n = len(M)
    U = [[0 for _ in range(n)] for _ in range(n)]
    Vt = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        max_index = 0
        max_value = abs(M[i][0])
        
        for j in range(1, n):
            if abs(M[i][j]) > max_value:
                max_value = abs(M[i][j])
                max_index = j
        
        U[i][max_index] = M[i][max_index]
        Vt[max_index][i] = 1 / M[i][max_index]
        
        for j in range(n):
            if j != i:
                factor = M[j][max_index] / M[i][max_index]
                M[j][max_index] = 0
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
    
    return U, Vt, Vt

def hadamard_matrix(N):
    if N == 1:
        return [[1]]
    
    H_half = hadamard_matrix(N // 2)
    H = [[0 for _ in range(N)] for _ in range(N)]
    
    for i in range(N // 2):
        for j in range(N // 2):
            H[i][j] = H_half[i][j]
            H[i + N // 2][j] = H_half[i][j]
            H[i][j + N // 2] = H_half[i][j]
            H[i + N // 2][j + N // 2] = -H_half[i][j]
    
    return H

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"mean\": {trial_result['mean']:.6f}, \"std\": {trial_result['std']:.6f}, \"support_fraction\": {trial_result['support_fraction']:.4f}}}")
        results.append(trial_result)
    
    overall_mean = sum(result["mean"] for result in results) / len(results)
    overall_std = (sum((result["mean"] - overall_mean) ** 2 for result in results) / len(results)) ** 0.5
    overall_support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.95) / len(results)
    
    if overall_support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={overall_mean:.6f} std={overall_std:.6f} support_fraction={overall_support_fraction:.4f}")
    elif any(result["support_fraction"] < 0.95 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.95)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_below_95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")