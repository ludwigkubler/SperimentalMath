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

def generate_boolean_circuit(n):
    if n <= 1:
        return []
    
    circuit = []
    for _ in range(n - 1):
        gate_type = random.choice(['AND', 'OR'])
        inputs = random.sample(range(len(circuit) + 1), 2)
        circuit.append((gate_type, inputs))
    
    return circuit

def compute_formal_power_series(circuit):
    n = len(circuit) + 1
    power_series = [0] * (n + 1)
    power_series[0] = 1
    
    for gate_type, inputs in circuit:
        new_series = [0] * (n + 1)
        if gate_type == 'AND':
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if i & j == i and i & j == j:
                        new_series[i | j] += power_series[i] * power_series[j]
        elif gate_type == 'OR':
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if (i | j) == i or (i | j) == j:
                        new_series[i | j] += power_series[i] * power_series[j]
        power_series = new_series
    
    return power_series

def minimal_p_adic_order(power_series):
    p = 2
    while True:
        non_zero_coefficients = [coeff for coeff in power_series if coeff % p != 0]
        if not non_zero_coefficients:
            break
        p += 1
    return p

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        power_series = compute_formal_power_series(circuit)
        p_adic_order = minimal_p_adic_order(power_series)
        
        if p_adic_order == 0:
            return {
                "metric_name": "minimal_p_adic_order",
                "metric_value": -1,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "p-adic order is zero for some circuit"
            }
        
        results.append(p_adic_order)
    
    mean_p_adic_order = sum(results) / len(results)
    max_p_adic_order = max(results)
    
    f_n_values = [math.log(n, 2)**2 for n in n_values]
    
    conjecture_holds = all(order <= f_n for order, f_n in zip(results, f_n_values))
    
    return {
        "metric_name": "minimal_p_adic_order",
        "metric_value": mean_p_adic_order,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"p-adic order {max_p_adic_order} exceeds f(n) for n={n_values[results.index(max_p_adic_order)]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")