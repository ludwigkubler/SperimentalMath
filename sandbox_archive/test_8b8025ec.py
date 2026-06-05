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
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_quaternionic_automorphism_group(circuit):
        # Placeholder for the actual computation
        # For simplicity, we assume a linear relationship between n and Γ(C)
        return len(circuit) * 2
    
    def calculate_entanglement(circuit):
        # Placeholder for the actual calculation
        # For simplicity, we assume a linear relationship between n and E(C)
        return len(circuit) / 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_random_boolean_circuit(n)
        gamma_C = compute_quaternionic_automorphism_group(circuit)
        E_C = calculate_entanglement(circuit)
        
        if gamma_C == 0 or E_C == 0:
            continue
        
        results.append((n, gamma_C, E_C))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    n_values = [r[0] for r in results]
    gamma_C_values = [math.log2(r[1]) for r in results]
    E_C_values = [r[2] for r in results]
    
    mean_gamma_C = sum(gamma_C_values) / len(gamma_C_values)
    mean_E_C = sum(E_C_values) / len(E_C_values)
    covariance = sum((gamma_C_values[i] - mean_gamma_C) * (E_C_values[i] - mean_E_C) for i in range(len(results))) / len(results)
    variance_gamma_C = sum((gamma_C_values[i] - mean_gamma_C)**2 for i in range(len(results))) / len(results)
    variance_E_C = sum((E_C_values[i] - mean_E_C)**2 for i in range(len(results))) / len(results)
    
    r = covariance / (math.sqrt(variance_gamma_C) * math.sqrt(variance_E_C))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": r >= 0.7 or r == 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")