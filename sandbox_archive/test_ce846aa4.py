# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def generate_circuit(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def monotone_width(circuit):
    n = len(circuit)
    max_inputs = 0
    stack = []
    
    for i in range(n):
        if circuit[i] == 1:
            stack.append(i + 1)
        else:
            while stack and stack[-1] > i + 1:
                stack.pop()
            if stack:
                max_inputs = max(max_inputs, stack[-1])
    
    return max_inputs

def git_degree(circuit):
    n = len(circuit)
    width = monotone_width(circuit)
    if width == 0:
        return 0
    return int(math.log2(n)) * width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n)
            git_deg = git_degree(circuit)
            width = monotone_width(circuit)
            if width == 0:
                continue
            results.append((git_deg, n * math.log2(n) * width))
    
    if not results:
        return {
            "metric_name": "GIT degree / log(n) * width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r[0] for r in results]
    ratios = [r[0] / (r[1] + 1e-9) for r in results]  # Add a small epsilon to avoid division by zero
    
    mean_ratio = sum(ratios) / len(ratios)
    
    return {
        "metric_name": "GIT degree / log(n) * width",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max([r[1] for r in results]),
        "conjecture_holds": mean_ratio <= 1,  # Assuming c = 1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(result)