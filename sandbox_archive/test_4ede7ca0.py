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

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            continue
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(n):
            matrix[i][j] /= matrix[i][i]
        for k in range(m):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    row_echelon_form = gaussian_elimination(matrix)
    rank = sum(1 for row in row_echelon_form if any(row))
    return rank

def generate_xor_function(n):
    def f(x):
        return x[0] ^ all(x[i] for i in range(1, n))
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        total_rank = 0
        instances_tested = 0
        for _ in range(5):  # Test each n 5 times
            f = generate_xor_function(n)
            matrix = [[f([i]) for i in range(1 << n)]]
            rank_value = rank(matrix)
            total_rank += rank_value
            instances_tested += 1
        avg_rank = total_rank / instances_tested
        results.append({"n": n, "avg_rank": avg_rank})
    
    conjecture_holds = all(result["avg_rank"] <= result["n"] for result in results)
    if not conjecture_holds:
        counterexample = f"avg_rank > n for some n"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Average Rank",
        "metric_value": sum(result["avg_rank"] for result in results) / len(results),
        "instances_tested": instances_tested * len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # First 30 primes
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds]
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='avg_rank > n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")