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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_tensor_representation(f):
        n = int(math.log2(len(f)))
        tensor = [[Fraction(f[i * (1 << j) + k], 2**(n - j)) for k in range(1 << j)] for j in range(n)]
        return tensor
    
    def calculate_geometric_complexity(tensor):
        n = len(tensor)
        rank = 0
        for i in range(n):
            if all(tensor[j][i] == 0 for j in range(n)):
                continue
            rank += 1
        return rank
    
    def calculate_communication_rank(f):
        n = int(math.log2(len(f)))
        # Simplified communication rank calculation (for demonstration purposes)
        return n
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov_xy / (std_dev_x * std_dev_y)
    
    def standard_deviation(values, mean):
        return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        tensor = calculate_tensor_representation(f)
        geometric_complexity = calculate_geometric_complexity(tensor)
        communication_rank = calculate_communication_rank(f)
        
        results.append((geometric_complexity, communication_rank))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "Geometric Complexity vs Communication Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    geometric_complexities, communication_ranks = zip(*results)
    correlation_coefficient = pearson_correlation(geometric_complexities, communication_ranks)
    mean_geometric_complexity = sum(geometric_complexities) / len(geometric_complexities)
    std_deviation = standard_deviation(geometric_complexities, mean_geometric_complexity)
    
    median_geometric_complexity = sorted(geometric_complexities)[len(geometric_complexities) // 2]
    support_fraction = sum(1 for gc in geometric_complexities if gc <= median_geometric_complexity - 3 * std_deviation) / len(geometric_complexities)
    
    return {
        "metric_name": "Geometric Complexity vs Communication Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8 and support_fraction >= 0.8,
        "counterexample": "" if correlation_coefficient > 0.8 and support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: INCONCLUSIVE reason=unknown")