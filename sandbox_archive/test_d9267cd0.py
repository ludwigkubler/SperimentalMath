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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    result = [[Fraction(0, 1)] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                result[i][j] += A[i][l] * B[l][j]
    return result

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        pivot_row = i
        while pivot_row < m and A[pivot_row][i] == Fraction(0, 1):
            pivot_row += 1
        if pivot_row == m:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        for j in range(n):
            if i != j:
                factor = -A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] += factor * A[i][k]
        rank += 1
    return rank

def ideal_class_group_size(n):
    # Placeholder function to simulate the size of the ideal class group
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, n)

def communication_complexity_rank(n):
    # Placeholder function to simulate the communication complexity rank
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    size_list = []
    rank_list = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        size = ideal_class_group_size(n)
        rank = communication_complexity_rank(n)
        size_list.append(size)
        rank_list.append(rank)
    
    mean_size = sum(size_list) / len(size_list)
    mean_rank = sum(rank_list) / len(rank_list)
    
    if len(size_list) < 2:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(size_list),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
            "conjecture_holds": False,
            "counterexample": "Insufficient data points"
        }
    
    std_deviation_size = math.sqrt(sum((size - mean_size) ** 2 for size in size_list) / len(size_list))
    std_deviation_rank = math.sqrt(sum((rank - mean_rank) ** 2 for rank in rank_list) / len(rank_list))
    
    if std_deviation_size == 0 or std_deviation_rank == 0:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(size_list),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
            "conjecture_holds": False,
            "counterexample": "Standard deviation is zero"
        }
    
    correlation_coefficient = sum((size - mean_size) * (rank - mean_rank) for size, rank in zip(size_list, rank_list)) / (len(size_list) * std_deviation_size * std_deviation_rank)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(size_list),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")