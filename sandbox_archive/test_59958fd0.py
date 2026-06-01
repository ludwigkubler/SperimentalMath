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
    
    def generate_k_colorable_graph(n, k):
        if n <= 1 or k < 2:
            return []
        
        graph = [[] for _ in range(n)]
        colors = list(range(1, k + 1))
        color_count = [0] * (k + 1)
        
        for i in range(n):
            available_colors = [c for c in colors if color_count[c] < n // k]
            if not available_colors:
                break
            color = random.choice(available_colors)
            graph[i].append(color)
            color_count[color] += 1
        
        return graph
    
    def compute_brauer_classes(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Construct the field over finite fields
        field_size = n + 1
        field_elements = [i for i in range(field_size)]
        
        # Compute Brauer classes (simplified example)
        brauer_classes = set()
        for node in graph:
            if node:
                color = node[0]
                brauer_classes.add((color, node))
        
        return len(brauer_classes)
    
    def compute_communication_rank(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Simulate distributed algorithms (simplified example)
        communication_rank = sum(len(node) for node in graph) / n
        return communication_rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_k_colorable_graph(n, k=3)
        if not graph:
            continue
        
        br_value = compute_brauer_classes(graph)
        comm_rank = compute_communication_rank(graph)
        
        results.append({
            "n": n,
            "br_value": br_value,
            "comm_rank": comm_rank
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson's r-value",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    br_values = [result["br_value"] for result in results]
    comm_ranks = [result["comm_rank"] for result in results]
    
    mean_br = sum(br_values) / len(br_values)
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    
    covariance = sum((br - mean_br) * (comm - mean_comm_rank) for br, comm in zip(br_values, comm_ranks))
    variance_br = sum((br - mean_br) ** 2 for br in br_values)
    variance_comm_rank = sum((comm - mean_comm_rank) ** 2 for comm in comm_ranks)
    
    if variance_br == 0 or variance_comm_rank == 0:
        return {
            "metric_name": "Pearson's r-value",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_variance"
        }
    
    pearsons_r = covariance / (math.sqrt(variance_br) * math.sqrt(variance_comm_rank))
    
    return {
        "metric_name": "Pearson's r-value",
        "metric_value": pearsons_r,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(pearsons_r) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")