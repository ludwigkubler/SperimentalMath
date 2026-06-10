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

def generate_random_circuit(depth):
    if depth <= 0:
        return []
    elif depth == 1:
        return ['NOT']
    else:
        inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
        gate = random.choice(['AND', 'OR'])
        return [gate] + inputs

def compute_matroid(circuit):
    if not circuit:
        return []
    elif len(circuit) == 1:
        return [circuit[0]]
    else:
        gate = circuit[0]
        inputs = circuit[1:]
        matroid = []
        for input_circuit in inputs:
            matroid.extend(compute_matroid(input_circuit))
        if gate == 'AND':
            matroid.append('AND')
        elif gate == 'OR':
            matroid.append('OR')
        return matroid

def compute_lidb(matroid):
    if not matroid:
        return 0
    else:
        lidb = 1
        for element in matroid:
            if element == 'NOT':
                lidb += 1
            elif element == 'AND' or element == 'OR':
                lidb += len(compute_matroid(element))
        return lidb

def compute_entanglement_complexity(circuit):
    if not circuit:
        return 0
    elif len(circuit) == 1:
        return 1
    else:
        gate = circuit[0]
        inputs = circuit[1:]
        complexity = 1
        for input_circuit in inputs:
            complexity += compute_entanglement_complexity(input_circuit)
        if gate == 'AND':
            complexity *= len(inputs)
        elif gate == 'OR':
            complexity *= sum(compute_entanglement_complexity(input_circuit) for input_circuit in inputs)
        return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    instances_tested = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(depth)
            matroid = compute_matroid(circuit)
            lidb = compute_lidb(matroid)
            entanglement_complexity = compute_entanglement_complexity(circuit)
            
            if n_max < depth:
                n_max = depth
            
            results.append((lidb, entanglement_complexity))
            instances_tested += 1
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lidb_values = [r[0] for r in results]
    entanglement_complexity_values = [r[1] for r in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_entanglement_complexity = sum(entanglement_complexity_values) / len(entanglement_complexity_values)
    
    covariance = sum((lidb - mean_lidb) * (entanglement_complexity - mean_entanglement_complexity) for lidb, entanglement_complexity in results) / len(results)
    variance_lidb = sum((lidb - mean_lidb) ** 2 for lidb in lidb_values) / len(lidb_values)
    variance_entanglement_complexity = sum((entanglement_complexity - mean_entanglement_complexity) ** 2 for entanglement_complexity in entanglement_complexity_values) / len(entanglement_complexity_values)
    
    correlation_coefficient = covariance / math.sqrt(variance_lidb * variance_entanglement_complexity)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")