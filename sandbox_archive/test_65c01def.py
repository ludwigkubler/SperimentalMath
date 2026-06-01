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

def generate_k_colorable_graph(n, k):
    if n <= 0 or k <= 1:
        return None
    
    graph = [[None for _ in range(n)] for _ in range(n)]
    available_colors = set(range(1, k + 1))
    
    def is_valid_color(i, j, color):
        for x in range(n):
            if graph[i][x] == color or (graph[x][i] is not None and graph[x][i] == color):
                return False
        return True
    
    def backtrack(i):
        if i == n:
            return True
        
        available_colors.discard(graph[i-1][i-1])
        
        for color in available_colors:
            if is_valid_color(i, i-1, color):
                graph[i][i-1] = color
                graph[i-1][i] = color
                if backtrack(i + 1):
                    return True
        
        available_colors.add(graph[i-1][i-1])
        return False
    
    if not backtrack(0):
        return None
    
    return graph

def compute_p_adic_l_function_rank(graph):
    n = len(graph)
    lrank = 0
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] is not None:
                lrank += 1
    return lrank

def compute_communication_rank_growth_rate(graph):
    n = len(graph)
    communication_rank = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] is not None:
                communication_rank[i] += 1
                communication_rank[j] += 1
    
    max_communication_rank = max(communication_rank)
    return max_communication_rank / (n * (n - 1) // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    k = 3
    instances_tested = 0
    lrank_values = []
    crg_rate_values = []
    
    for _ in range(30):
        graph = generate_k_colorable_graph(n_max, k)
        if graph is None:
            continue
        
        lrank = compute_p_adic_l_function_rank(graph)
        crg_rate = compute_communication_rank_growth_rate(graph)
        
        lrank_values.append(lrank)
        crg_rate_values.append(crg_rate)
        instances_tested += 1
    
    if not lrank_values or not crg_rate_values:
        return {
            "metric_name": "lrank vs crg_rate",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_lrank = sum(lrank_values) / len(lrank_values)
    std_lrank = math.sqrt(sum((x - mean_lrank) ** 2 for x in lrank_values) / len(lrank_values))
    correlation_coefficient = sum((lrank_values[i] - mean_lrank) * (crg_rate_values[i] - crg_rate_values[0]) for i in range(len(lrank_values))) / (len(lrank_values) * std_lrank * math.sqrt(sum((x - crg_rate_values[0]) ** 2 for x in crg_rate_values)))
    
    return {
        "metric_name": "lrank vs crg_rate",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_lrank <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        counterexample = "lrank vs crg_rate"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")