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
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def is_independent_system(A, b):
    try:
        gaussian_elimination(A, b)
        return True
    except ZeroDivisionError:
        return False

def generate_tseitin_instance(n):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(1, n+1):
        clauses.append([i])
        clauses.append([-i])
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            clauses.append([i, -j])
            clauses.append([-i, j])
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            variables, clauses = generate_tseitin_instance(n)
            A = [[1 if i == abs(j) else 0 for j in range(1, n+1)] for i in range(1, n+1)]
            b = [1 if i % 2 == 1 else -1 for i in range(1, n+1)]
            
            if not is_independent_system(A, b):
                conjecture_holds = False
                counterexample = f"n={n}, independent system found"
                break
            
            instances_tested += 1
        
        results.append({
            "metric_name": "instances_tested",
            "metric_value": instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")