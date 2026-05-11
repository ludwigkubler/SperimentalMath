# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def create_symmetric_tensor(n, clauses):
    tensor = [[0] * n for _ in range(n)]
    for clause in clauses:
        for i in clause:
            for j in clause:
                tensor[i-1][j-1] += 1
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = random.randint(n, n * (n - 1))
    
    # Generate a random CNF formula
    clauses = []
    for _ in range(num_clauses):
        clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
        clauses.append(clause)
    
    # Convert to symmetric tensor
    A = create_symmetric_tensor(n, clauses)
    
    # Compute symmetric tensor rank
    tensor_rank = rank(A)
    
    # The conjecture states that the permanent's rank is Ω(n²) and determinant's rank is O(n)
    # For simplicity, we will check if the rank is at least n^2 for a random permutation of variables
    permuted_clauses = [set(random.sample(range(1, n + 1), len(clause))) for clause in clauses]
    permuted_A = create_symmetric_tensor(n, permuted_clauses)
    permuted_rank = rank(permuted_A)
    
    # Check if the rank is at least n^2
    conjecture_holds = permuted_rank >= n**2
    
    return {
        "metric_name": "symmetric_tensor_rank",
        "metric_value": tensor_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rank < n^2"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < n^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")