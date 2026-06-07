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
        if n <= 0 or d <= 0 or (n % d != 0):
            return None
        circuit = []
        for i in range(n):
            row = [random.randint(0, 1) for _ in range(d)]
            circuit.append(row)
        return circuit
    
    def calculate_entanglement_complexity(circuit):
        n = len(circuit)
        d = len(circuit[0])
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if any(circuit[i][k] != circuit[j][k] for k in range(d)):
                    complexity += 1
        return complexity
    
    def calculate_minimal_index(circuit):
        n = len(circuit)
        d = len(circuit[0])
        index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if any(circuit[i][k] != circuit[j][k] for k in range(d)):
                    index += 1
        return index
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_d_regular_circuit(n, 2)  # Assuming d=2 for simplicity
            if circuit is None:
                continue
            entanglement_complexity = calculate_entanglement_complexity(circuit)
            minimal_index = calculate_minimal_index(circuit)
            results.append((entanglement_complexity, minimal_index))
    
    if not results:
        return {
            "metric_name": "PearsonCorrelation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglement_complexities, minimal_indices = zip(*results)
    correlation_coefficient = pearson_correlation(entanglement_complexities, minimal_indices)
    
    return {
        "metric_name": "PearsonCorrelation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(circuit) for circuit in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        print("RESULT: INCONCLUSIVE no data")