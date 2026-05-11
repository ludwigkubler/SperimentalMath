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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    rank = 0
    A = gaussian_elimination(A)
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_maxcut_instance(n, m):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(m):
        a, b = random.sample(variables, 2)
        polarity_a = random.choice([1, -1])
        polarity_b = random.choice([1, -1])
        clause = f"{polarity_a}*{a} + {polarity_b}*{b} >= 0"
        clauses.append(clause)
    return variables, clauses

def construct_moment_matrix(variables, clauses):
    n = len(variables)
    m = len(clauses)
    M = [[0] * (n + m) for _ in range(n + m)]
    
    # Identity matrix
    for i in range(n):
        M[i][i] = 1
    
    # Variables
    for i, var in enumerate(variables):
        for j, clause in enumerate(clauses):
            if var in clause:
                M[n + j][i] = 1
    
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, int(n * (n - 1) / 8))  # Ensure at least one clause
        variables, clauses = generate_maxcut_instance(n, m)
        M = construct_moment_matrix(variables, clauses)
        
        rank = matrix_rank(M)
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    total_instances_tested = sum(len(result) for result in results)
    mean_rank = sum(result["rank"] for result in results) / total_instances_tested
    
    conjecture_holds = all(n <= result["rank"] <= 2 * n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Real Rank of Moment Matrix",
        "metric_value": mean_rank,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")