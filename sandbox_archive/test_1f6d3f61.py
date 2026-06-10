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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def rank(A):
    m, n = len(A), len(A[0])
    RREF = gaussian_elimination(A, [0]*m)
    rank = 0
    for row in RREF:
        if any(row):
            rank += 1
    return rank

def p_adic_valuation(n, p):
    count = 0
    while n % p == 0 and n > 0:
        n //= p
        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        p_adic_valuation_sum = 0
        rank_variance_sum = 0
        for _ in range(5):
            # Generate a random communication complexity instance
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            b = [random.randint(0, 1) for _ in range(n)]
            
            # Compute the associated matroid and its p-adic valuation
            rank_matroid = rank(A)
            p_adic_valuation_val = sum(p_adic_valuation(sum(row), 2) for row in A)
            
            # Calculate the rank variance of the communication complexity problem
            rank_variance = (sum((A[i][j] - b[j])**2 for i in range(n)) / n)**0.5
            
            p_adic_valuation_sum += p_adic_valuation_val
            rank_variance_sum += rank_variance
            instances_tested += 1
        
        mean_p_adic_valuation = p_adic_valuation_sum / instances_tested
        mean_rank_variance = rank_variance_sum / instances_tested
        
        results.append({
            "n": n,
            "mean_p_adic_valuation": mean_p_adic_valuation,
            "mean_rank_variance": mean_rank_variance
        })
    
    if len(results) < 30:
        return {
            "metric_name": "p-adic Valuation Rank Variance Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    correlation_sum = 0
    p_adic_valuation_mean = sum(result["mean_p_adic_valuation"] for result in results) / len(results)
    rank_variance_mean = sum(result["mean_rank_variance"] for result in results) / len(results)
    
    for result in results:
        correlation_sum += (result["mean_p_adic_valuation"] - p_adic_valuation_mean) * (result["mean_rank_variance"] - rank_variance_mean)
    
    variance_p_adic_valuation = sum((result["mean_p_adic_valuation"] - p_adic_valuation_mean)**2 for result in results) / len(results)
    variance_rank_variance = sum((result["mean_rank_variance"] - rank_variance_mean)**2 for result in results) / len(results)
    
    correlation_coefficient = correlation_sum / (math.sqrt(variance_p_adic_valuation * variance_rank_variance))
    
    return {
        "metric_name": "p-adic Valuation Rank Variance Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient <= 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_samples")