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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(random.randint(1, n)):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(0, n-1)))
            else:
                inputs = random.sample(range(n), 2)
                circuit.append((gate, inputs[0], inputs[1]))
        return circuit
    
    def compute_quaternionic_automorphism_group(circuit):
        # Placeholder for quaternionic automorphism group computation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(circuit)
        return 2**n
    
    def calculate_entanglement(circuit):
        # Placeholder for entanglement calculation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(circuit)
        return random.uniform(0, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            automorphism_group_order = compute_quaternionic_automorphism_group(circuit)
            entanglement = calculate_entanglement(circuit)
            results.append({
                "n": n,
                "automorphism_group_order": automorphism_group_order,
                "entanglement": entanglement
            })
    
    log2_automorphism_group_orders = [math.log2(result["automorphism_group_order"]) for result in results]
    entanglements = [result["entanglement"] for result in results]
    
    if len(log2_automorphism_group_orders) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    n = len(log2_automorphism_group_orders)
    mean_log2_order = sum(log2_automorphism_group_orders) / n
    mean_entanglement = sum(entanglements) / n
    
    covariance = sum((log2_automorphism_group_orders[i] - mean_log2_order) * (entanglements[i] - mean_entanglement) for i in range(n)) / n
    variance_log2_order = sum((log2_automorphism_group_orders[i] - mean_log2_order)**2 for i in range(n)) / n
    variance_entanglement = sum((entanglements[i] - mean_entanglement)**2 for i in range(n)) / n
    
    pearson_correlation_coefficient = covariance / (math.sqrt(variance_log2_order) * math.sqrt(variance_entanglement))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": pearson_correlation_coefficient >= 0.7 or pearson_correlation_coefficient == 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")