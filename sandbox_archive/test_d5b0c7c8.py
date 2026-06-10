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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return [(gate, inputs)]

    def her(circuit):
        if not circuit:
            return 0
        elif isinstance(circuit[0], list):
            return sum(her(subcircuit) for subcircuit in circuit[0])
        else:
            gate, inputs = circuit
            return max(her(input_circuit) for input_circuit in inputs)

    def calculate_circuit_depth(circuit):
        if not circuit:
            return 0
        elif isinstance(circuit[0], list):
            return 1 + max(calculate_circuit_depth(subcircuit) for subcircuit in circuit[0])
        else:
            gate, inputs = circuit
            return 1 + max(calculate_circuit_depth(input_circuit) for input_circuit in inputs)

    metric_values = []
    instances_tested = 0
    n_max = 0

    for depth in range(5, 41):
        circuit = generate_random_circuit(depth)
        her_value = her(circuit)
        depth_value = calculate_circuit_depth(circuit)
        
        if her_value > 0 and depth_value > 0:
            metric_values.append(her_value / depth_value)
            instances_tested += 1
            n_max = max(n_max, depth)

    if not metric_values:
        return {
            "metric_name": "HER/D",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }

    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(value <= 1 for value in metric_values)

    return {
        "metric_name": "HER/D",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No valid circuits generated")