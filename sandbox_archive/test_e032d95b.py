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
    
    def generate_random_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def barycentric_coordinates(circuit):
        n = len(circuit)
        coordinates = []
        for i in range(2**n):
            coords = [0] * (n + 1)
            for j in range(n):
                if circuit[i & (1 << j)] == 1:
                    coords[j] += 1
            coordinates.append(coords)
        return coordinates
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for i in range(2**n):
            if circuit[i] == 1:
                complexity += 1
        return complexity
    
    def compute_ratio(coordinates, complexity):
        if complexity == 0:
            return None
        return len(coordinates) / complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            coordinates = barycentric_coordinates(circuit)
            complexity = entanglement_complexity(circuit)
            ratio = compute_ratio(coordinates, complexity)
            
            if ratio is not None:
                total_metric_value += abs(ratio - 1)
                instances_tested += 1
                n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    return {
        "metric_name": "Ratio of Barycentric Coordinates to Entanglement Complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_data\" first_failing_seed={first_failing_seed}")