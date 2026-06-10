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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        cc = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    cc += 1
        return cc
    
    def noncommutative_algebra_rank(f):
        n = len(f)
        A_f = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    A_f[i][j] = 1
        rank = 0
        for row in A_f:
            if any(row):
                rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i+1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def minrank(A_f):
        return gaussian_elimination(A_f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        rank = minrank(A_f)
        if rank is None:
            return {
                "metric_name": "minrank/CC ratio",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Gaussian elimination failed"
            }
        results.append(rank / cc)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.95 <= abs(r - mean) / std <= 1.05) / len(results)
    
    return {
        "metric_name": "minrank/CC ratio",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Non-linear relationship found with ratio {mean} ± {std}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.95 <= abs(r - mean) / std <= 1.05) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-linear relationship found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")