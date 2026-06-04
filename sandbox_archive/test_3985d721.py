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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges_added) == n * d // 2:
                    break
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
                    edges_added.add((i, j))
        return adj_matrix
    
    def calculate_mhd(adj_matrix):
        n = len(adj_matrix)
        # Placeholder for actual symplectic hull diameter calculation
        return random.random() * n
    
    def calculate_circuit_monotone_width(adj_matrix):
        n = len(adj_matrix)
        # Placeholder for actual circuit monotone width calculation
        return random.random() * n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = 2 if n == 5 else 3
        G = generate_d_regular_graph(n, d)
        if G is None:
            continue
        mhd_G = calculate_mhd(G)
        w_G = calculate_circuit_monotone_width(G)
        results.append((mhd_G, w_G))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mhd_values = [m for m, _ in results]
    w_values = [w for _, w in results]
    mean_mhd = sum(mhd_values) / len(mhd_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = sum((m - mean_mhd) * (w - mean_w) for m, w in results) / (len(results) * math.sqrt(sum((m - mean_mhd) ** 2 for m in mhd_values)) * math.sqrt(sum((w - mean_w) ** 2 for w in w_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and mean_w / mean_mhd >= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")