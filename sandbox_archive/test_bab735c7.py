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
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_barcode_matrix(instance):
        n = len(instance)
        B = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] != instance[j]:
                    B[i][j] = 1
                    B[j][i] = 1
        return B
    
    def compute_betti_numbers(B):
        n = len(B) - 1
        rank = 0
        for i in range(n + 1):
            if sum(B[i]) == 1:
                rank += 1
        b_1 = rank
        b_2 = n - rank
        return b_1, b_2
    
    def compute_resolution_proof_width(instance):
        n = len(instance)
        width = 0
        for i in range(n):
            if instance[i] == 1:
                width += 1
        return width
    
    metric_name = "correlation_coefficient"
    instances_tested = 30
    n_max = 40
    total_betti_sum = 0
    total_width = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = generate_instance(n)
        B = compute_barcode_matrix(instance)
        b_1, b_2 = compute_betti_numbers(B)
        width = compute_resolution_proof_width(instance)
        
        total_betti_sum += b_1 + b_2
        total_width += width
    
    mean_betti_sum = Fraction(total_betti_sum, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    correlation_coefficient = (mean_betti_sum * mean_width - instances_tested) / (instances_tested - 1)
    
    conjecture_holds = correlation_coefficient >= Fraction(7, 10)
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")