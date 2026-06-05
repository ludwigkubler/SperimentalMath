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
    
    def generate_d_regular_circuit(n, d):
        if (n * d) % 2 != 0:
            return None
        circuit = [[None] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        for u, v in edges:
            circuit[u][v] = 'X'
            circuit[v][u] = 'X'
        return circuit
    
    def count_automorphism_generators(circuit):
        n = len(circuit)
        generators = set()
        for i in range(n):
            for j in range(i + 1, n):
                if all(circuit[i][k] == circuit[j][k] for k in range(n)):
                    generators.add((i, j))
        return len(generators)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(circuit[i][k] == circuit[j][k] for k in range(n)):
                    width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_d_regular_circuit(n, 2)
        if circuit is None:
            continue
        generators = count_automorphism_generators(circuit)
        width = monotone_width(circuit)
        results.append({
            "n": n,
            "generators": generators,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "Automorphism Generators vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [math.sqrt(result["width"]) for result in results]
    generators_values = [result["generators"] for result in results]
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = sum((metric_values[i] - mean_metric_value) * (generators_values[i] - mean_generators_value) for i in range(len(results))) / (len(results) * std_metric_value * math.sqrt(sum((x - mean_generators_value) ** 2 for x in generators_values)))
    
    p_value = 2 * (1 - abs(correlation_coefficient)) if correlation_coefficient >= 0 else 2 * abs(correlation_coefficient)
    
    return {
        "metric_name": "Automorphism Generators vs Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value > 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_metric_values_are_none")