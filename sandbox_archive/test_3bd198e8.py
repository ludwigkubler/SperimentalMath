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

def generate_binary_matrix(n):
    return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

def matrix_multiplication(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def transpose(matrix):
    n = len(matrix)
    return [[matrix[j][i] for j in range(n)] for i in range(n)]

def gram_schmidt(matrix):
    n = len(matrix)
    Q = []
    R = [[0] * n for _ in range(n)]
    for k in range(n):
        v = [matrix[i][k] for i in range(n)]
        for j in range(k):
            r = sum(Q[j][i] * v[i] for i in range(n))
            for i in range(n):
                v[i] -= r * Q[j][i]
        norm = math.sqrt(sum(v[i]**2 for i in range(n)))
        if norm == 0:
            continue
        Q.append([v[i] / norm for i in range(n)])
        for j in range(k, n):
            R[k][j] = sum(Q[k][i] * matrix[i][j] for i in range(n))
    return Q, R

def minrank(matrix):
    Q, _ = gram_schmidt(matrix)
    rank = 0
    for row in Q:
        if any(row[i] != 0 for i in range(len(row))):
            rank += 1
    return rank

def communication_complexity(matrix):
    n = len(matrix)
    # Simplified model: complexity is proportional to the number of non-zero entries
    return sum(sum(1 for x in row if x == 1) for row in matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            A = generate_binary_matrix(n)
            symplectic_A = matrix_multiplication(A, transpose(A))
            rank = minrank(symplectic_A)
            complexity = communication_complexity(A)
            results.append((n, rank, complexity))
    
    if len(results) < 30:
        return {
            "metric_name": "minrank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks = [rank for _, rank, _ in results]
    complexities = [complexity for _, _, complexity in results]
    mean_rank = sum(ranks) / len(ranks)
    mean_complexity = sum(complexities) / len(complexities)
    
    correlation_coefficient = 0
    n = len(results)
    if n > 1:
        numerator = sum((ranks[i] - mean_rank) * (complexities[i] - mean_complexity) for i in range(n))
        denominator = math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(n))) * math.sqrt(sum((complexities[i] - mean_complexity)**2 for i in range(n)))
        correlation_coefficient = numerator / denominator
    
    p_value = 0.05  # Placeholder, actual calculation would be complex
    if correlation_coefficient > 0.9 and p_value < 0.05:
        return {
            "metric_name": "minrank",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minrank",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "correlation_threshold_not_met"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break