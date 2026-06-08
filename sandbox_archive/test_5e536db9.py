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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def factorial(n):
        result = 1
        for i in range(2, n+1):
            result *= i
        return result
    
    def kahler_manifold_volume(v, n):
        lower_bound = (v / factorial(n)) ** (1/3)
        upper_bound = v ** (1/3)
        return lower_bound, upper_bound
    
    n_bits = random.randint(5, 30)
    n = 2 ** n_bits
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    rank_variance = matrix_rank(A)
    
    lower_bound, upper_bound = kahler_manifold_volume(rank_variance, n_bits)
    
    if not (lower_bound <= rank_variance <= upper_bound):
        return {
            "metric_name": "Kähler Manifold Volume",
            "metric_value": rank_variance,
            "instances_tested": 1,
            "n_max": n_bits,
            "conjecture_holds": False,
            "counterexample": f"Rank variance {rank_variance} out of bounds [{lower_bound}, {upper_bound}]"
        }
    
    return {
        "metric_name": "Kähler Manifold Volume",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n_bits,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank variance out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")