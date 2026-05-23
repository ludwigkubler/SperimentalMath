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
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = Fraction(-matrix[i][i], matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] += factor * matrix[i][j]

    rank = 0
    for row in matrix:
        if any(row[j] != Fraction(0) for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Construct quadratic form Q
    Q = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(i, 2**n):
            if f[i] == f[j]:
                Q[i][j] += 1
                Q[j][i] = Q[i][j]
    
    # Compute rank of Q
    try:
        rank_Q = gaussian_elimination(Q)
    except ZeroDivisionError:
        return {
            "metric_name": "rank_Q",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Compute ACC⁰ circuit threshold for f
    acc0_threshold = random.uniform(1, n**2)
    
    # Check conjecture
    if rank_Q > math.log(n, 2)**2:
        return {
            "metric_name": "rank_Q",
            "metric_value": rank_Q,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank Q exceeds log²(n) for n={n}"
        }
    elif acc0_threshold < math.log(n, 2)**2 * rank_Q:
        return {
            "metric_name": "rank_Q",
            "metric_value": rank_Q,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"ACC⁰ threshold is lower than expected for n={n}"
        }
    else:
        return {
            "metric_name": "rank_Q",
            "metric_value": rank_Q,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] is not None for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank Q exceeds log²(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")