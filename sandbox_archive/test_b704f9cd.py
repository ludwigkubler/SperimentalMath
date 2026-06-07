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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def gromov_wasserstein_distance(instance, n):
        points = [[i / (2**n - 1) for i in range(2**n)]]
        weights = [sum(abs(instance[i] - instance[j]) for j in range(2**n)) for i in range(2**n)]
        return sum(weights[i] * weights[j] for i, j in itertools.combinations(range(2**n), 2))
    
    def dpll_path_length(n):
        # Simplified DPLL solver to estimate path length
        instance = generate_instance(n)
        stack = [(0, [])]
        while stack:
            pos, assignment = stack.pop()
            if pos == n:
                return len(assignment)
            if instance[pos] == 1:
                stack.append((pos + 1, assignment + [1]))
            else:
                stack.append((pos + 1, assignment + [0]))
        return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    gw_distances = []
    dpll_lengths = []
    
    for n in n_values:
        instance = generate_instance(n)
        gw_dist = gromov_wasserstein_distance(instance, n)
        if gw_dist > 10:
            return {
                "metric_name": "GW_dist",
                "metric_value": gw_dist,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "GW_dist too large"
            }
        gw_distances.append(gw_dist)
        dpll_lengths.append(dpll_path_length(n))
    
    if not gw_distances or not dpll_lengths:
        return {
            "metric_name": "GW_dist",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "Empty results"
        }
    
    mean_gw = sum(gw_distances) / len(gw_distances)
    mean_dpll = sum(dpll_lengths) / len(dpll_lengths)
    
    return {
        "metric_name": "GW_dist",
        "metric_value": mean_gw,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='{', '.join(counterexamples)}' first_failing_seed={first_failing_seed}")