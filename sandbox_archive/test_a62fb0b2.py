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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def is_connected(graph, n):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph:
                    if neighbor[0] == node and not visited[neighbor[1]]:
                        stack.append(neighbor[1])
                    elif neighbor[1] == node and not visited[neighbor[0]]:
                        stack.append(neighbor[0])
        return all(visited)
    
    def compute_subgroup_order(graph):
        n = len(graph)
        if not is_connected(graph, n):
            return 0
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in graph or (j, i) in graph:
                    order *= 2
        return order
    
    def compute_frege_proof_width(sat_instance):
        # Simplified Frege proof width computation
        # This is a placeholder and should be replaced with actual logic
        return len(sat_instance.split()) * 2
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    subgroup_order = compute_subgroup_order(graph)
    sat_instance = " ".join(f"x{i+1}" for i in range(n))
    frege_width = compute_frege_proof_width(sat_instance)
    
    if frege_width == 0:
        return {
            "metric_name": "Frege Proof Width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "frege_width_zero"
        }
    
    c = math.log2(subgroup_order) / frege_width if frege_width > 0 else float('inf')
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": subgroup_order <= 2**c * frege_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["instances_tested"] > 0) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='subgroup_order_too_large' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")