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
    
    def generate_geometric_circuit(n):
        G = [set(range(1, n+1)) for _ in range(n)]
        for i in range(n):
            G[i].remove(i+1)
        return G
    
    def incidence_algebra(G):
        n = len(G)
        A_G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    A_G[i][j] = sum(len(set(G[k]) & set(G[l])) for k in range(n) if k != i and k != j)
        return A_G
    
    def minimal_index(A_G):
        n = len(A_G)
        min_index = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                min_index = min(min_index, abs(A_G[i][j]))
        return min_index
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            rank += max(len(set(G[k]) & set(G[l])) for k in range(n) if k != i and k not in G[i])
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        G = generate_geometric_circuit(n)
        A_G = incidence_algebra(G)
        i_G = minimal_index(A_G)
        r_G = communication_complexity_rank(G)
        results.append({"n": n, "i_G": i_G, "r_G": r_G})
    
    if not results:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    i_G_values = [result["i_G"] for result in results]
    r_G_values = [result["r_G"] for result in results]
    
    mean_i_G = sum(i_G_values) / len(i_G_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    
    if len(results) < 30:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) * sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else float('nan')
    
    corr_coefficient = pearson_correlation(i_G_values, r_G_values)
    
    return {
        "metric_name": "minimal_index",
        "metric_value": corr_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(corr_coefficient) >= 0.7 and math.isnan(corr_coefficient) == False,
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
    
    mean_corr_coefficient = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coefficient} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coefficient} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")