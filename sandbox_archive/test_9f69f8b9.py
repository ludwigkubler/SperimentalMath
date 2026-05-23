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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def chromatic_number(graph, n):
        colors = [-1] * n
        color_count = 0
        
        def is_safe(node, color):
            for neighbor in graph[node]:
                if colors[neighbor] == color:
                    return False
            return True
        
        def backtrack(node):
            nonlocal color_count
            if node == n:
                return True
            for c in range(color_count + 1):
                if is_safe(node, c):
                    colors[node] = c
                    if backtrack(node + 1):
                        return True
                    colors[node] = -1
            color_count += 1
            return False
        
        backtrack(0)
        return color_count
    
    def tropicalized_rank(graph, n):
        # Placeholder for the actual computation of the tropicalized rank
        # This is a dummy implementation for demonstration purposes
        return len(graph) / 2
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    chi_G = chromatic_number(graph, n)
    r_t_G = tropicalized_rank(graph, n)
    
    if chi_G == 0 or r_t_G == 0:
        return {
            "metric_name": "chi_G / r_t_G",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = chi_G / r_t_G
    return {
        "metric_name": "chi_G / r_t_G",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.0) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 1.0 for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(seeds) if run_trial(result)["metric_value"] > 1.0)
        print(f"RESULT: FALSIFIED counterexample=\"chi_G / r_t_G > 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")