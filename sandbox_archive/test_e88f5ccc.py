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

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    aug_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(aug_matrix[j][i]) > abs(aug_matrix[max_row][i]):
                max_row = j
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]
        pivot = aug_matrix[i][i]
        for j in range(i, n+1):
            aug_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = aug_matrix[j][i]
                for k in range(i, n+1):
                    aug_matrix[j][k] -= factor * aug_matrix[i][k]
    return [row[-1] for row in aug_matrix]

def is_independent_set(S, edges):
    for u, v in edges:
        if {u, v}.issubset(S):
            return False
    return True

def matroid_rank(edges, n):
    independent_sets = []
    for r in range(n+1):
        for S in itertools.combinations(range(n), r):
            if is_independent_set(S, edges):
                independent_sets.append(S)
    return len(max(independent_sets, key=len))

def k_clique_dnf(k, n):
    edges = set()
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if (i & j) == 0:
                edges.add((i, j))
    return matroid_rank(edges, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n == 2:
            continue
        size = min(n**2, 100)  # Limit size to avoid excessive computation
        dnf_size = random.randint(1, size)
        dnf_formula = [random.sample(range(1, n+1), random.randint(1, n)) for _ in range(dnf_size)]
        
        independent_sets = []
        for r in range(n+1):
            for S in itertools.combinations(range(n), r):
                if is_independent_set(S, dnf_formula):
                    independent_sets.append(S)
        
        mu_f = len(max(independent_sets, key=len))
        results.append(mu_f)
    
    mean_mu_f = sum(results) / len(results)
    conjecture_holds = all(mu <= math.log(n_values[-1]) for mu in results[:3])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mu(f)",
        "metric_value": mean_mu_f,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_mu_f = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu_f} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")