# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_circuit(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def affine_scheme(circuit):
    n = len(circuit)
    scheme = []
    for i in range(2**n):
        if all(circuit[j] == circuit[i ^ j] for j in range(n)):
            scheme.append(i)
    return scheme

def symplectic_volume(scheme):
    n = int(math.log2(len(scheme)))
    volume = 0
    for i in range(n):
        count = sum(1 for x in scheme if (x >> i) & 1 == 1)
        volume += count * (len(scheme) - count)
    return volume

def monotone_complexity(circuit):
    n = len(circuit)
    complexity = 0
    for i in range(n):
        if circuit[i] == 1:
            complexity += sum(1 for j in range(i+1, n) if circuit[j] == 1 and (i & j) == i)
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_circuit(n)
        scheme = affine_scheme(circuit)
        volume = symplectic_volume(scheme)
        complexity = monotone_complexity(circuit)
        results.append((volume, complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n = len(results)
    mean_volume = sum(v for v, _ in results) / n
    mean_complexity = sum(c for _, c in results) / n
    
    covariance = sum((v - mean_volume) * (c - mean_complexity) for v, c in results) / n
    variance_volume = sum((v - mean_volume)**2 for v, _ in results) / n
    variance_complexity = sum((c - mean_complexity)**2 for _, c in results) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_volume) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")