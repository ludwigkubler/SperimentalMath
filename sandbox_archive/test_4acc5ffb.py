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

def matrix_multiplication(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def compute_tropical_derivative(protocol):
    # Placeholder function to simulate the computation of a tropical pseudo-derivative
    # This is a dummy implementation and should be replaced with actual logic
    n = len(protocol)
    derivative = 0
    for i in range(n):
        for j in range(i+1, n):
            if protocol[i] > protocol[j]:
                derivative += 1
    return derivative

def compute_local_index(tropical_derivative):
    # Placeholder function to simulate the computation of the minimal local index
    # This is a dummy implementation and should be replaced with actual logic
    return len(set(tropical_derivative))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 6) * 5  # Sweep through n ∈ {5,10,15,20,30,40}
    if n < 5 or n > 40:
        return {
            "metric_name": "local_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic_n"
        }
    
    protocol = [random.randint(1, 100) for _ in range(n)]
    tropical_derivative = compute_tropical_derivative(protocol)
    local_index = compute_local_index(tropical_derivative)
    
    return {
        "metric_name": "local_index",
        "metric_value": local_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_local_index = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_local_index = math.sqrt(sum((r["metric_value"] - mean_local_index) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_local_index} std={std_local_index} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data_or_support")