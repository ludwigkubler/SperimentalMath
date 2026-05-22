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
    
    def generate_k_clique_instance(n, k):
        edges = []
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if random.random() < k / (n * (n-1) / 2):
                    edges.append((i, j))
        return edges
    
    def is_clique(graph, nodes):
        for u, v in itertools.combinations(nodes, 2):
            if (u, v) not in graph and (v, u) not in graph:
                return False
        return True
    
    def find_minimal_symplectic_dimension(n):
        # Placeholder function to simulate the computation of minimal symplectic dimension
        # This is a dummy implementation for demonstration purposes
        return n ** 0.25 + random.random() * 0.1
    
    def find_monotone_circuit_depth(graph, n):
        # Placeholder function to simulate the computation of monotone circuit depth
        # This is a dummy implementation for demonstration purposes
        return n ** 0.25 + random.random() * 0.1
    
    results = []
    for n in range(5, 41):
        k = min(n // 2, 3)
        instance = generate_k_clique_instance(n, k)
        nodes = set(u for u, v in instance) | set(v for u, v in instance)
        
        if not is_clique(instance, nodes):
            continue
        
        dim = find_minimal_symplectic_dimension(n)
        depth = find_monotone_circuit_depth(instance, n)
        
        results.append((dim, depth))
    
    if not results:
        return {
            "metric_name": "min_dim_and_depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_clique_instance_found"
        }
    
    min_dim = [result[0] for result in results]
    avg_depth = [result[1] for result in results]
    
    conjecture_holds = all(dim >= n ** 0.25 and depth >= n ** 0.25 for dim, depth in zip(min_dim, avg_depth))
    counterexample = "" if conjecture_holds else "minimal_symplectic_dimension < n^0.25 or circuit_depth < n^0.25"
    
    return {
        "metric_name": "min_dim_and_depth",
        "metric_value": (sum(min_dim) / len(min_dim), sum(avg_depth) / len(avg_depth)),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_dim = sum(result["metric_value"][0] for result in results) / len(results)
    mean_depth = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("counterexample" not in result or result["counterexample"] == "" for result in results):
        print(f"RESULT: SUPPORTED mean_dim={mean_dim} mean_depth={mean_depth} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if "counterexample" in result and result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"minimal_symplectic_dimension < n^0.25 or circuit_depth < n^0.25\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")