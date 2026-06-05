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
        if n % d != 0:
            return None
        circuit = []
        for _ in range(d):
            layer = [random.randint(0, 1) for _ in range(n // d)]
            circuit.append(layer)
        return circuit
    
    def compute_monotone_width(circuit):
        width = 0
        n = len(circuit[0])
        for i in range(n):
            count_ones = sum(row[i] for row in circuit)
            if count_ones > width:
                width = count_ones
        return width
    
    def compute_automorphism_group(circuit):
        n = len(circuit[0])
        generators = set()
        for perm in itertools.permutations(range(n)):
            permuted_circuit = [row[i] for i, row in enumerate(circuit)]
            if all(permuted_circuit == circuit for _ in range(len(circuit))):
                generators.add(tuple(perm))
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_d_regular_circuit(n, 2)
            if circuit is None:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            generators = compute_automorphism_group(circuit)
            width = compute_monotone_width(circuit)
            results.append({"n": n, "generators": generators, "width": width})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["width"] for result in results]
    generators_values = [result["generators"] for result in results]
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    mean_generators_value = sum(generators_values) / len(generators_values)
    
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    std_generators_value = math.sqrt(sum((x - mean_generators_value) ** 2 for x in generators_values) / len(generators_values))
    
    correlation_coefficient = sum((metric_values[i] - mean_metric_value) * (generators_values[i] - mean_generators_value) for i in range(len(results))) / (len(results) * std_metric_value * std_generators_value)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")