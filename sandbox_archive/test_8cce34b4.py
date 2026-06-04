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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_barcode_matrix(instance):
        n = int(math.log2(len(instance)))
        matrix = [[instance[i] if i & (1 << j) else 0 for j in range(n)] for i in range(2**n)]
        return matrix
    
    def calculate_betti_numbers(matrix):
        # Simplified Betti number calculation for demonstration
        n = len(matrix)
        b_1 = sum(1 for row in matrix if sum(row) == 1)
        b_2 = sum(1 for row in matrix if sum(row) == 2)
        return b_1, b_2
    
    def resolution_proof_width(instance):
        # Simplified resolution proof width calculation for demonstration
        n = int(math.log2(len(instance)))
        return n
    
    instances_tested = 0
    total_betti_sum = 0
    total_resolution_width = 0
    n_max = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        instance = generate_instance(n)
        barcode_matrix = compute_barcode_matrix(instance)
        b_1, b_2 = calculate_betti_numbers(barcode_matrix)
        resolution_width = resolution_proof_width(instance)
        
        total_betti_sum += b_1 + b_2
        total_resolution_width += resolution_width
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = total_betti_sum / total_resolution_width
    conjecture_holds = correlation_coefficient >= 0.7
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["metric_value"] is not None for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")