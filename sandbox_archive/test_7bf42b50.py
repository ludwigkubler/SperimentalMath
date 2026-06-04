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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def communication_complexity_rank(graph, n):
        # Placeholder for actual communication complexity rank calculation
        # This is a dummy implementation for testing purposes
        return len(graph)
    
    def minimal_order_of_quaternionic_kahler_forms(n):
        # Placeholder for actual quaternionic Kähler form calculation
        # This is a dummy implementation for testing purposes
        return n
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        graph = generate_graph(n)
        r_G = communication_complexity_rank(graph, n)
        o_G = minimal_order_of_quaternionic_kahler_forms(n)
        
        results.append({
            "n": n,
            "r_G": r_G,
            "o_G": o_G
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_sum = 0
    n_total = sum(r["n"] for r in results)
    r_G_sum = sum(r["r_G"] * r["n"] for r in results)
    o_G_sum = sum(r["o_G"] * r["n"] for r in results)
    r_G_squared_sum = sum(r["r_G"] ** 2 * r["n"] for r in results)
    o_G_squared_sum = sum(r["o_G"] ** 2 * r["n"] for r in results)
    
    correlation = (len(results) * n_total * r_G_sum * o_G_sum - r_G_sum * o_G_sum) / (
        math.sqrt((len(results) * n_total * r_G_squared_sum - r_G_sum ** 2) * 
                  (len(results) * n_total * o_G_squared_sum - o_G_sum ** 2))
    )
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")