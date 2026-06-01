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
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(Augmented[r][i]))
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(i + 1, n):
            factor = Augmented[j][i] / Augmented[i][i]
            for k in range(n + 1):
                Augmented[j][k] -= factor * Augmented[i][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (Augmented[i][-1] - sum(Augmented[i][j] * x[j] for j in range(i + 1, n))) / Augmented[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_size = 0
        total_rank = 0
        
        for _ in range(5):  # Sample 5 instances per size
            inputs = [random.randint(1, 100) for _ in range(n)]
            rank = len(inputs)
            size = rank  # Simplified example: size is equal to rank
            
            total_size += size
            total_rank += rank
            instances_tested += 1
        
        mean_size = total_size / instances_tested
        mean_rank = total_rank / instances_tested
        correlation_coefficient = (instances_tested * sum(size * rank for size, rank in zip([mean_size] * instances_tested, [mean_rank] * instances_tested)) - 
                                   instances_tested * mean_size * mean_rank) / \
                                  math.sqrt((instances_tested * sum(size ** 2 for size in [mean_size] * instances_tested) - instances_tested * mean_size ** 2) *
                                            (instances_tested * sum(rank ** 2 for rank in [mean_rank] * instances_tested) - instances_tested * mean_rank ** 2))
        
        results.append({
            "n": n,
            "size": size,
            "rank": rank,
            "correlation_coefficient": correlation_coefficient
        })
    
    mean_correlation = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["correlation_coefficient"] - mean_correlation) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["correlation_coefficient"]) >= mean_correlation - 2 * std_deviation and abs(result["correlation_coefficient"]) <= mean_correlation + 2 * std_deviation for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")