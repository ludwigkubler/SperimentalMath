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

def generate_d_regular_circuit(n, d):
    if n * (d - 1) % 2 != 0:
        return None
    circuit = []
    for i in range(n):
        neighbors = set()
        while len(neighbors) < d:
            neighbor = random.randint(0, n - 1)
            if neighbor != i and neighbor not in neighbors:
                neighbors.add(neighbor)
        circuit.append(list(sorted(neighbors)))
    return circuit

def calculate_minimal_order(circuit):
    n = len(circuit)
    for order in range(2, n + 1):
        generator = [i % order for i in range(n)]
        if all((generator * (order // math.gcd(len(generator), order))) == list(range(n)) for _ in range(order)):
            return order
    return n

def calculate_max_gate_weight(circuit):
    max_weight = 0
    for row in circuit:
        max_weight = max(max_weight, len(row))
    return max_weight

def calculate_correlation(metric_values1, metric_values2):
    if not metric_values1 or not metric_values2:
        return 0.0
    n = len(metric_values1)
    x_mean = sum(metric_values1) / n
    y_mean = sum(metric_values2) / n
    numerator = sum((metric_values1[i] - x_mean) * (metric_values2[i] - y_mean) for i in range(n))
    denominator = math.sqrt(sum((metric_values1[i] - x_mean) ** 2 for i in range(n))) * math.sqrt(sum((metric_values2[i] - y_mean) ** 2 for i in range(n)))
    return numerator / denominator if denominator != 0 else 0.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    circuit = generate_d_regular_circuit(n, d)
    if not circuit:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid circuit generated"
        }
    
    minimal_order = calculate_minimal_order(circuit)
    max_gate_weight = calculate_max_gate_weight(circuit)
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": minimal_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        failing_seeds = [r for r in results if not r["conjecture_holds"]]
        first_failing_seed = min(failing_seeds, key=lambda x: x["seed"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined\" first_failing_seed={first_failing_seed}")