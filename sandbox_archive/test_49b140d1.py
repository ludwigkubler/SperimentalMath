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
    
    def generate_boolean_circuit(n):
        # Generate a random Boolean circuit with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_coxeter_group(circuit):
        # Construct the Coxeter group associated with the circuit
        n = int(math.log2(len(circuit)))
        return [[i, i^j] for i in range(n) for j in range(i+1, n)]
    
    def diameter(group):
        # Compute the diameter of the Coxeter group
        n = len(group)
        dist = [[float('inf')] * n for _ in range(n)]
        for u in range(n):
            dist[u][u] = 0
        for u, v in group:
            dist[u][v] = dist[v][u] = 1
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return max(max(row) for row in dist)
    
    def reflection_system_size(group):
        # Compute the size of a reflection system
        n = len(group)
        reflections = set()
        for u, v in group:
            if abs(u - v) == 1:
                reflections.add((u, v))
        return len(reflections)
    
    n_max = 0
    metric_value = 0.0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        circuit = generate_boolean_circuit(n)
        group = construct_coxeter_group(circuit)
        diameter_value = diameter(group)
        reflection_size = reflection_system_size(group)
        
        metric_value += diameter_value
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "diameter",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_diameter = metric_value / instances_tested
    conjecture_holds = all(diameter <= n**2 * math.log(n) for diameter in [diameter(group) for _ in range(30)])
    
    return {
        "metric_name": "diameter",
        "metric_value": mean_diameter,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")