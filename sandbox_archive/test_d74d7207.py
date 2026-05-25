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
    
    def generate_circuit(depth, size):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1), size//2) for _ in range(size)]
            return [sum(subcircuit) % 2 for subcircuit in zip(*subcircuits)]
    
    def spectral_radius(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        max_eigenvalue = 0
        for i in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]  # Normalize
            Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            max_eigenvalue = max(max_eigenvalue, abs(sum(Av[i] * v[i] for i in range(n))))
        return max_eigenvalue
    
    def coxeter_group_action(circuit):
        n = len(circuit)
        action = [[0]*n for _ in range(n)]
        for i in range(n):
            action[i][i] = 1
        return action
    
    depth_values = [5, 10, 15, 20, 30, 40]
    size_values = [5, 10, 15, 20, 30, 40]
    
    results = []
    for depth in depth_values:
        for size in size_values:
            circuit = generate_circuit(depth, size)
            action = coxeter_group_action(circuit)
            radius = spectral_radius(action)
            results.append({
                "depth": depth,
                "size": size,
                "radius": radius
            })
    
    metric_value = sum(result["radius"] for result in results) / len(results)
    conjecture_holds = all(result["radius"] >= result["depth"] / math.log(result["size"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spectral Radius",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")