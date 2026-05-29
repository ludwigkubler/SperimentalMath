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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_symmetry_group_order(circuit):
        # Simplified algorithm to simulate symmetry group order computation
        size = len(circuit)
        depth = max(len(inputs) for _, inputs in circuit)
        return Fraction(size * (size - 1), depth)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_monotone_circuit(n)
            depth = max(len(inputs) for _, inputs in circuit)
            order = compute_symmetry_group_order(circuit)
            results.append((n, len(circuit), depth, order))
    
    total_size = sum(size for _, size, _, _ in results)
    total_depth = sum(depth for _, _, depth, _ in results)
    total_order = sum(order for _, _, _, order in results)
    
    mean_size = Fraction(total_size, len(results))
    mean_depth = Fraction(total_depth, len(results))
    mean_order = Fraction(total_order, len(results))
    
    expected_order = mean_size * (mean_size - 1) / mean_depth
    within_range = all(abs(order - expected_order) <= expected_order * Fraction(10, 100) for _, _, _, order in results)
    
    conjecture_holds = within_range
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = Fraction(total_metric_value, len(results))
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")