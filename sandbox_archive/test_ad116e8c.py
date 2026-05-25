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
        if matrix[i][i] == 0:
            # Swap with a row below that has a non-zero element in the same column
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate all other elements below the pivot
        for j in range(i + 1, n):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def generate_matrix_product_state(depth):
    n = 2 ** depth
    state = [[0] * n for _ in range(n)]
    state[0][0] = 1
    for i in range(1, depth + 1):
        new_state = [[0] * n for _ in range(n)]
        for j in range(n // 2):
            new_state[j][j] = 1
            new_state[j + n // 2][j + n // 2] = 1
        state = [[state[i][k] * new_state[k][j] for k in range(n)] for i in range(n)]
    return state

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    depth = random.randint(5, 40)
    matrix_product_state = generate_matrix_product_state(depth)
    
    try:
        kahler_rank = rank(matrix_product_state)
        communication_complexity_depth = depth
        metric_value = abs(kahler_rank - communication_complexity_depth)
        
        conjecture_holds = kahler_rank >= communication_complexity_depth
        counterexample = "" if conjecture_holds else f"Depth={depth}, Kähler Rank={kahler_rank}"
    except Exception as e:
        print(f"Error in run_trial with seed {seed}: {e}")
        return {
            "metric_name": "rank_diff",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "metric_name": "rank_diff",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_diff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        result = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    
    print(result)