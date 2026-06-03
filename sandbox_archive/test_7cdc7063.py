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
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        n = len(circuit[0][1])
        width = 0
        for i in range(2**n):
            active_gates = [j for j, (_, inputs) in enumerate(circuit) if all(inputs[k] == (i >> k) & 1 for k in range(n))]
            width = max(width, len(active_gates))
        return width
    
    def compute_diophantine_degree(circuit):
        n = len(circuit[0][1])
        degree = 0
        for i in range(2**n):
            active_gates = [j for j, (_, inputs) in enumerate(circuit) if all(inputs[k] == (i >> k) & 1 for k in range(n))]
            degree = max(degree, len(active_gates))
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_boolean_circuit(n)
        w = compute_monotone_width(circuit)
        d = compute_diophantine_degree(circuit)
        results.append((w, d))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ws = [w for w, _ in results]
    ds = [d for _, d in results]
    
    mean_w = sum(ws) / len(ws)
    mean_d = sum(ds) / len(ds)
    var_w = sum((x - mean_w)**2 for x in ws) / len(ws)
    var_d = sum((y - mean_d)**2 for y in ds) / len(ds)
    
    if var_w == 0 or var_d == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    cov = sum((ws[i] - mean_w) * (ds[i] - mean_d) for i in range(len(ws))) / len(ws)
    correlation_coefficient = cov / math.sqrt(var_w * var_d)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "first_failing_seed"
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")