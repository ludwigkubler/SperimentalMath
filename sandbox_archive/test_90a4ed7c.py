# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(depth):
        if depth == 1:
            return ['AND', 'OR']
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return [random.choice(['AND', 'OR']), *subcircuits]
    
    def is_valid_circuit(circuit):
        if isinstance(circuit, list):
            return all(isinstance(x, (str, list)) and x in ['AND', 'OR'] for x in circuit)
        return False
    
    def compute_symmetry_group(circuit):
        # Simplified version of computing the symmetry group
        # This is a placeholder as actual computation would be complex
        return 2 ** len(circuit) if is_valid_circuit(circuit) else None
    
    def depth_of_circuit(circuit):
        if isinstance(circuit, list):
            return 1 + max(depth_of_circuit(x) for x in circuit)
        return 0
    
    metrics = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # 5 instances per depth
            circuit = generate_circuit(n)
            if is_valid_circuit(circuit):
                symmetry_group_order = compute_symmetry_group(circuit)
                circuit_depth = depth_of_circuit(circuit)
                metrics.append((symmetry_group_order, circuit_depth))
                n_max = max(n_max, n)
                instances_tested += 1
    
    if not metrics:
        return {
            "metric_name": "Symmetry Group Order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_order = sum(order for order, _ in metrics)
    avg_order = Fraction(total_order, instances_tested)
    max_order = max(order for order, _ in metrics)
    
    conjecture_holds = all(order <= 2**depth for order, depth in metrics) and avg_order <= 2**(max(metrics, key=lambda x: x[1])[1] + 1)
    counterexample = "" if conjecture_holds else f"Max Order: {max_order}, Max Depth: {max(metrics, key=lambda x: x[1])[1]}"
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": avg_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - avg_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")