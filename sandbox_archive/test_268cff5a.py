# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def xor(a, b):
    return a ^ b

def add_vectors(v1, v2):
    return [xor(v1[i], v2[i]) for i in range(len(v1))]

def scalar_multiply(vector, scalar):
    return [vector[i] * scalar for i in range(len(vector))]

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] ^= A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] ^= scalar_multiply(augmented_matrix[i], 1 / pivot)
        
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] ^= scalar_multiply(augmented_matrix[i], factor)
    
    return [row[n] for row in augmented_matrix]

def generate_3xor_instance(n, alpha):
    m = int(alpha * n * (n - 1) / 2)
    A = []
    while len(A) < m:
        a = random.randint(0, 2**n - 1)
        b = random.randint(0, 2**n - 1)
        if xor(a, b) not in A:
            A.append(xor(a, b))
    return A

def compute_sigma(A):
    set_A = {xor(a, b) for a in A for b in A}
    return math.log2(len(set_A)) - math.log2(len(A + A))

def compute_g_star(F, n):
    m = len(F)
    A = [F[i][0] for i in range(m)]
    b = [F[i][1] for i in range(m)]
    
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    g_star = 0
    while any(row[-1] != 0 for row in augmented_matrix):
        pivot_row = next(i for i, row in enumerate(augmented_matrix) if row[-1] != 0)
        pivot_col = next(j for j, val in enumerate(augmented_matrix[pivot_row]) if val != 0)
        
        g_star += 1
        for i in range(m):
            if i != pivot_row:
                factor = augmented_matrix[i][pivot_col]
                for j in range(n + 1):
                    augmented_matrix[i][j] ^= scalar_multiply(augmented_matrix[pivot_row], factor)
    
    return g_star

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14, 16]
    alpha_values = [1.2, 2.0, 3.0]
    trials_per_cell = 200
    total_trials = len(n_values) * len(alpha_values) * trials_per_cell
    
    results = []
    for n in n_values:
        for alpha in alpha_values:
            for _ in range(trials_per_cell):
                F = generate_3xor_instance(n, alpha)
                A = [F[i][0] for i in range(len(F))]
                
                sigma_A = compute_sigma(A)
                g_star_F = compute_g_star(F, n)
                
                results.append({
                    "n": n,
                    "alpha": alpha,
                    "sigma_A": sigma_A,
                    "g_star_F": g_star_F
                })
    
    mean_gap = sum(result["g_star_F"] - result["sigma_A"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["g_star_F"] >= result["sigma_A"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.99
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "gap",
        "metric_value": mean_gap,
        "instances_tested": total_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
    
    mean_gap = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_gap} std=undefined support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")