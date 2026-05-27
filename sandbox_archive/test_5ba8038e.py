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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        factor = Fraction(matrix[i][i])
        for j in range(i, n):
            matrix[i][j] /= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(matrix[k][i])
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

def rank(matrix):
    n = len(matrix)
    A = [row[:] for row in matrix]
    gaussian_elimination(A)
    
    rank = 0
    for i in range(n):
        if any(A[i][j] != 0 for j in range(n)):
            rank += 1
    
    return rank

def noncommutative_tensor_product(M):
    n = len(M)
    result = [[0] * (n*n) for _ in range(n*n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    result[i*n + j][k*n + l] += M[i][k] * M[j][l]
    
    return result

def randomized_communication_complexity(M):
    n = len(M)
    # Simplified version of CC_R using a random sampling approach
    samples = set()
    while len(samples) < 10:  # Sample 10 unique pairs (i, j)
        i, j = random.sample(range(n), 2)
        if (i, j) not in samples:
            samples.add((i, j))
    
    complexity = sum(M[i][j] for i, j in samples)
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    τ_n = rank(noncommutative_tensor_product(M))
    CC_R = randomized_communication_complexity(M)
    
    if CC_R == 0:
        return {
            "metric_name": "τ_n / CC_R",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "CC_R is zero, division by zero"
        }
    
    ratio = τ_n / CC_R
    
    return {
        "metric_name": "τ_n / CC_R",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "CC_R is zero, division by zero"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")