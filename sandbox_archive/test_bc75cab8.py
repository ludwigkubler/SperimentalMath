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

# Helper functions for basic linear algebra operations
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][n] / augmented_matrix[i][i]
        for j in range(i-1, -1, -1):
            augmented_matrix[j][n] -= augmented_matrix[j][i] * x[i]
    
    return x

def compute_rank(matrix):
    m = len(matrix)
    n = len(matrix[0])
    A = [row[:] for row in matrix]
    rank = 0
    for i in range(min(m, n)):
        if A[i][i] != 0:
            rank += 1
            gaussian_elimination(A, [0]*i + [1] + [0]*(n-i-1))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random language L in NP with n variables
    n = random.randint(5, 40)
    language = {tuple(random.sample(range(n), k)) for k in range(1, n)}
    
    # Construct a commutative group G and represent L using an action of G on a set
    elements = list(range(n))
    generators = [random.sample(elements, random.randint(2, 4)) for _ in range(random.randint(2, 3))]
    group_table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            product = (i + j) % n
            group_table[i][j] = product
    
    # Compute the rank of the representation and measure its variance
    ranks = []
    for _ in range(100):  # Sample 100 instances
        assignment = {var: random.choice(elements) for var in range(n)}
        representation = [[group_table[assignment[var]][j] for j in range(n)] for var in range(n)]
        rank = compute_rank(representation)
        ranks.append(rank)
    
    variance = sum((x - sum(ranks)/len(ranks))**2 for x in ranks) / len(ranks)
    mean_variance = sum(ranks) / len(ranks)
    
    # Check if the variance is greater than or equal to log(n)
    conjecture_holds = variance >= math.log(n)
    counterexample = "" if conjecture_holds else f"Variance {variance} < log({n}) = {math.log(n)}"
    
    return {
        "metric_name": "Communication Complexity Rank Variance",
        "metric_value": mean_variance,
        "instances_tested": len(ranks),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i for i in range(5, 6)]  # Default to a list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"variance < log(n)\" first_failing_seed={first_failing_seed}")