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
    
    def characteristic_polynomial(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        return matrix
    
    def grothendieck_witt_class(matrix, mod=2):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(n):
                if i == j:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def communication_complexity_rank_variance(matrix, mod=2):
        n = len(matrix)
        ranks = []
        for i in range(1 << n):
            submatrix = [[matrix[j][k] & (i >> j) & (i >> k) for k in range(n)] for j in range(n)]
            rank = 0
            for j in range(n):
                if all(submatrix[j][k] == 0 for k in range(j, n)):
                    continue
                pivot_row = next(k for k in range(j, n) if submatrix[k][j] != 0)
                submatrix[j], submatrix[pivot_row] = submatrix[pivot_row], submatrix[j]
                rank += 1
            ranks.append(rank)
        return max(ranks) - min(ranks)
    
    def log_gw_class(matrix, mod=2):
        gw_class = grothendieck_witt_class(matrix, mod)
        if gw_class == 0:
            return 0
        return math.log(gw_class, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_rank_diffs = []
    log_gw_classes = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        char_poly = characteristic_polynomial(f)
        gw_class = log_gw_class(char_poly)
        rank_variance = communication_complexity_rank_variance(char_poly)
        
        if gw_class == 0:
            continue
        
        max_rank_diffs.append(rank_variance)
        log_gw_classes.append(gw_class)
    
    if not max_rank_diffs or not log_gw_classes:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank_diff = sum(max_rank_diffs) / len(max_rank_diffs)
    mean_gw_class = sum(log_gw_classes) / len(log_gw_classes)
    std_rank_diff = math.sqrt(sum((x - mean_rank_diff) ** 2 for x in max_rank_diffs) / len(max_rank_diffs))
    
    correlation_coefficient = sum((x - mean_rank_diff) * (y - mean_gw_class) for x, y in zip(max_rank_diffs, log_gw_classes)) / (len(max_rank_diffs) * std_rank_diff * math.sqrt(sum((y - mean_gw_class) ** 2 for y in log_gw_classes)))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_rank_diff,
        "instances_tested": len(max_rank_diffs),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")