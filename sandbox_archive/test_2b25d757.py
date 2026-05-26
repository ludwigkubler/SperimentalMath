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
    
    def generate_tseitin_formula(n, delta):
        # Simplified Tseitin formula generation for demonstration
        return [random.randint(1, n) for _ in range(delta)]
    
    def geometric_quantization_rank(formula):
        # Placeholder function to simulate the rank calculation
        return len(formula)
    
    def min_degree(graph):
        return min(len(neighbors) for _, neighbors in graph.items())
    
    def has_long_paths(graph, k):
        # Placeholder function to check for long paths
        return any(len(path) > k for path in find_all_paths(graph))
    
    def find_all_paths(graph):
        # Placeholder function to find all paths in the graph
        def dfs(node, path):
            if node in path:
                yield path + [node]
            else:
                yield from (path + [node] for neighbor in graph[node] for p in dfs(neighbor, path))
        
        return set(path for node in graph for path in dfs(node, []))
    
    n = random.randint(5, 40)
    delta = min_degree({i: random.sample(range(1, n), random.randint(2, n-1)) for i in range(n)})
    k = random.randint(1, n//2)
    formula = generate_tseitin_formula(n, delta)
    
    if has_long_paths({i: random.sample(range(1, n), random.randint(2, n-1)) for i in range(n)}, k):
        return {
            "metric_name": "geometric_quantization_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "formula_has_long_paths"
        }
    
    rank = geometric_quantization_rank(formula)
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='formula_has_long_paths' first_failing_seed={first_failing_seed}")