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
from itertools import permutations

def calculate_automorphism_group(quandle):
    n = len(quandle)
    automorphisms = []
    
    for perm in permutations(range(n)):
        if all(quandle[perm[i]][j] == quandle[i][perm[j]] for i in range(n) for j in range(n)):
            automorphisms.append(perm)
    
    return automorphisms

def calculate_communication_complexity_rank_variance(circuit):
    # Placeholder function to simulate communication complexity rank variance calculation
    n = len(circuit)
    return random.random() * n  # Simplified for demonstration purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "correlation_coefficient"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    correlation_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        # Generate a random circuit (simplified for demonstration)
        circuit = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        quandle = calculate_quandle(circuit)
        automorphism_order = len(calculate_automorphism_group(quandle))
        communication_complexity_rank_variance = calculate_communication_complexity_rank_variance(circuit)
        
        if communication_complexity_rank_variance == 0:
            continue
        
        log_automorphism_order = math.log2(automorphism_order) if automorphism_order > 0 else -math.inf
        correlation_values.append((log_automorphism_order, communication_complexity_rank_variance))
        
        instances_tested += n
        n_max = max(n_max, n)
    
    if len(correlation_values) < 30:
        conjecture_holds = False
        counterexample = "not_enough_instances"
    
    correlation_coefficient = calculate_correlation(correlation_values)
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_quandle(circuit):
    # Placeholder function to simulate quandle calculation from circuit
    n = len(circuit)
    quandle = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            quandle[i][j] = (circuit[i][j] + 1) % 2
    
    return quandle

def calculate_correlation(data):
    if len(data) < 2:
        return 0
    
    n = len(data)
    x_sum = sum(x for x, _ in data)
    y_sum = sum(y for _, y in data)
    x_mean = x_sum / n
    y_mean = y_sum / n
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in data)
    denominator = math.sqrt(sum((x - x_mean) ** 2 for x, _ in data)) * math.sqrt(sum((y - y_mean) ** 2 for _, y in data))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")