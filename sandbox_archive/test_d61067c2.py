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
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(inputs)
            elif gate_type == 'OR':
                result = any(inputs)
            stack.append(result)
        return stack.pop()
    
    def monotone_width(circuit):
        n = len(circuit)
        max_width = 0
        for i in range(n):
            width = sum(1 for _, inputs in circuit[:i+1] if len(inputs) > 1)
            max_width = max(max_width, width)
        return max_width
    
    def tropical_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if any(len(inputs) > 1 for _, inputs in circuit[:i+1]):
                rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        w_C = monotone_width(circuit)
        r_trop_C = tropical_rank(circuit)
        if evaluate_circuit(circuit) == 1:
            results.append((w_C, r_trop_C))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    w_C_values, r_trop_C_values = zip(*results)
    mean_w_C = sum(w_C_values) / len(w_C_values)
    mean_r_trop_C = sum(r_trop_C_values) / len(r_trop_C_values)
    correlation = sum((w - mean_w_C) * (r - mean_r_trop_C) for w, r in zip(w_C_values, r_trop_C_values)) / (len(results) * math.sqrt(sum((w - mean_w_C)**2 for w in w_C_values) * sum((r - mean_r_trop_C)**2 for r in r_trop_C_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": correlation > 0.8 and mean_r_trop_C / mean_w_C <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")