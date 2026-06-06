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

# Helper functions for graph operations
def generate_d_regular_graph(n, d):
    if n * d % 2 != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    for node in range(n):
        for neighbor in range(node + 1, n):
            if len(graph[node]) >= d or len(graph[neighbor]) >= d:
                continue
            if (node, neighbor) not in edges_added and (neighbor, node) not in edges_added:
                graph[node].append(neighbor)
                graph[neighbor].append(node)
                edges_added.add((node, neighbor))
    
    return graph

def dfs(graph, start, parent):
    stack = [start]
    visited = set()
    max_depth = 0
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor != parent:
                    max_depth = max(max_depth, dfs(graph, neighbor, node))
    
    return max_depth + 1

def circuit_monotone_width(graph):
    n = len(graph)
    width = 0
    
    for i in range(n):
        width = max(width, dfs(graph, i, -1))
    
    return width

# Main function to run a trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        width = circuit_monotone_width(graph)
        order = len(graph)  # Simplified order as the number of vertices
        
        results.append({
            "n": n,
            "width": width,
            "order": order
        })
    
    if not results:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_graphs_generated"
        }
    
    total_order = sum(result["order"] for result in results)
    total_width = sum(result["width"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    if instances_tested < 30:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * width for result in results) - 
                               mean_order * total_width - mean_width * total_order) / \
                              math.sqrt((instances_tested * sum(order**2 for result in results) - mean_order**2) *
                                        (instances_tested * sum(width**2 for result in results) - mean_width**2))
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result and result["counterexample"])
        first_failing_seed = next(result["seed"] for result in results if "conjecture_holds" in result and not result["conjecture_holds"])
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")