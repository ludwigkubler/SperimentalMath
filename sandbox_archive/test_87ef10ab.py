# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_complexity_instance(rank):
        # Placeholder for generating an instance of communication complexity problem with given rank
        return [random.randint(0, 1) for _ in range(2**rank)]
    
    def construct_graph(instance):
        # Placeholder for constructing the graph from the instance
        n = len(instance)
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if instance[i] != instance[j]:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def compute_minimal_order_of_affine_divisor(graph):
        # Placeholder for computing the minimal order of an affine divisor
        n = len(graph)
        min_order = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] == 1:
                    min_order = min(min_order, abs(j - i))
        return min_order
    
    rank_max = 10
    results = []
    
    for r in range(5, rank_max + 1, 5):
        instance = generate_communication_complexity_instance(r)
        graph = construct_graph(instance)
        min_order = compute_minimal_order_of_affine_divisor(graph)
        
        results.append({
            "rank": r,
            "min_order": min_order
        })
    
    if not results:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 10,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [result["min_order"] for result in results]
    ranks = [result["rank"] for result in results]
    
    # Pearson correlation coefficient
    n = len(min_orders)
    mean_min_order = sum(min_orders) / n
    mean_rank = sum(ranks) / n
    numerator = sum((min_orders[i] - mean_min_order) * (ranks[i] - mean_rank) for i in range(n))
    denominator = sum((min_orders[i] - mean_min_order)**2 for i in range(n)) ** 0.5 * sum((ranks[i] - mean_rank)**2 for i in range(n)) ** 0.5
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "minimal_order",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": rank_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,  # Arbitrary threshold for support
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")