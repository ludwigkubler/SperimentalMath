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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(m):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def communication_matrix(f, n):
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                x = [int(b) for b in format(i, f'0{n}b')]
                y = [int(b) for b in format(j, f'0{n}b')]
                matrix[i][j] = f(x + y)
        return matrix
    
    def field_rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = lambda x: random.choice([0, 1])
        C = communication_matrix(f, n)
        rank = field_rank(C)
        results.append((n, rank))
    
    if len(results) < 30:
        return {
            "metric_name": "Brauer group rank vs. Communication complexity rank variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    ranks = [rank for _, rank in results]
    variances = [variance([r] * 2**n) for n, r in results]
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(ranks, variances)) / len(ranks)
    mean_rank = sum(ranks) / len(ranks)
    std_dev_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    within_3_std = [r for r in ranks if abs(r - mean_rank) <= 3 * std_dev_rank]
    support_fraction = len(within_3_std) / len(ranks)
    
    return {
        "metric_name": "Brauer group rank vs. Communication complexity rank variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "Not enough data to support the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not enough data to support the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient data")