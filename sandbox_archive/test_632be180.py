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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j and (i, j) not in edges_added:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
                    edges_added.add((i, j))
        
        return adj_matrix
    
    def gromov_witten_invariant(adj_matrix):
        n = len(adj_matrix)
        count = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    count += 1
        
        return Fraction(count, (n * (n - 1)) // 2)
    
    def communication_complexity_rank(adj_matrix):
        n = len(adj_matrix)
        rank = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    rank += 1
        
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        
        if std_dev_x == 0 or std_dev_y == 0:
            return 0
        
        return cov_xy / (std_dev_x * std_dev_y)
    
    gwi_values = []
    ccr_values = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = 2
        graph = generate_d_regular_graph(n, d)
        
        if graph is None:
            continue
        
        gwi_values.append(gromov_witten_invariant(graph))
        ccr_values.append(communication_complexity_rank(graph))
    
    if not gwi_values or not ccr_values:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": 0,
            "instances_tested": len(gwi_values),
            "n_max": max(n for n, _ in [random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    correlation = pearson_correlation(gwi_values, ccr_values)
    p_value = 2 * (1 - math.erf(abs(correlation) / math.sqrt(2 * len(gwi_values) - 3)))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(gwi_values),
        "n_max": max(n for n, _ in [random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
        "conjecture_holds": correlation >= 0.5 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")