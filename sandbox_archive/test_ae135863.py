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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    def swap_rows(i, j):
        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
    
    def scale_row(i, c):
        augmented_matrix[i] = [c * x for x in augmented_matrix[i]]
    
    def add_multiple_of_row(i, j, c):
        augmented_matrix[j] = [a + b * c for a, b in zip(augmented_matrix[j], augmented_matrix[i])]
    
    pivot_row = 0
    for col in range(n):
        if pivot_row >= m:
            break
        
        max_pivot = abs(augmented_matrix[pivot_row][col])
        max_row = pivot_row
        for i in range(pivot_row + 1, m):
            if abs(augmented_matrix[i][col]) > max_pivot:
                max_pivot = abs(augmented_matrix[i][col])
                max_row = i
        
        if max_pivot == 0:
            continue
        
        swap_rows(pivot_row, max_row)
        
        scale_row(pivot_row, Fraction(1, augmented_matrix[pivot_row][col]))
        
        for i in range(m):
            if i != pivot_row:
                add_multiple_of_row(pivot_row, i, -augmented_matrix[i][col])
        
        pivot_row += 1
    
    return [row[:-1] for row in augmented_matrix]

def rank(matrix):
    A = matrix
    m, n = len(A), len(A[0])
    rref = gaussian_elimination(A, [0] * n)
    rank = sum(1 for row in rref if any(row[i] != 0 for i in range(n)))
    return rank

def generate_monotone_kclique_instance(n):
    variables = list(range(n))
    clauses = []
    for _ in range(n // 2):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return variables, clauses

def tropicalized_birkhoff_polytope_rank(variables, clauses):
    n = len(variables)
    m = len(clauses)
    
    A = [[0] * (n + m) for _ in range(n)]
    b = [1] * n
    
    for i in range(m):
        clause = clauses[i]
        for j in clause:
            A[j][i + n] = 1
        b[clause[0]] += 1
        b[clause[1]] += 1
    
    return rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables, clauses = generate_monotone_kclique_instance(n)
            rank_value = tropicalized_birkhoff_polytope_rank(variables, clauses)
            results.append((n, rank_value))
    
    mean_rank = sum(rank_value for n, rank_value in results) / len(results)
    std_dev = math.sqrt(sum((rank_value - mean_rank) ** 2 for n, rank_value in results) / len(results))
    
    conjecture_holds = all(mean_rank >= n ** 0.5 for n, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(abs(result["metric_value"] - n ** 0.5) > n ** 0.5 * 0.2 for n, _ in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")