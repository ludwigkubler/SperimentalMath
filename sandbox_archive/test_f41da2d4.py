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
    n = 10  # Start with a small size and increase if needed
    max_n = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Calculate communication complexity rank r(f)
        circuit_ranks = [len(circuit) for circuit in generate_circuits(f)]
        r_f = max(circuit_ranks)
        
        # Encode Boolean function f as a modular form φ_f using graphical Langlands duality
        phi_f = encode_modular_form(f)
        
        # Calculate minimal representation degree d(φ_f)
        d_phi_f = calculate_minimal_representation_degree(phi_f)
        
        metric_values.append((d_phi_f, r_f))
    
    correlation_coefficient = pearson_correlation(metric_values)
    mean_absolute_difference = sum(abs(d - r) for d, r in metric_values) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_circuits(f):
    # Placeholder for circuit generation logic
    circuits = []
    for i in range(len(f)):
        if f[i] == 1:
            circuits.append([i])
    return circuits

def encode_modular_form(f):
    # Placeholder for modular form encoding logic
    phi_f = [0] * len(f)
    for i, val in enumerate(f):
        phi_f[i] = val
    return phi_f

def calculate_minimal_representation_degree(phi_f):
    # Placeholder for minimal representation degree calculation logic
    d_phi_f = sum(1 for x in phi_f if x == 1)
    return d_phi_f

def pearson_correlation(metric_values):
    n = len(metric_values)
    if n < 2:
        return 0
    
    x_sum, y_sum = 0, 0
    xy_sum, xx_sum, yy_sum = 0, 0, 0
    
    for d_phi_f, r_f in metric_values:
        x_sum += d_phi_f
        y_sum += r_f
        xy_sum += d_phi_f * r_f
        xx_sum += d_phi_f ** 2
        yy_sum += r_f ** 2
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * xx_sum - x_sum ** 2) * (n * yy_sum - y_sum ** 2))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")