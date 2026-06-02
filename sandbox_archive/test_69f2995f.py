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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        n = len(phi)
        rank = 0
        for i in range(n):
            if all(phi[j] == phi[j + 2**i] for j in range(2**(n - i) - 1)):
                rank += 1
        return rank
    
    def twistor_space_order(phi):
        n = len(phi)
        order = 0
        for i in range(n):
            if all(phi[j] == phi[j + 2**i] for j in range(2**(n - i) - 1)):
                order += 1
        return order
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        c_phi = communication_complexity_rank(phi)
        order_twistor_space = twistor_space_order(phi)
        results.append((order_twistor_space, c_phi))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    x, y = zip(*results)
    correlation = pearson_correlation(x, y)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(len(phi) for phi, _ in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results if r["metric_value"] is not None) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        counterexample = next(r["counterexample"] for r in all_results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")