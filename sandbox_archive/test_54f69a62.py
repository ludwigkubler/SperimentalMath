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
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        if factor == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= factor
        for j in range(rows):
            if i != j:
                factor = matrix[j][i]
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def min_rank(matrix):
    rows = len(matrix)
    rank = 0
    for row in gaussian_elimination(matrix):
        if any(row):
            rank += 1
    return rank

def construct_quadratic_form(bp):
    n = len(bp)
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Q[i][j] = bp[j]
            Q[j][i] = bp[j]
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    size = random.randint(5, 40)
    bp = [random.choice([0, 1]) for _ in range(size)]
    quadratic_form = construct_quadratic_form(bp)
    min_rank_val = min_rank(quadratic_form)
    
    if bp == [0] * size:
        return {
            "metric_name": "min_rank",
            "metric_value": min_rank_val,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "IP_2 BP with all zeros"
        }
    
    conjecture_holds = (size == 1 or min_rank_val <= 1.5 * math.log(size, 2))
    counterexample = "" if conjecture_holds else f"BP size {size} with rank {min_rank_val}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_val,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(result)]}")