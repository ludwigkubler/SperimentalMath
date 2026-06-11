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
            # Find pivot row
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            # Eliminate column elements below the pivot
            for j in range(i + 1, n):
                factor = -matrix[j][i] / pivot
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def communication_complexity_rank_variance(boolean_function):
        n = len(boolean_function)
        vector_space = [[0 if boolean_function(i, j) else 1 for j in range(n)] for i in range(n)]
        A = gaussian_elimination(vector_space)
        rank = sum(1 for row in A if any(row))
        return (n - rank) / n
    
    def random_boolean_function(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(5):
            boolean_function = random_boolean_function(n)
            rank_var = communication_complexity_rank_variance(boolean_function)
            index_tgb = len([row for row in gaussian_elimination(vector_space) if any(row)])
            results.append({
                "n": n,
                "rank_var": rank_var,
                "index_tgb": index_tgb
            })
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    metric_values = [result["rank_var"] * result["index_tgb"] for result in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_metric_value,
        "instances_tested": total_instances,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")