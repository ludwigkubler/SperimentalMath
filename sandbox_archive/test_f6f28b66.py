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

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(matrix):
    n = len(matrix)
    T = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            T[j][i] = matrix[i][j]
    return T

def gram_schmidt(A):
    n = len(A)
    Q = []
    R = [[0] * n for _ in range(n)]
    
    for i in range(n):
        v = A[i]
        for j in range(i):
            r = sum(Q[j][k] * v[k] for k in range(n))
            v = [v[k] - r * Q[j][k] for k in range(n)]
        norm = math.sqrt(sum(v[k]**2 for k in range(n)))
        if norm == 0:
            continue
        Q.append([v[k] / norm for k in range(n)])
        R[i][i] = norm
    
    return Q, R

def minrank(matrix):
    Q, _ = gram_schmidt(matrix)
    rank = sum(1 for row in Q if any(row))
    return rank

def communication_complexity(A):
    n = len(A)
    # Simulate a simple function computed by the matrix
    function_values = [sum(A[i][j] * random.choice([0, 1]) for j in range(n)) % 2 for i in range(n)]
    # Calculate the communication complexity (simulated as the number of non-zero values)
    return sum(1 for value in function_values if value != 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            symplectic_A = matrix_multiplication(A, transpose(A))
            rank = minrank(symplectic_A)
            complexity = communication_complexity(A)
            
            ranks.append(rank)
            complexities.append(complexity)
    
    if not ranks or not complexities:
        return {
            "metric_name": "minrank vs complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_ranks_or_complexities"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_complexity = sum(complexities) / len(complexities)
    correlation_coefficient = (sum((r - mean_rank) * (c - mean_complexity) for r, c in zip(ranks, complexities)) /
                                math.sqrt(sum((r - mean_rank)**2 for r in ranks) *
                                          sum((c - mean_complexity)**2 for c in complexities)))
    
    return {
        "metric_name": "minrank vs complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_metric_value:.4f} std=NOT_COMPUTABLE support_fraction={support_fraction:.2f}")