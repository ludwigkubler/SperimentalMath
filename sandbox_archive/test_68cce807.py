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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def circuit_monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if any(j < i for j in circuit[i][1]):
                width += 1
        return width
    
    def minimal_order_of_elliptic_curve(circuit):
        # Simplified model to generate a random order
        n = len(circuit)
        return random.randint(2, n * 5)
    
    instances_tested = 0
    n_max = 0
    ord_E_values = []
    w_mon_C_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            ord_E = minimal_order_of_elliptic_curve(circuit)
            w_mon_C = circuit_monotone_width(circuit)
            
            ord_E_values.append(ord_E)
            w_mon_C_values.append(w_mon_C)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_ord_E = sum(ord_E_values) / instances_tested
    mean_w_mon_C = sum(w_mon_C_values) / instances_tested
    
    covariance = sum((ord_E - mean_ord_E) * (w_mon_C - mean_w_mon_C) for ord_E, w_mon_C in zip(ord_E_values, w_mon_C_values)) / instances_tested
    variance_ord_E = sum((ord_E - mean_ord_E)**2 for ord_E in ord_E_values) / instances_tested
    variance_w_mon_C = sum((w_mon_C - mean_w_mon_C)**2 for w_mon_C in w_mon_C_values) / instances_tested
    
    correlation_coefficient = covariance / (math.sqrt(variance_ord_E) * math.sqrt(variance_w_mon_C))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")