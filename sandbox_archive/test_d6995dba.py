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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def incidence_algebra(phi):
        n = len(phi)
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all((i & (1 << k)) == (j & (1 << k)) for k in range(n)):
                    A[i][j] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        rank = 0
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            rank += 1
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def dpll_search_tree(phi):
        n = len(phi)
        stack = [(0, 0)]
        max_height = 0
        while stack:
            i, depth = stack.pop()
            if i == n:
                max_height = max(max_height, depth)
                continue
            stack.append((i+1, depth))
            if phi[i] == 1:
                stack.append((i+1, depth+1))
        return max_height
    
    def min_order_twisted_module(A):
        rank = gaussian_elimination(A)
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = generate_sat_instance(n)
        A = incidence_algebra(phi)
        min_order = min_order_twisted_module(A)
        dpll_height = dpll_search_tree(phi)
        metric_values.append((min_order, dpll_height))
    
    if len(metric_values) < instances_tested:
        return {
            "metric_name": "MinOrder_TwistedMod vs H_DPLL",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    mean_d = sum(d for _, d in metric_values) / instances_tested
    std_d = math.sqrt(sum((d - mean_d)**2 for _, d in metric_values) / instances_tested)
    
    correlation = 0.0
    for min_order, dpll_height in metric_values:
        correlation += (min_order - mean_d) * (dpll_height - mean_d)
    correlation /= instances_tested * std_d
    
    return {
        "metric_name": "MinOrder_TwistedMod vs H_DPLL",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if abs(r["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")