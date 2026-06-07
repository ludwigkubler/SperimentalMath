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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        return [[f[i * (1 << (n - j)) + j] for j in range(n)] for i in range(2**(n-1))]
    
    def dual_vector(matrix):
        n = len(matrix)
        dual = [0] * n
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    dual[j] += (i + 1) % n
        return dual
    
    def minimal_order(dual):
        gcd = 0
        for x in dual:
            gcd = math.gcd(gcd, x)
        return gcd
    
    def communication_complexity_rank_variance(matrix):
        rank = 0
        for i in range(len(matrix)):
            if any(matrix[i][j] == 1 for j in range(len(matrix))):
                rank += 1
        return Fraction(rank * (len(matrix) - rank), len(matrix))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matrix = matrix_representation(f, n)
        dual = dual_vector(matrix)
        order = minimal_order(dual)
        variance = communication_complexity_rank_variance(matrix)
        
        results.append({
            "n": n,
            "order": order,
            "variance": variance
        })
    
    if not results:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    metric_values = [result["order"] / result["variance"] for result in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(0.5 <= x <= 1.5 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")