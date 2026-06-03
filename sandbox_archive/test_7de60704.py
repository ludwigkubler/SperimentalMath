# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_monoidal_category(n):
        # Generate a simple monoidal category with n objects and some morphisms
        objects = list(range(n))
        morphisms = {}
        for i in range(n):
            for j in range(n):
                morphisms[(i, j)] = random.randint(1, 5)
        return objects, morphisms
    
    def calculate_local_indeterminacy(morphisms):
        # Placeholder for local indeterminacy calculation
        total_morphisms = sum(morphisms.values())
        unique_morphisms = len(set(morphisms.values()))
        return Fraction(unique_morphisms, total_morphisms)
    
    def calculate_communication_complexity_rank(morphisms):
        # Placeholder for communication complexity rank calculation
        max_out_degree = 0
        for obj in range(len(morphisms)):
            out_degree = sum(1 for _, j in morphisms if j == obj)
            if out_degree > max_out_degree:
                max_out_degree = out_degree
        return max_out_degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    local_indet_values = []
    comm_complexity_rank_values = []
    
    for n in n_values:
        objects, morphisms = generate_random_monoidal_category(n)
        local_indet = calculate_local_indeterminacy(morphisms)
        comm_complexity_rank = calculate_communication_complexity_rank(morphisms)
        
        local_indet_values.append(local_indet)
        comm_complexity_rank_values.append(comm_complexity_rank)
    
    if not local_indet_values or not comm_complexity_rank_values:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = ((sum((xi - mean_x) ** 2 for xi in x)) * (sum((yi - mean_y) ** 2 for yi in y))) ** 0.5
        return numerator / denominator if denominator != 0 else 0
    
    correlation = pearson_correlation(local_indet_values, comm_complexity_rank_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")