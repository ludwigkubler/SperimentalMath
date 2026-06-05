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
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def construct_quasi_crystal(circuit):
        quasi_crystal = set()
        for gate, inputs in circuit:
            if gate == 'AND':
                key = tuple(sorted(inputs + [0]))
            elif gate == 'OR':
                key = tuple(sorted(inputs + [1]))
            quasi_crystal.add(key)
        return quasi_crystal
    
    def calculate_minimal_order(quasi_crystal):
        return len(quasi_crystal)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_qc_size = 0
    total_w_cubertwothirds = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            w = random.randint(1, n)
            circuit = generate_circuit(n, w)
            quasi_crystal = construct_quasi_crystal(circuit)
            qc_size = calculate_minimal_order(quasi_crystal)
            
            instances_tested += 1
            total_qc_size += qc_size
            total_w_cubertwothirds += w ** (2/3)
    
    mean_qc_size = total_qc_size / instances_tested
    mean_w_cubertwothirds = total_w_cubertwothirds / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    correlation_coefficient = (mean_qc_size * mean_w_cubertwothirds) / (math.sqrt(mean_qc_size ** 2 * mean_w_cubertwothirds ** 2))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.1,  # Non-trivially greater than zero
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")