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
    
    def generate_tensor(n):
        tensor = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
        return tensor
    
    def calculate_geometric_complexity(tensor):
        n = len(tensor)
        rank = sum(sum(row) for row in tensor) / n
        return rank
    
    def calculate_communication_rank(tensor):
        # Simplified communication rank calculation (for demonstration purposes)
        return len(tensor)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    def median(lst):
        lst.sort()
        n = len(lst)
        if n % 2 == 1:
            return lst[n // 2]
        else:
            return (lst[n // 2 - 1] + lst[n // 2]) / 2
    
    def std_deviation(lst, mean):
        return math.sqrt(sum((x - mean)**2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_geometric_complexity = 0
    communication_ranks = []
    geometric_complexities = []
    
    for n in n_values:
        for _ in range(5):
            tensor = generate_tensor(n)
            geometric_complexity = calculate_geometric_complexity(tensor)
            communication_rank = calculate_communication_rank(tensor)
            
            instances_tested += 1
            total_geometric_complexity += geometric_complexity
            communication_ranks.append(communication_rank)
            geometric_complexities.append(geometric_complexity)
    
    mean_geometric_complexity = total_geometric_complexity / instances_tested
    median_geometric_complexity = median(geometric_complexities)
    std_deviation_geometric_complexity = std_deviation(geometric_complexities, mean_geometric_complexity)
    
    correlation_coefficient = pearson_correlation(communication_ranks, geometric_complexities)
    conjecture_holds = correlation_coefficient > 0.8 and max(geometric_complexities) <= median_geometric_complexity + 3 * std_deviation_geometric_complexity
    
    return {
        "metric_name": "Geometric Complexity",
        "metric_value": mean_geometric_complexity,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")