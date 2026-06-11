# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def generate_boolean_circuit(n, d):
    if n == 1:
        return ['x']
    elif d == 1:
        inputs = generate_boolean_circuit(n // 2, d - 1)
        outputs = generate_boolean_circuit(n // 2, d - 1)
        return [f'({inputs[i]} {outputs[i]} {inputs[i + len(inputs)//2]})' for i in range(len(inputs))]
    else:
        inputs = generate_boolean_circuit(n, d - 1)
        return inputs

def calculate_entanglement_complexity(circuit):
    # Placeholder function to simulate entanglement complexity calculation
    return len(circuit)

def calculate_hodge_de_rham_cohomology_dimension(circuit):
    # Placeholder function to simulate Hodge-De Rham cohomology dimension calculation
    return len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 1:
            circuit = generate_boolean_circuit(n, 40)
            entanglement_complexity = calculate_entanglement_complexity(circuit)
            hodge_de_rham_dimension = calculate_hodge_de_rham_cohomology_dimension(circuit)
            results.append((hodge_de_rham_dimension, entanglement_complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    hdim = [r[0] for r in results]
    e_phi = [r[1] for r in results]
    
    n = len(hdim)
    mean_hdim = sum(hdim) / n
    mean_e_phi = sum(e_phi) / n
    
    covariance = sum((hdim[i] - mean_hdim) * (e_phi[i] - mean_e_phi) for i in range(n)) / n
    variance_hdim = sum((hdim[i] - mean_hdim) ** 2 for i in range(n)) / n
    variance_e_phi = sum((e_phi[i] - mean_e_phi) ** 2 for i in range(n)) / n
    
    pearson_correlation_coefficient = covariance / (math.sqrt(variance_hdim) * math.sqrt(variance_e_phi))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": n,
        "n_max": 40,
        "conjecture_holds": pearson_correlation_coefficient >= 0.8 and pearson_correlation_coefficient <= -0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 or r["metric_value"] > -0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<not provided>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")