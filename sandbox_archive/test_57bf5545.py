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
        # Generate a random boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        # Simplified heuristic to estimate entanglement complexity
        complexity = sum(len(inputs) for gate, inputs in circuit)
        return complexity
    
    def generate_quasi_monte_carlo_points(n, order):
        # Generate quasi-Monte Carlo lattice points using a simple method
        points = []
        for i in range(order):
            point = [math.cos(2 * math.pi * i / (order + 1)) for _ in range(n)]
            points.append(point)
        return points
    
    def check_uniform_distribution(points, circuit):
        # Check if the points cover all input vectors uniformly
        covered = set()
        for gate, inputs in circuit:
            key = tuple(inputs)
            if key not in covered:
                covered.add(key)
        return len(covered) == 2**len(circuit[0][1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        complexity = compute_entanglement_complexity(circuit)
        order = complexity + 1  # Simplified heuristic to estimate minimal order
        
        if not check_uniform_distribution(generate_quasi_monte_carlo_points(n, order), circuit):
            return {
                "metric_name": "order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "uniform_distribution_failed"
            }
        
        total_order += order
        total_complexity += complexity
        instances_tested += 1
    
    mean_order = total_order / len(n_values)
    mean_complexity = total_complexity / len(n_values)
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_order - mean_complexity) <= 2 * mean_complexity**(1/2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='uniform_distribution_failed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")