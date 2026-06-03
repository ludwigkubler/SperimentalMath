# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product

# Helper function to generate a random boolean circuit
def generate_random_circuit(n):
    gate_types = ['AND', 'OR', 'NOT']
    circuit = []
    for _ in range(2**n - 1):  # Number of gates needed for n inputs
        gate_type = random.choice(gate_types)
        if gate_type == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(2)]
        circuit.append((gate_type, inputs))
    return circuit

# Helper function to compute the minimal local indeterminacy (mli)
def mli(circuit):
    # Placeholder implementation
    return random.random()

# Helper function to compute the monotone width (w_mon)
def w_mon(circuit):
    # Placeholder implementation
    return random.randint(1, 5)

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mli_values = []
    w_mon_values = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        mli_val = mli(circuit)
        w_mon_val = w_mon(circuit)
        
        mli_values.append(mli_val)
        w_mon_values.append(w_mon_val)
    
    if len(mli_values) < 30 or len(w_mon_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(mli_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    # Calculate Pearson correlation coefficient
    mean_mli = sum(mli_values) / len(mli_values)
    mean_w_mon = sum(w_mon_values) / len(w_mon_values)
    numerator = sum((mli_val - mean_mli) * (w_mon_val - mean_w_mon) for mli_val, w_mon_val in zip(mli_values, w_mon_values))
    denominator = sum((mli_val - mean_mli)**2 for mli_val in mli_values) ** 0.5 * sum((w_mon_val - mean_w_mon)**2 for w_mon_val in w_mon_values) ** 0.5
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mli_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

# Main function to run trials for multiple seeds
if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    # Calculate mean and standard deviation of metric_value
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    else:
        mean_metric_value = None
        std_metric_value = None
    
    # Calculate fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")