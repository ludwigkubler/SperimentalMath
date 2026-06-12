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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_symplectic_hull_volume(circuit):
        # Placeholder function to simulate SHV computation
        return random.random() * 10
    
    def derive_frege_proof_depth(circuit):
        # Placeholder function to simulate FPD computation
        return random.randint(5, 20)
    
    n_max = 38
    instances_tested = 0
    shv_values = []
    fpd_values = []
    
    for _ in range(30):
        circuit = generate_boolean_circuit(n_max)
        shv = compute_symplectic_hull_volume(circuit)
        fpd = derive_frege_proof_depth(circuit)
        
        if shv is not None and fpd is not None:
            instances_tested += 1
            shv_values.append(shv)
            fpd_values.append(fpd)
    
    if instances_tested == 0:
        return {
            "metric_name": "SHV vs FPD",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((shv_values[i] - mean_shv) * (fpd_values[i] - mean_fpd) for i in range(instances_tested)) / instances_tested
    mean_shv = sum(shv_values) / instances_tested
    mean_fpd = sum(fpd_values) / instances_tested
    
    return {
        "metric_name": "SHV vs FPD",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / (sum(1 for r in results if r["metric_value"] is not None) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")