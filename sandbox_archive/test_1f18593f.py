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
    
    def generate_tensor_representation(n):
        # Placeholder for tensor generation logic
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def calculate_geometric_complexity(tensor):
        n = len(tensor)
        # Placeholder for geometric complexity calculation logic
        return sum(sum(row) for row in tensor)
    
    def calculate_communication_rank(tensor):
        n = len(tensor)
        # Placeholder for communication rank calculation logic
        return random.randint(1, n)
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    def median(lst):
        n = len(lst)
        sorted_lst = sorted(lst)
        if n % 2 == 1:
            return sorted_lst[n // 2]
        else:
            return (sorted_lst[n // 2 - 1] + sorted_lst[n // 2]) / 2
    
    def standard_deviation(lst, mean):
        return math.sqrt(sum((x - mean) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    geometric_complexities = []
    communication_ranks = []
    
    for n in n_values:
        tensor = generate_tensor_representation(n)
        geometric_complexity = calculate_geometric_complexity(tensor)
        communication_rank = calculate_communication_rank(tensor)
        
        geometric_complexities.append(geometric_complexity)
        communication_ranks.append(communication_rank)
    
    correlation_coefficient = pearson_correlation(geometric_complexities, communication_ranks)
    mean_geometric_complexity = sum(geometric_complexities) / len(geometric_complexities)
    median_geometric_complexity = median(geometric_complexities)
    std_deviation = standard_deviation(geometric_complexities, mean_geometric_complexity)
    
    conjecture_holds = correlation_coefficient > 0.8 and all(
        geometric_complexity <= median_geometric_complexity + 3 * std_deviation
        for geometric_complexity in geometric_complexities
    )
    
    return {
        "metric_name": "Geometric Complexity vs Communication Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(geometric_complexities),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = standard_deviation([res["metric_value"] for res in results], mean_metric_value)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")