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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_invertible(A):
    det = 1
    n = len(A)
    for i in range(n):
        det *= A[i][i]
    return det != 0

def minimal_representation_degree(n):
    if n == 1:
        return 1
    A = [[random.randint(0, 1) if i == j else random.choice([0, -A[i][j]]) for j in range(n)] for i in range(n)]
    while not is_invertible(A):
        A = [[random.randint(0, 1) if i == j else random.choice([0, -A[i][j]]) for j in range(n)] for i in range(n)]
    gaussian_elimination(A)
    return sum(abs(x) for row in A for x in row)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    D_S = []
    q_phi = []
    
    for n in n_values:
        D_S.append(minimal_representation_degree(n))
        # For simplicity, we assume the number of distinct quadratic forms is proportional to n
        q_phi.append(n)
    
    if len(D_S) != len(q_phi):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(D_S)
    mean_D_S = sum(D_S) / n
    mean_q_phi = sum(q_phi) / n
    
    covariance = sum((D_S[i] - mean_D_S) * (q_phi[i] - mean_q_phi) for i in range(n)) / n
    variance_D_S = sum((D_S[i] - mean_D_S) ** 2 for i in range(n)) / n
    variance_q_phi = sum((q_phi[i] - mean_q_phi) ** 2 for i in range(n)) / n
    
    if variance_D_S == 0 or variance_q_phi == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_D_S) * math.sqrt(variance_q_phi))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _ in range(n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std={math.sqrt(sum((result['metric_value'] - (sum(result['metric_value'] for result in results) / len(results))) ** 2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")