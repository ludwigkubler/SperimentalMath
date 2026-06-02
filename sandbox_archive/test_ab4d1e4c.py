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
    
    def generate_d_regular_circuit(n, d):
        if n <= 1 or d < 2 or d >= n:
            return None
        circuit = []
        for _ in range(n):
            row = [0] * n
            row[random.randint(0, n-1)] = d
            circuit.append(row)
        return circuit
    
    def construct_representation(circuit):
        if not circuit:
            return None
        n = len(circuit)
        generator = [0] * n
        for i in range(n):
            if circuit[i][i] == 0:
                continue
            generator[i] = 1
            break
        return generator
    
    def calculate_max_weight(circuit):
        if not circuit:
            return None
        max_weight = 0
        for row in circuit:
            max_weight = max(max_weight, max(row))
        return max_weight
    
    def calculate_correlation(representations, weights):
        n = len(representations)
        if n != len(weights):
            return None
        x_sum = sum(weights)
        y_sum = sum([math.log2(len(r)) for r in representations])
        xy_sum = sum(w * math.log2(len(r)) for w, r in zip(weights, representations))
        x_square_sum = sum(w**2 for w in weights)
        y_square_sum = sum((len(r) ** 2) / n for r in representations)
        
        if x_square_sum == 0 or y_square_sum == 0:
            return None
        
        correlation_coefficient = (n * xy_sum - x_sum * y_sum) / math.sqrt(n * x_square_sum - x_sum**2) / math.sqrt(n * y_square_sum - y_sum**2)
        return correlation_coefficient
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        d = random.randint(2, min(n-1, 10))
        circuit = generate_d_regular_circuit(n, d)
        if not circuit:
            continue
        
        representation = construct_representation(circuit)
        weight = calculate_max_weight(circuit)
        
        if representation is None or weight is None:
            continue
        
        metric_values.append(weight * math.log2(len(representation)))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    correlation_coefficient = calculate_correlation(metric_values, metric_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")