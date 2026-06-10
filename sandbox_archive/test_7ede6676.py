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
from fractions import Fraction
import math

def generate_random_circuit(n):
    if n < 2:
        raise ValueError("n must be at least 2")
    
    circuit = []
    gate_types = ["AND", "OR", "NOT"]
    for _ in range(10):  # Generate a simple circuit with 10 gates
        gate_type = random.choice(gate_types)
        if gate_type == "NOT":
            inputs = [random.randint(0, n-1)]
        else:
            inputs = [random.randint(0, n-1), random.randint(0, n-1)]
        circuit.append((gate_type, inputs))
    return circuit

def depth_of_circuit(circuit):
    if not circuit:
        return 0
    max_depth = 0
    for gate in circuit:
        if gate[0] == "NOT":
            depth = depth_of_circuit(gate[1])
        else:
            depth = max(depth_of_circuit(gate[1][0]), depth_of_circuit(gate[1][1]))
        max_depth = max(max_depth, depth + 1)
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        depth = depth_of_circuit(circuit)
        
        # Simulate constructing an arithmetic variety X and computing O(X)
        # For simplicity, let's assume O(X) is proportional to the number of gates
        O_X = len(circuit)
        
        results.append((O_X, depth))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    O_X_values = [O_X for O_X, _ in results]
    depth_values = [depth for _, depth in results]
    
    mean_O_X = sum(O_X_values) / len(O_X_values)
    mean_depth = sum(depth_values) / len(depth_values)
    
    covariance = sum((O_X - mean_O_X) * (depth - mean_depth) for O_X, depth in results) / len(results)
    variance_O_X = sum((O_X - mean_O_X) ** 2 for O_X in O_X_values) / len(O_X_values)
    variance_depth = sum((depth - mean_depth) ** 2 for depth in depth_values) / len(depth_values)
    
    if variance_O_X == 0 or variance_depth == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_O_X) * math.sqrt(variance_depth))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and all(O_X <= 2 * depth for O_X, depth in results),
        "counterexample": "" if correlation_coefficient >= 0.7 and all(O_X <= 2 * depth for O_X, depth in results) else "O(X) > 2*d(C)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not results:
            results.append(trial_result)
        else:
            results[-1]["instances_tested"] += trial_result["instances_tested"]
            results[-1]["n_max"] = max(results[-1]["n_max"], trial_result["n_max"])
            results[-1]["conjecture_holds"] &= trial_result["conjecture_holds"]
    
    if all(trial["conjecture_holds"] for trial in results):
        mean_metric_value = sum(trial["metric_value"] for trial in results) / len(results)
        std_metric_value = math.sqrt(sum((trial["metric_value"] - mean_metric_value) ** 2 for trial in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, trial in zip(seeds, results) if not trial["conjecture_holds"])
        mean_metric_value = sum(trial["metric_value"] for trial in results) / len(results)
        std_metric_value = math.sqrt(sum((trial["metric_value"] - mean_metric_value) ** 2 for trial in results) / len(results))
        support_fraction = (len(results) - sum(not trial["conjecture_holds"] for trial in results)) / len(results)
    
    if all(trial["instances_tested"] >= 30 for trial in results):
        RESULT = f"SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    else:
        RESULT = f"FALSIFIED counterexample=\"insufficient_instances\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)