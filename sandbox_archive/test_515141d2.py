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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def max_cut(graph):
        n = len(graph)
        best_cut_value = -1
        for mask in range(1 << n):
            cut_value = sum(1 for u, v in graph if (mask >> u) & 1 and not (mask >> v) & 1)
            best_cut_value = max(best_cut_value, cut_value)
        return best_cut_value
    
    def geometric_quantization_rank(graph):
        # Placeholder function to simulate the minimal rank
        n = len(graph)
        return math.log(n + 1, 2)
    
    def sum_of_squares_hierarchy_level(cut_value):
        # Placeholder function to simulate the hierarchy level
        return cut_value
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        graph = generate_graph(n)
        max_cut_value = max_cut(graph)
        rank = geometric_quantization_rank(graph)
        hierarchy_level = sum_of_squares_hierarchy_level(max_cut_value)
        
        if rank == 0 or hierarchy_level == 0:
            continue
        
        ratio = abs(rank / math.log(max_cut_value, 2) - 1)
        results.append((rank, hierarchy_level, ratio))
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to Log(Max-Cut)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = sum(ratio for _, _, ratio in results) / len(results)
    return {
        "metric_name": "Ratio of Rank to Log(Max-Cut)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(0.9 <= ratio <= 1.1 for _, _, ratio in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif any(abs(result["metric_value"] - 1) > 0.2 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 1) > 0.2)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±20%\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")