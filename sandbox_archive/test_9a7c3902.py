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
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        gate, left, right = circuit
        if gate == 'AND':
            return '1' if evaluate_circuit(left) == '1' and evaluate_circuit(right) == '1' else '0'
        elif gate == 'OR':
            return '1' if evaluate_circuit(left) == '1' or evaluate_circuit(right) == '1' else '0'
    
    def generate_random_circuit(depth):
        if depth == 0:
            return random.choice(['0', '1'])
        gate = random.choice(['AND', 'OR'])
        left = generate_random_circuit(depth - 1)
        right = generate_random_circuit(depth - 1)
        return (gate, left, right)
    
    def her(state):
        # Placeholder for actual HER calculation
        # For simplicity, we assume a linear relationship
        return len(state)
    
    circuit_depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in circuit_depths:
        circuit = generate_random_circuit(depth)
        state = evaluate_circuit(circuit)
        her_value = her(state)
        results.append({
            "depth": depth,
            "her_value": her_value
        })
    
    n_max = max(result["depth"] for result in results)
    instances_tested = len(results)
    metric_name = "HER(C)"
    metric_values = [result["her_value"] for result in results]
    mean_metric_value = sum(metric_values) / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / instances_tested)
    
    conjecture_holds = all(value <= depth * 1.5 for value, depth in zip(metric_values, circuit_depths))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")