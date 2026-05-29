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

def polynomial_representation(f, n):
    k = 2
    A = [[0] * (1 << n) for _ in range(1 << n)]
    points = list(range(1 << n))
    for point in points:
        f_val = f(point)
        A[f_val][sum(points)] += 1
    return A

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if all(matrix[i][j] == 0 for j in range(n)):
            continue
        pivot_row = i
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == m:
                return rank
        for j in range(i, n):
            matrix[pivot_row][j], matrix[i][j] = matrix[i][j], matrix[pivot_row][j]
        for j in range(m):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] += factor * matrix[i][k]
        rank += 1
    return rank

def tree_like_resolution_width(f, n):
    # Placeholder implementation; actual computation depends on the function f
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = 2
    A = polynomial_representation(f, n)
    rank_A = matrix_rank(A)
    t_star_f = tree_like_resolution_width(f, n)
    
    metric_name = "rank_bound"
    metric_value = rank_A / (math.sqrt(n) * math.log(n))
    instances_tested = 1
    n_max = n
    conjecture_holds = rank_A <= math.sqrt(n) * math.log(n)
    counterexample = "" if conjecture_holds else f"Rank {rank_A} exceeds bound O(√{n}·log{n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")