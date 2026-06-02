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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_depth(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        depth = 0
        for i in range(n):
            if circuit[i] == 1:
                depth += 1 + max(compute_depth(circuit[:i]), compute_depth(circuit[i+1:]))
        return depth
    
    def compute_mlc(circuit):
        n = len(circuit)
        mlc = 0
        for i in range(n):
            if circuit[i] == 1:
                mlc += 1 / (2 ** i)
        return mlc
    
    correlation_coefficient = None
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            depth = compute_depth(circuit)
            mlc = compute_mlc(circuit)
            
            if correlation_coefficient is None:
                correlation_coefficient = 0
                mean_mlc = 0
                mean_depth = 0
            
            correlation_coefficient += (mlc - mean_mlc) * (depth - mean_depth)
            mean_mlc += mlc
            mean_depth += depth
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    mean_mlc /= instances_tested
    mean_depth /= instances_tested
    correlation_coefficient /= (instances_tested * mean_mlc * mean_depth)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.8 <= abs(correlation_coefficient) <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8 and abs(r["metric_value"]) <= 1.2) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.8 and abs(r["metric_value"]) <= 1.2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.8 or abs(r["metric_value"]) > 1.2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8 or abs(result["metric_value"]) > 1.2)
        print(f"RESULT: FALSIFIED counterexample='out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric_values")