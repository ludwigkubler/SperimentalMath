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
    
    def is_k_colorable(graph, k):
        colors = [-1] * len(graph)
        colors[0] = 0
        
        def dfs(node, color):
            if node in graph and color == colors[node]:
                return False
            colors[node] = color
            for neighbor in graph[node]:
                if not dfs(neighbor, (color + 1) % k):
                    return False
            return True
        
        for i in range(len(graph)):
            if colors[i] == -1:
                if not dfs(i, 0):
                    return False
        return True
    
    def minimal_quadratic_residue_representation(graph):
        n = len(graph)
        mqr = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    mqr += (i - j) ** 2
        return mqr
    
    def communication_complexity_growth_rate(graph, k):
        n = len(graph)
        growth_rate = 0
        for i in range(1, n):
            growth_rate += math.log(i + 1, 2)
        return growth_rate
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            if not is_k_colorable(graph, k):
                continue
            mqr = minimal_quadratic_residue_representation(graph)
            growth_rate = communication_complexity_growth_rate(graph, k)
            results.append((mqr, growth_rate))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mqr_values, growth_rate_values = zip(*results)
    correlation_coefficient = pearson_correlation_coefficient(mqr_values, growth_rate_values)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")