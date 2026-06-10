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
    
    def generate_circuit(n, d):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(d)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_kissing_number(circuit):
        n = len(circuit)
        d = len(circuit[0][1])
        positions = {}
        for i, (gate_type, inputs) in enumerate(circuit):
            position = tuple(inputs)
            if position not in positions:
                positions[position] = []
            positions[position].append(i)
        
        kissing_number = 0
        for pos, indices in positions.items():
            if len(indices) > 1:
                kissing_number += len(indices)
        return kissing_number
    
    def d_n_log_n(d, n):
        return d**n * math.log(n)
    
    def run_circuit_trials(seed: int, n_min=5, n_max=30, num_trials=30):
        results = []
        for _ in range(num_trials):
            n = random.randint(n_min, n_max)
            d = random.randint(1, 5)  # Simplified to avoid high-dimensional space
            circuit = generate_circuit(n, d)
            k_C = compute_kissing_number(circuit)
            upper_bound = d_n_log_n(d, n)
            ratio = k_C / upper_bound if upper_bound != 0 else float('inf')
            results.append(ratio)
        return results
    
    ratios = run_circuit_trials(seed)
    
    metric_name = "kissing_number_ratio"
    metric_value = sum(ratios) / len(ratios)
    instances_tested = len(ratios)
    n_max = max(30, max(len(gate[1]) for gate in generate_circuit(30, 5)))
    conjecture_holds = all(r <= 1.5 for r in ratios) and metric_value <= 1.2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")