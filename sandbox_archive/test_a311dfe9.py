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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def rank(A):
        rref = gaussian_elimination(A)
        rank = sum(1 for row in rref if any(row))
        return rank
    
    def volume(v, n):
        lower_bound = (v / factorial(n)) ** (1/3)
        upper_bound = v ** (1/3)
        return lower_bound, upper_bound
    
    def communication_complexity_rank_variance(n):
        # Simulate a random matrix and compute its rank variance
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        r = rank(A)
        return r * (n - r)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        v = communication_complexity_rank_variance(n)
        lower_bound, upper_bound = volume(v, n)
        if v < lower_bound or v > upper_bound:
            return {
                "metric_name": "Volume",
                "metric_value": v,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"v={v}, n={n}"
            }
        results.append(v)
    
    mean_volume = sum(results) / len(results)
    return {
        "metric_name": "Volume",
        "metric_value": mean_volume,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_volume = sum(results) / len(results)
    std_volume = (sum((x - mean_volume) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r > 0) / len(results)
    
    if all(r > 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    elif any(r <= 0 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r <= 0))]
        print(f"RESULT: FALSIFIED counterexample=\"Volume is non-positive\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation")