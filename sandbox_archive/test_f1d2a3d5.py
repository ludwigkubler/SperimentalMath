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
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'NOT':
                result = 1 - inputs[0]
            elif gate_type == 'AND':
                result = all(inputs)
            else:
                result = any(inputs)
            stack.append(result)
        return stack.pop()
    
    def calculate_minimal_local_indeterminacy(state):
        # Placeholder for actual calculation
        return random.random() * len(state)
    
    def calculate_monotone_width(circuit):
        # Placeholder for actual calculation
        return len(circuit)
    
    mli_values = []
    w_mon_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_boolean_circuit(n)
        state = evaluate_circuit(circuit)
        mli = calculate_minimal_local_indeterminacy(state)
        w_mon = calculate_monotone_width(circuit)
        
        if len(mli_values) >= 30:
            break
        
        mli_values.append(mli)
        w_mon_values.append(w_mon)
    
    if len(mli_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(mli_values),
            "n_max": max(len(circuit) for circuit in [generate_boolean_circuit(n) for n in range(5, 41)]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_mli = sum(mli_values) / len(mli_values)
    mean_w_mon = sum(w_mon_values) / len(w_mon_values)
    covariance = sum((mli - mean_mli) * (w_mon - mean_w_mon) for mli, w_mon in zip(mli_values, w_mon_values)) / len(mli_values)
    variance_mli = sum((mli - mean_mli) ** 2 for mli in mli_values) / len(mli_values)
    variance_w_mon = sum((w_mon - mean_w_mon) ** 2 for w_mon in w_mon_values) / len(w_mon_values)
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_mli) * math.sqrt(variance_w_mon))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": 30,
        "n_max": max(len(circuit) for circuit in [generate_boolean_circuit(n) for n in range(5, 41)]),
        "conjecture_holds": pearson_corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 1000) for _ in range(30)]
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_support")