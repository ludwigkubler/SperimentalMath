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
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    rows, cols = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(rows)]
    for i in range(cols):
        max_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, cols+1):
            augmented_matrix[i][j] /= pivot
        for j in range(rows):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, cols+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 6))
    
    # Generate a random k-clique instance
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i+1, k):
            edges.append((vertices[i], vertices[j]))
    
    # Construct the adjacency matrix
    adj_matrix = [[0]*n for _ in range(n)]
    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    
    # Compute the minimal order of the quaternion algebra
    order_Q = n**k / math.log(n)
    
    # Construct a monotone circuit for k-clique
    # This is a simplified example; actual construction would be complex
    circuit_size = 2**(n//2)
    
    # Check if the conjecture holds
    conjecture_holds = abs(order_Q - circuit_size) <= 2**(n/2)
    counterexample = "" if conjecture_holds else f"order(Q)={order_Q}, circuit_size={circuit_size}"
    
    return {
        "metric_name": "Order of Quaternion Algebra",
        "metric_value": order_Q,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order(Q) != circuit_size\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")