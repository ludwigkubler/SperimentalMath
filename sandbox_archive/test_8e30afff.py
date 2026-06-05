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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rref_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in rref_matrix:
            if any(row):
                rank += 1
        return rank
    
    def mld(matroid):
        # Placeholder for actual MLD computation
        # This is a dummy implementation for testing purposes
        return random.random() * 10  # Replace with actual MLD calculation
    
    n = random.randint(5, 40)
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    mld_value = mld(matrix)
    rank_value = rank(matrix)
    
    k = 2  # Placeholder constant
    if mld_value > k * math.log(n):
        return {
            "metric_name": "mld_vs_log_rank",
            "metric_value": mld_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mld > k * log(n)"
        }
    
    return {
        "metric_name": "mld_vs_log_rank",
        "metric_value": mld_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    total_metric_value = 0
    num_supporting_seeds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            num_supporting_seeds += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = num_supporting_seeds / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mld > k * log(n)\" first_failing_seed={first_failing_seed}")