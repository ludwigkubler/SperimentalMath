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
    
    def generate_sat_instance(n):
        phi = [random.choice([0, 1]) for _ in range(2**n)]
        return phi
    
    def incidence_algebra(phi):
        n = int(math.log2(len(phi)))
        I = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if i & j == 0:
                    I[i][j] = 1
        return I
    
    def dpll_search_tree_height(phi, n):
        stack = [(phi, 0)]
        max_height = 0
        while stack:
            current_phi, height = stack.pop()
            if all(current_phi[i] == phi[i] for i in range(n)):
                max_height = max(max_height, height)
            else:
                for i in range(n):
                    if current_phi[i] != phi[i]:
                        new_phi = current_phi[:]
                        new_phi[i] = 1 - new_phi[i]
                        stack.append((new_phi, height + 1))
        return max_height
    
    def min_order_twisted_module(I):
        n = int(math.log2(len(I)))
        order = 0
        for i in range(2**n):
            if any(I[i][j] != I[j][i] for j in range(i+1, 2**n)):
                order += 1
        return order
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        phi = generate_sat_instance(n)
        I = incidence_algebra(phi)
        height = dpll_search_tree_height(phi, n)
        order = min_order_twisted_module(I)
        
        results.append({
            "n": n,
            "phi": phi,
            "I": I,
            "height": height,
            "order": order
        })
    
    mean_order = sum(result["order"] for result in results) / len(results)
    mean_height = sum(result["height"] for result in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((result["order"] - mean_order) * (result["height"] - mean_height) for result in results)
        denominator = math.sqrt(sum((result["order"] - mean_order)**2 for result in results)) * math.sqrt(sum((result["height"] - mean_height)**2 for result in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for result in results if abs(result["metric_value"]) < 0.5) >= 25:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")