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
        graph = {i: set() for i in range(n)}
        colors = [random.randint(0, k-1) for _ in range(n)]
        for u in range(n):
            for v in range(u+1, n):
                if colors[u] != colors[v]:
                    graph[u].add(v)
                    graph[v].add(u)
        return graph
    
    def compute_brauer_classes(graph):
        # Simplified Brauer class computation (not actual Brauer theory)
        return len(graph)  # Placeholder for actual computation
    
    def simulate_communication_rank(graph):
        # Simulate communication rank growth rate
        n = len(graph)
        if n == 1:
            return 0
        return random.randint(1, n-1)  # Placeholder for actual simulation
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_k_colorable_graph(n, k=3)
        br_G = compute_brauer_classes(graph)
        communication_rank = simulate_communication_rank(graph)
        results.append((br_G, communication_rank))
    
    if not results:
        return {
            "metric_name": "Pearson's r-value",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    br_values, communication_rank_values = zip(*results)
    mean_br = sum(br_values) / instances_tested
    mean_communication_rank = sum(communication_rank_values) / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson's r-value",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    # Calculate Pearson's r-value
    covariance = sum((br - mean_br) * (comm - mean_communication_rank) for br, comm in results)
    variance_br = sum((br - mean_br)**2 for br in br_values)
    variance_communication_rank = sum((comm - mean_communication_rank)**2 for comm in communication_rank_values)
    
    if variance_br == 0 or variance_communication_rank == 0:
        return {
            "metric_name": "Pearson's r-value",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    pearsons_r = covariance / (math.sqrt(variance_br) * math.sqrt(variance_communication_rank))
    
    return {
        "metric_name": "Pearson's r-value",
        "metric_value": pearsons_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearsons_r >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in res or res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = sum("conjecture_holds" in res and res["conjecture_holds"] for res in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(res['counterexample'] for res in results if 'counterexample' in res)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")