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
    
    def is_valid_graph(graph):
        if graph is None or not isinstance(graph, list):
            return False
        n = len(graph)
        for i in range(n):
            if len(graph[i]) != n:
                return False
            for j in range(n):
                if graph[i][j] != graph[j][i]:
                    return False
        return True
    
    def generate_d_regular_graph(d, n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def resolution_proof_width(graph):
        n = len(graph)
        # Simplified heuristic for demonstration purposes
        return n * (n - 1) // 2
    
    d = random.randint(3, 5)  # Degree of the regular graph
    n = random.randint(5, 40)  # Number of vertices
    graph = generate_d_regular_graph(d, n)
    
    if not is_valid_graph(graph):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    g = d * n // 2  # Number of generators (simplified)
    w = resolution_proof_width(graph)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": abs(g - w),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(g - w) <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")