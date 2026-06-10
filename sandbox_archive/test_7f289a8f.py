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
        I = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all(phi[i >> k & 1] == phi[j >> k & 1] for k in range(n)):
                    I[i][j] = 1
        return I
    
    def min_twisted_module_order(I):
        n = len(I)
        order = float('inf')
        for i in range(2**n):
            if all(I[i][j] == 0 or I[j][i] == 0 for j in range(n)):
                order = min(order, sum(I[i][j] * I[j][k] * I[k][i] for j, k in itertools.combinations(range(n), 2)))
        return order
    
    def dpll_search_tree_height(phi):
        n = len(phi)
        stack = [(0, 0)]
        max_height = 0
        while stack:
            node, depth = stack.pop()
            if node == (1 << n) - 1:
                max_height = max(max_height, depth)
            else:
                for i in range(n):
                    if phi[node >> i & 1] == 0:
                        stack.append((node | (1 << i), depth + 1))
        return max_height
    
    def pearson_correlation(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        cov = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n)) / n
        var1 = sum((values1[i] - mean1)**2 for i in range(n)) / n
        var2 = sum((values2[i] - mean2)**2 for i in range(n)) / n
        return cov / math.sqrt(var1 * var2)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_sat_instance(n)
        I = incidence_algebra(phi)
        min_order = min_twisted_module_order(I)
        height = dpll_search_tree_height(phi)
        results.append((min_order, height))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    min_orders, heights = zip(*results)
    correlation = pearson_correlation(min_orders, heights)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": "" if abs(correlation) >= 0.8 else f"r={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(abs(r["metric_value"]) < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"|r| < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_samples")