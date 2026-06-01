# auto-injected by SEC sandbox
import math
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

def generate_random_circuit(n):
    if n == 1:
        return ['NOT']
    else:
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, len(circuit)-1) for _ in range(2)]
        circuit = [gate] + inputs
        return circuit

def compute_circuit_monotone_width(circuit):
    if not circuit:
        return 0
    elif isinstance(circuit[0], list):
        return max(compute_circuit_monotone_width(subcircuit) for subcircuit in circuit)
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_random_circuit(n)
            monotone_width = compute_circuit_monotone_width(circuit)
            
            if len(circuit) > 1:  # Skip trivial circuits
                total_instances += 1
                
                # Simulate computing the minimal order of an elliptic curve (placeholder value)
                ord_E = random.randint(1, n * 2)
                
                results.append((ord_E, monotone_width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_E_values = [r[0] for r in results]
    monotone_widths = [r[1] for r in results]
    
    mean_ord_E = sum(ord_E_values) / len(ord_E_values)
    mean_monotone_width = sum(monotone_widths) / len(monotone_widths)
    
    covariance = sum((ord_E - mean_ord_E) * (monotone_width - mean_monotone_width) for ord_E, monotone_width in results) / len(results)
    variance_ord_E = sum((ord_E - mean_ord_E)**2 for ord_E in ord_E_values) / len(ord_E_values)
    variance_monotone_width = sum((monotone_width - mean_monotone_width)**2 for monotone_width in monotone_widths) / len(monotone_widths)
    
    correlation_coefficient = covariance / (variance_ord_E * variance_monotone_width**0.5)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": 0,
                "conjecture_holds": False,
                "counterexample": f"seed={seed}"
            }
        
        results.append(trial_result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = (sum((r["metric_value"] - mean_metric)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")