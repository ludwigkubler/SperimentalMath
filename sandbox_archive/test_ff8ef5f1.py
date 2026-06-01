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

def generate_circuit(depth):
    if depth == 0:
        return ['x1', 'x2']
    else:
        inputs = generate_circuit(depth - 1)
        gate = random.choice(['AND', 'OR'])
        new_input = f'({gate} {inputs[0]} {inputs[1]})'
        return [new_input]

def compute_geometric_entropy(circuit):
    # Placeholder for geometric entropy calculation
    # This is a dummy implementation and should be replaced with actual logic
    return 1.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        inputs = set(circuit)
        H_geo_I_C = compute_geometric_entropy(circuit)
        d_C = len(inputs) - 1
        
        if d_C == 0 or H_geo_I_C <= 0:
            continue
        
        results.append({
            "n": n,
            "d_C": d_C,
            "H_geo_I_C": H_geo_I_C
        })
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    d_values = [result["d_C"] for result in results]
    H_geo_I_C_values = [result["H_geo_I_C"] for result in results]
    
    mean_d = sum(d_values) / instances_tested
    mean_H_geo_I_C = sum(H_geo_I_C_values) / instances_tested
    
    covariance = sum((d - mean_d) * (H_geo_I_C - mean_H_geo_I_C) for d, H_geo_I_C in zip(d_values, H_geo_I_C_values))
    variance_d = sum((d - mean_d)**2 for d in d_values)
    
    if variance_d == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Variance of d_C is zero"
        }
    
    pearsons_r = covariance / math.sqrt(variance_d * sum((H_geo_I_C - mean_H_geo_I_C)**2 for H_geo_I_C in H_geo_I_C_values))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearsons_r >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")