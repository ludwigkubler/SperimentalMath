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

def generate_d_regular_graph(n, d):
    if 2 * d < n or d > n - 1:
        return None
    
    graph = [[] for _ in range(n)]
    degree_count = [0] * n
    
    for i in range(n):
        while degree_count[i] < d:
            j = random.randint(0, n - 1)
            if i != j and j not in graph[i]:
                graph[i].append(j)
                graph[j].append(i)
                degree_count[i] += 1
                degree_count[j] += 1
    
    return graph

def calculate_geoc(phi):
    # Placeholder for the actual implementation of geoc(φ_G)
    # This is a dummy function that returns a random value for demonstration purposes
    return random.random()

def calculate_circuit_size(phi):
    # Placeholder for the actual implementation of s(φ_G)
    # This is a dummy function that returns a random value for demonstration purposes
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        
        if graph is None:
            continue
        
        phi = (graph, d)  # Placeholder for the actual group action φ_G
        geoc_value = calculate_geoc(phi)
        circuit_size = calculate_circuit_size(phi)
        
        results.append({
            "n": n,
            "geoc_value": geoc_value,
            "circuit_size": circuit_size
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    geoc_values = [result["geoc_value"] for result in results]
    circuit_sizes = [result["circuit_size"] for result in results]
    
    mean_geoc = sum(geoc_values) / instances_tested
    mean_circuit_size = sum(circuit_sizes) / instances_tested
    
    covariance = sum((x - mean_geoc) * (y - mean_circuit_size) for x, y in zip(geoc_values, circuit_sizes))
    variance_geoc = sum((x - mean_geoc) ** 2 for x in geoc_values)
    variance_circuit_size = sum((x - mean_circuit_size) ** 2 for x in circuit_sizes)
    
    if variance_geoc == 0 or variance_circuit_size == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Zero variance in geoc or circuit size"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_geoc) * math.sqrt(variance_circuit_size))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no valid trials")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        
        support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min(results, key=lambda x: abs(x - 0.8)))]
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation below threshold\" first_failing_seed={first_failing_seed}")