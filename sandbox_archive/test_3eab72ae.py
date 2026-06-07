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

def matrix_representation(f, n):
    return [[f[i * (1 << (n - j)) + j] for j in range(n)] for i in range(2**(n-1))]

def dual_vector(matrix):
    m = len(matrix)
    n = len(matrix[0])
    dual = [0] * n
    for i in range(m):
        for j in range(n):
            dual[j] += matrix[i][j]
    return dual

def minimal_order(dual):
    if not dual:
        return 0
    gcd = dual[0]
    for x in dual[1:]:
        while x != 0:
            gcd, x = x, gcd % x
    return gcd

def communication_complexity_rank_variance(matrix):
    m = len(matrix)
    n = len(matrix[0])
    rank = 0
    for i in range(m):
        if any(matrix[i][j] != 0 for j in range(n)):
            rank += 1
    variance = (n - rank) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_metric_value = 0.0
        max_n = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = [random.choice([0, 1]) for _ in range(2**n)]
            matrix = matrix_representation(f, n)
            dual = dual_vector(matrix)
            minimal_order_value = minimal_order(dual)
            variance = communication_complexity_rank_variance(matrix)
            
            if minimal_order_value == 0:
                conjecture_holds = False
                counterexample = "minimal_order_zero"
                break
            
            instances_tested += 1
            total_metric_value += minimal_order_value * variance
        
        if instances_tested < 30:
            conjecture_holds = False
            counterexample = "not_enough_instances"
        
        metric_name = "min_order_variance_product"
        metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
        n_max = max_n
        
        results.append({
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.extend(trial_result["results"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in all_results):
        first_failing_seed = next((r["seed"] for r in all_results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")