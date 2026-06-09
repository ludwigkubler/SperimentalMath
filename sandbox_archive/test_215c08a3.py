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

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        factor = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= factor
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    return [row[-1] for row in augmented_matrix]

def compute_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(abs(matrix[j][i]) < 1e-9 for j in range(rank)):
            continue
        rank += 1
        factor = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def generate_language_instance(n):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def compute_communication_complexity_rank(clauses):
    n = len(clauses)
    G = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            if any(var in clauses[i] and var in clauses[j] for var in variables):
                G[i][j] = 1
                G[j][i] = 1
    
    return compute_rank(G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            clauses = generate_language_instance(n)
            rank = compute_communication_complexity_rank(clauses)
            results.append(rank)
    
    mean_value = sum(results) / len(results)
    variance = sum((x - mean_value)**2 for x in results) / len(results)
    conjecture_holds = variance >= math.log(len(results))
    counterexample = "" if conjecture_holds else f"Variance {variance} < log({len(results)})={math.log(len(results))}"
    
    return {
        "metric_name": "Communication Complexity Rank Variance",
        "metric_value": variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    variance = sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={variance} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Variance < log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")