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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def smith_normal_form(matrix):
    m, n = len(matrix), len(matrix[0])
    r, c = 0, 0
    while r < m and c < n:
        pivot_row = r
        for i in range(r + 1, m):
            if abs(matrix[i][c]) > abs(matrix[pivot_row][c]):
                pivot_row = i
        matrix[r], matrix[pivot_row] = matrix[pivot_row], matrix[r]
        if matrix[r][c] == 0:
            c += 1
            continue
        for i in range(r + 1, m):
            factor = -matrix[i][c] // matrix[r][c]
            for j in range(c, n):
                matrix[i][j] += factor * matrix[r][j]
        r += 1
        c += 1
    return matrix

def min_rank(matrix):
    snf = smith_normal_form(matrix)
    rank = sum(1 for row in snf if any(row[j] != 0 for j in range(len(row))))
    return rank

def generate_disjointness_instance(n):
    inputs = [random.choice([0, 1]) for _ in range(n)]
    outputs = [inputs[i] ^ inputs[j] for i in range(n) for j in range(i + 1, n)]
    truth_table = [[inputs[i], outputs[(i * (n - 1)) // 2 + j]] for i in range(n) for j in range((n - 1) // 2 + 1)]
    return truth_table

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 30
        total_rank = 0
        
        for _ in range(instances_tested):
            truth_table = generate_disjointness_instance(n)
            rank = min_rank(truth_table)
            total_rank += rank
            if rank < n * math.log2(n):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank} < {n * math.log2(n)}"
                }
        
        avg_rank = total_rank / instances_tested
        results.append(avg_rank)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = all(rank >= n * math.log2(n) for rank in results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={len(results)}, rank<{math.log2(len(results))}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")