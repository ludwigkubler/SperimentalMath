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
    
    def generate_planar_graph(n):
        if n == 3:
            return {(0, 1), (1, 2), (2, 0)}
        elif n == 4:
            return {(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)}
        else:
            return None
    
    def geometric_entropy(graph):
        if not graph:
            return 0.0
        degree_sum = sum(len(neighbors) for neighbors in graph.values())
        n = len(graph)
        entropy = -sum(Fraction(degree, 2 * n) * math.log2(Fraction(degree, 2 * n)) for degree in degree_sum)
        return entropy
    
    def communication_rank(graph):
        if not graph:
            return 0
        rank = 0
        visited = set()
        queue = list(graph.keys())
        
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                rank += 1
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_planar_graph(n)
        if not graph:
            continue
        
        entropy = geometric_entropy(graph)
        rank = communication_rank(graph)
        
        if entropy < 0.1 or entropy > 10 or rank < 0.1 or rank > 10:
            return {
                "metric_name": "geometric_entropy",
                "metric_value": entropy,
                "instances_tested": n_values.count(n),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Invalid values: entropy={entropy}, rank={rank}"
            }
        
        results.append((entropy, rank))
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    n = len(results)
    mean_entropy = sum(result[0] for result in results) / n
    mean_rank = sum(result[1] for result in results) / n
    
    if n < 30:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Insufficient instances tested: {n}"
        }
    
    variance_entropy = sum((result[0] - mean_entropy) ** 2 for result in results) / n
    variance_rank = sum((result[1] - mean_rank) ** 2 for result in results) / n
    
    std_dev_entropy = math.sqrt(variance_entropy)
    std_dev_rank = math.sqrt(variance_rank)
    
    correlation_coefficient = (sum((results[i][0] - mean_entropy) * (results[i][1] - mean_rank) for i in range(n)) / n) / (std_dev_entropy * std_dev_rank)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 * std_dev_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")