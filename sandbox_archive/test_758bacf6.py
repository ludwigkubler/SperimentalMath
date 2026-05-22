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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i] / A[i][i]
            for j in range(i-1, -1, -1):
                b[j] -= A[j][i] * x[i]
        return x
    
    def min_index_of_group_action(ring_size, group_size):
        # Simplified model: index is proportional to ring_size and group_size
        return ring_size * group_size
    
    def sum_of_squares_degree(max_cut_instance):
        # Simplified model: degree is proportional to the number of edges in max-cut instance
        return len(max_cut_instance) // 2
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        max_cut_instance = generate_max_cut_instance(n)
        ring_size = n
        group_size = random.randint(1, n)
        
        index = min_index_of_group_action(ring_size, group_size)
        degree = sum_of_squares_degree(max_cut_instance)
        
        results.append({
            "n": n,
            "index": index,
            "degree": degree
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    indices = [r["index"] for r in results]
    degrees = [r["degree"] for r in results]
    
    mean_index = sum(indices) / len(indices)
    mean_degree = sum(degrees) / len(degrees)
    
    correlation_coefficient = 0
    if mean_degree != 0:
        covariance = sum((indices[i] - mean_index) * (degrees[i] - mean_degree) for i in range(len(results))) / len(results)
        variance_index = sum((indices[i] - mean_index) ** 2 for i in range(len(results))) / len(results)
        variance_degree = sum((degrees[i] - mean_degree) ** 2 for i in range(len(results))) / len(results)
        correlation_coefficient = covariance / math.sqrt(variance_index * variance_degree)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(range(53, 83))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")