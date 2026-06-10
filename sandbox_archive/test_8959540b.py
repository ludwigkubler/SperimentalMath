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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(i, n + 1):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n + 1):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    r = 0
    for row in A_copy:
        if any(row):
            r += 1
    return r

def tseitin_formula(G, n):
    clauses = []
    literals = {}
    var_id = 1
    for i in range(n):
        literals[i] = var_id
        var_id += 1
        clauses.append([literals[i]])
    
    for u, v in G:
        literal_u = literals[u]
        literal_v = literals[v]
        new_var_id = var_id
        literals[(u, v)] = new_var_id
        var_id += 1
        
        clauses.append([-literal_u, -new_var_id])
        clauses.append([-literal_v, -new_var_id])
        clauses.append([literal_u, literal_v, new_var_id])
    
    return clauses

def resolution_width(clauses):
    queue = [0] * len(clauses)
    for i in range(len(queue)):
        queue[i] = random.randint(1, 2 * len(clauses))
    width = 0
    while True:
        u, v = random.sample(queue, 2)
        if u == v:
            continue
        new_clause = []
        for lit in clauses[u]:
            if -lit not in clauses[v]:
                new_clause.append(lit)
        if len(new_clause) == 0:
            return width
        queue.append(len(clauses))
        clauses.append(new_clause)
        width += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = 2 * (n - 1)
    G = []
    for _ in range(d * n // 2):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in G and (v, u) not in G:
            G.append((u, v))
    
    clauses = tseitin_formula(G, n)
    width = resolution_width(clauses)
    k_theory_rank = rank([[1] * n])
    
    return {
        "metric_name": "Resolution Width vs K-Theory Rank",
        "metric_value": width / k_theory_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= 3 * k_theory_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")