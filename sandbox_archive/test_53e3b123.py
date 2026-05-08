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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [row + [b[i]] for i, row in enumerate(A)]
    
    # Forward elimination
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A_augmented[r][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        for j in range(i + 1, n):
            factor = A_augmented[j][i] / A_augmented[i][i]
            A_augmented[j] = [A_augmented[j][k] - factor * A_augmented[i][k] for k in range(n + 1)]
    
    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i + 1, n))) / A_augmented[i][i]
    
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def zeta_inversion(A):
    n = len(A)
    A_inv = [[0] * n for _ in range(n)]
    for i in range(n):
        A_inv[i][i] = 1
    for k in range(1, n + 1):
        B = matrix_multiply(A_inv, A)
        C = [[A_inv[i][j] - B[i][j] / k for j in range(n)] for i in range(n)]
        A_inv = C
    return A_inv

def mobius_function(L):
    n = len(L)
    mu = [0] * (1 << n)
    mu[0] = 1
    for i in range(1, 1 << n):
        if L[i].issubset(L[i - 1]):
            mu[i] = -mu[i - 1]
        else:
            j = i & -i
            k = i ^ j
            mu[i] = mu[k] - mu[j]
    return mu

def compute_L(F, N):
    L = {frozenset(), frozenset(range(N))}
    for m in F:
        L.add(frozenset(m))
    return sorted(L, key=len)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_graphs = [4, 5, 6, 7]
    k = 3
    max_s = {n: n * (n - 1) // 2 for n in n_graphs}
    num_samples = 30
    
    results = []
    for n_graph in n_graphs:
        N = n_graph * (n_graph - 1) // 2
        s_values = [n_graph, 2 * n_graph, 4 * n_graph, 8 * n_graph]
        
        # Compute Λ(F_triangle)
        F_triangle = [[i, j] for i in range(n_graph) for j in range(i + 1, n_graph)]
        L_triangle = compute_L(F_triangle, N)
        mu_triangle = mobius_function(L_triangle)
        Lambda_triangle = sum(abs(mu_triangle[0]) for x in L_triangle if x != frozenset())
        
        results.append({
            "n_graph": n_graph,
            "Lambda_triangle": Lambda_triangle
        })
    
    return {
        "metric_name": "Lambda",
        "metric_value": max(result["Lambda_triangle"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["Lambda_triangle"] >= (1/8) * n_graph * math.log2(n_graph) for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Lambda(F_triangle) < (1/8)n log2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")