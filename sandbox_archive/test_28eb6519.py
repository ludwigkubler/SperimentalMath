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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_convolution_matrix(f):
        n = len(f)
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                M[i][j] = sum(f[k] * f[i ^ j ^ k] for k in range(n))
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            for j in range(pivot_row, n):
                if matrix[j][i] != 0:
                    break
            else:
                continue
            matrix[pivot_row], matrix[j] = matrix[j], matrix[pivot_row]
            for j in range(n):
                if j == pivot_row:
                    continue
                factor = matrix[j][i] / matrix[pivot_row][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[pivot_row][k]
            rank += 1
        return rank
    
    def bp_readtwice_width(f):
        n = len(f)
        width = 0
        for i in range(2**n):
            if f[i] == 1:
                width = max(width, bin(i).count('1'))
        return width
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            M = free_convolution_matrix(f)
            rank = min_rank(M)
            if rank < 0.9 * n**0.5 or rank > 1.1 * n**0.5:
                return {
                    "metric_name": "Free Convolution Rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank}"
                }
            results.append(rank)
    
    bp_rank = min_rank(free_convolution_matrix([0] * (2**40)))
    if bp_rank > 2:
        return {
            "metric_name": "BP ReadTwice Width",
            "metric_value": bp_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"BP Rank={bp_rank}"
        }
    
    return {
        "metric_name": "Free Convolution Rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 200, 7))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.9 * n**0.5 and r <= 1.1 * n**0.5) / len(results)
    
    if all(r >= 0.9 * n**0.5 and r <= 1.1 * n**0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not (0.9 * n**0.5 <= r <= 1.1 * n**0.5))]
        print(f"RESULT: FALSIFIED counterexample='n={n}, rank={r}' first_failing_seed={first_failing_seed}")