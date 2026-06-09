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
    
    def generate_communication_complexity_instance(n, r):
        # Generate a random communication complexity instance with rank r
        A = [[random.randint(0, 1) for _ in range(r)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(r)] for _ in range(n)]
        Q = [[sum(a * b for a, b in zip(row_A, row_B)) for row_B in B] for row_A in A]
        return Q
    
    def matrix_rank(matrix):
        # Compute the rank of a matrix using Gaussian elimination
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def communication_complexity_rank_variance(Q):
        # Compute the communication complexity rank variance
        r = matrix_rank(Q)
        n = len(Q)
        return (r / math.log(n)) ** 2
    
    def minimal_rank_of_quadratic_form(matrix):
        # Compute the minimal rank of a quadratic form matrix
        m, n = len(matrix), len(matrix[0])
        min_rank = float('inf')
        for i in range(m):
            row = [matrix[i][j] for j in range(n)]
            if any(row[j] != 0 for j in range(n)):
                min_rank = min(min_rank, matrix_rank([row]))
        return min_rank
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            Q = generate_communication_complexity_instance(n, random.randint(1, n))
            min_rank = minimal_rank_of_quadratic_form(Q)
            r_phi = communication_complexity_rank_variance(Q)
            results.append({
                "n": n,
                "min_rank": min_rank,
                "r_phi": r_phi
            })
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = sum(result["min_rank"] / (math.log(result["n"]) * math.log(result["r_phi"])) for result in results) / len(results)
    conjecture_holds = any(ratio <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else "ratio > 1.5"
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"ratio > 10\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")