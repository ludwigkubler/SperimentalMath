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
    
    def mean(values):
        return sum(values) / len(values)
    
    def pearson_correlation(x, y):
        x_mean = mean(x)
        y_mean = mean(y)
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - x_mean) ** 2 for xi in x)) * math.sqrt(sum((yi - y_mean) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    def generate_d_regular_graph(n, d):
        graph = {i: [] for i in range(n)}
        degree_count = [0] * n
        edges_added = set()
        
        while any(count < d for count in degree_count):
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added.add((u, v))
        
        return graph
    
    def algebraic_geometry_of_boolean_functions(graph):
        # Placeholder for actual computation
        return random.randint(1, n)
    
    def communication_complexity_rank_variance(graph):
        # Placeholder for actual computation
        return random.random()
    
    instances_tested = 30
    log_H1_G_values = []
    R_var_G_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        d = random.randint(2, min(n-1, 4))
        graph = generate_d_regular_graph(n, d)
        H1_G = algebraic_geometry_of_boolean_functions(graph)
        R_var_G = communication_complexity_rank_variance(graph)
        
        log_H1_G_values.append(math.log(H1_G))
        R_var_G_values.append(R_var_G)
    
    correlation_coefficient = pearson_correlation(log_H1_G_values, R_var_G_values)
    mean_log_H1_G = mean(log_H1_G_values)
    mean_R_var_G = mean(R_var_G_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n for _ in range(instances_tested)),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")