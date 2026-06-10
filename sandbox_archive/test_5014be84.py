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

def generate_random_circuit(n):
    gates = ['AND', 'OR', 'NOT']
    circuit = []
    for _ in range(n):
        gate = random.choice(gates)
        if gate == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(2)]
        circuit.append((gate, inputs))
    return circuit

def p_adic_metric(circuit):
    metric = 0
    for gate, inputs in circuit:
        if gate == 'NOT':
            metric += abs(inputs[0] - (1 - inputs[0]))
        elif gate == 'AND':
            metric += abs(inputs[0] * inputs[1] - (inputs[0] + inputs[1] - inputs[0] * inputs[1]))
        elif gate == 'OR':
            metric += abs(inputs[0] + inputs[1] - inputs[0] * inputs[1])
    return metric

def entanglement_complexity(circuit):
    # Simplified version for demonstration
    complexity = 0
    for _, inputs in circuit:
        if len(set(inputs)) > 1:
            complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    r_p_list = []
    e_c_list = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        r_p = p_adic_metric(circuit)
        e_c = entanglement_complexity(circuit)
        
        if r_p is None or e_c is None:
            return {
                "metric_name": "p-adic Metric Rank vs Entanglement Complexity",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        r_p_list.append(r_p)
        e_c_list.append(e_c)
    
    if not r_p_list or not e_c_list:
        return {
            "metric_name": "p-adic Metric Rank vs Entanglement Complexity",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "empty_list"
        }
    
    mean_r_p = sum(r_p_list) / len(r_p_list)
    mean_e_c = sum(e_c_list) / len(e_c_list)
    mean_diff = sum(abs(r - e) for r, e in zip(r_p_list, e_c_list)) / len(r_p_list)
    
    correlation_coefficient = 0
    if len(r_p_list) > 1:
        numerator = sum((r_p - mean_r_p) * (e_c - mean_e_c) for r_p, e_c in zip(r_p_list, e_c_list))
        denominator = math.sqrt(sum((r_p - mean_r_p)**2 for r_p in r_p_list)) * math.sqrt(sum((e_c - mean_e_c)**2 for e_c in e_c_list))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "p-adic Metric Rank vs Entanglement Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and mean_diff <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        mean_value = sum(r["metric_value"] for r in results if "metric_value" in r)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if "metric_value" in r))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all('conjecture_holds' in r and r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")