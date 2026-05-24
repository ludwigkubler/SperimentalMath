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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def matrix_multiplication(A, B):
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
        if i >= m:
            break
        pivot_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                pivot_row = j
        
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        
        for j in range(m):
            if i == j:
                continue
            factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    rank = n
    for i in range(n):
        if all(x == 0 for x in augmented_matrix[i]):
            rank -= 1
    
    return rank

def quasi_plurality_matrix(f, n):
    m = len(f)
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(m):
        for j in range(2**n):
            if f[i] == 1:
                matrix[j][j ^ i] += 1
    return matrix

def communication_complexity_disjointness(f, n):
    # Simplified version of the communication complexity for disjointness problem
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed for statistical signal
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        
        Q_f = quasi_plurality_matrix(f, n)
        c_f = communication_complexity_disjointness(f, n)
        
        rank_Q_f = gaussian_elimination(Q_f, [0] * (2**n))
        
        results.append({
            "metric_name": "Rank of Quasi-Plurality Matrix",
            "metric_value": rank_Q_f,
            "instances_tested": 1,
            "conjecture_holds": rank_Q_f <= c_f ** 2,  # Example polynomial function
            "counterexample": "" if rank_Q_f <= c_f ** 2 else f"Rank({rank_Q_f}) > {c_f}^2"
        })
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "std_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["mean_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["mean_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if all(result["support_fraction"] == 1 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")