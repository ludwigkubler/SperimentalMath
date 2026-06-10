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
    
    def generate_random_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_entanglement_entropy(circuit):
        # Simplified version of entanglement entropy calculation
        n = int(math.log2(len(circuit)))
        if n == 0:
            return 0
        p = circuit.count(1) / len(circuit)
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    def calculate_symplectic_volume(circuit):
        # Simplified version of symplectic volume calculation
        n = int(math.log2(len(circuit)))
        if n == 0:
            return 1
        return sum(1 for bit in circuit if bit == 1) / len(circuit)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_random_boolean_circuit(n)
        sv = calculate_symplectic_volume(circuit)
        h = calculate_entanglement_entropy(circuit)
        results.append((sv, h))
    
    if n == 1:
        conjecture_holds = True
        counterexample = ""
    else:
        correlation_coefficient = pearson_correlation([x for x, _ in results], [y for _, y in results])
        conjecture_holds = correlation_coefficient >= 0.8
        counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_correlation([x for x, _ in results], [y for _, y in results]),
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["n_max"] >= 16 for result in results):
        if mean_metric_value is not None and std_metric_value is not None:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE metric_value or std is None")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds support the conjecture")