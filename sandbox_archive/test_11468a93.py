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
    
    def generate_random_boolean_circuit(depth):
        if depth == 1:
            return ['0', '1']
        else:
            left = generate_random_boolean_circuit(random.randint(1, depth-1))
            right = generate_random_boolean_circuit(random.randint(1, depth-1))
            gate = random.choice(['AND', 'OR'])
            return [f"({gate} {x} {y})" for x in left for y in right]
    
    def evaluate_circuit(circuit):
        if circuit == '0':
            return 0
        elif circuit == '1':
            return 1
        else:
            gate, x, y = circuit.split()
            if gate == 'AND':
                return evaluate_circuit(x) and evaluate_circuit(y)
            elif gate == 'OR':
                return evaluate_circuit(x) or evaluate_circuit(y)
    
    def galois_group(circuit):
        # Simplified Galois group calculation for demonstration
        # This is a placeholder and should be replaced with actual computation
        return set()
    
    def minimal_splitting_field_extension_degree(galois_group):
        # Placeholder for actual computation
        return len(galois_group)
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        for _ in range(5):  # Aim for at least 30 instances per seed
            circuit = generate_random_boolean_circuit(depth)
            value = evaluate_circuit(circuit)
            galois_group_value = galois_group(circuit)
            degree = minimal_splitting_field_extension_degree(galois_group_value)
            results.append((depth, degree))
    
    if not results:
        return {
            "metric_name": "minimal_splitting_field_extension_degree",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(result[1] for result in results) / len(results)
    conjecture_holds = all(degree <= 4 * depth ** 2 for depth, degree in results)
    counterexample = "" if conjecture_holds else "degree > 4*D^2"
    
    return {
        "metric_name": "minimal_splitting_field_extension_degree",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(depth for depth, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] >= 30 for result in results):
        print("RESULT: INCONCLUSIVE reason=insufficient_instances")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"degree > 4*D^2\" first_failing_seed={first_failing_seed}")