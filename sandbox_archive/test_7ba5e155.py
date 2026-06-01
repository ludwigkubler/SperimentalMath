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
        return [random.choice(['0', '1']) for _ in range(2**n)]
    
    def monotone_complexity(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        complexity = 0
        for i in range(n):
            sub_circuit = circuit[:i] + ['1'] + circuit[i+1:]
            if all(sub_circuit[j] == '1' or sub_circuit[j] == circuit[j] for j in range(i)):
                complexity += 1
        return complexity
    
    def symplectic_volume(circuit):
        n = len(circuit)
        volume = 0
        for i in range(n):
            if all(circuit[j] == '1' or circuit[j] == circuit[i] for j in range(i)):
                volume += 1
        return volume
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_circuit(n)
        min_vol = symplectic_volume(circuit)
        w_M = monotone_complexity(circuit)
        results.append((min_vol, w_M))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    x_mean = sum(x for x, _ in results) / n
    y_mean = sum(y for _, y in results) / n
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in results)
    denominator = math.sqrt(sum((x - x_mean)**2 for x, _ in results)) * math.sqrt(sum((y - y_mean)**2 for _, y in results))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": 0.0,
            "instances_tested": n,
            "n_max": max(n),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(n),
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")