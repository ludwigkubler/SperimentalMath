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
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} {r})' for l in left for r in right]
    
    def local_index(circuit):
        if circuit == '0':
            return 1
        elif circuit[0] == '(':
            return local_index(circuit[1:circuit.index(' ')]) * local_index(circuit[circuit.index(' ') + 1:circuit.rindex(' ')])
        else:
            return 1
    
    def monotone_width(circuit):
        if circuit == '0':
            return 1
        elif circuit[0] == '(':
            left = monotone_width(circuit[1:circuit.index(' ')])
            right = monotone_width(circuit[circuit.index(' ') + 1:circuit.rindex(' ')])
            return max(left, right) + 1
        else:
            return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_G = 0
        total_c_w = 0
        
        while len(results) < 30:
            circuit = generate_circuit(n)
            G = local_index(circuit)
            w = monotone_width(circuit)
            
            if G > 0 and w > 0:
                instances_tested += 1
                total_G += G
                total_c_w += math.pow(2, w)  # Assuming c=2 for simplicity
            
        if instances_tested < 30:
            return {
                "metric_name": "Local Index vs Monotone Width",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Insufficient instances"
            }
        
        results.append({
            "n": n,
            "G": total_G / instances_tested,
            "c_w": total_c_w / instances_tested
        })
    
    G_values = [r["G"] for r in results]
    c_w_values = [r["c_w"] for r in results]
    
    correlation_coefficient = sum((G - mean(G_values)) * (c_w - mean(c_w_values)) for G, c_w in zip(G_values, c_w_values)) / (len(results) * std(G_values) * std(c_w_values))
    
    return {
        "metric_name": "Local Index vs Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")