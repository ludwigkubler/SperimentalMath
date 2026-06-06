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
    
    def generate_bipartite_graph(n):
        A = [random.choice([0, 1]) for _ in range(n * n // 2)]
        B = [random.choice([0, 1]) for _ in range(n * n // 2)]
        return A, B
    
    def frobenius_representation_count(adj_matrix):
        n = len(adj_matrix)
        count = 0
        visited = set()
        
        def dfs(v):
            stack = [v]
            while stack:
                u = stack.pop()
                if u not in visited:
                    visited.add(u)
                    for v in range(n):
                        if adj_matrix[u][v] == 1 and v not in visited:
                            stack.append(v)
        
        for i in range(n):
            if i not in visited:
                dfs(i)
                count += 1
        
        return count
    
    def communication_complexity_rank_variance(adj_matrix):
        n = len(adj_matrix)
        rank = 0
        for i in range(n):
            row_sum = sum(adj_matrix[i])
            col_sum = sum(row[j] for row in adj_matrix)
            if row_sum > 0 and col_sum > 0:
                rank += 1
        
        return Fraction(rank, n) * (1 - Fraction(rank, n))
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        A, B = generate_bipartite_graph(n)
        adj_matrix = [[A[i * n + j] if i < n // 2 else B[(i - n // 2) * n + j] for j in range(n)] for i in range(n)]
        frobenius_count = frobenius_representation_count(adj_matrix)
        comm_rank_var = communication_complexity_rank_variance(adj_matrix)
        
        results.append({
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient([frobenius_count], [comm_rank_var]),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "metric_name": "correlation_coefficient",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(abs(r["metric_value"]) >= 0.95 and abs(r["metric_value"]) <= 1.05 for r in results),
        "counterexample": ""
    }

def std_dev(data, mean):
    return math.sqrt(sum((x - mean) ** 2 for x in data) / len(data))

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [673, 701, 739, 767, 797, 827, 857, 887, 911, 941, 971, 1009, 1031, 1061, 1091, 1123, 1151, 1181, 1213, 1249, 1277, 1301, 1327, 1361, 1399, 1427, 1451, 1481, 1511, 1543, 1571, 1597]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = std_dev([r["metric_value"] for r in results], mean_metric_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not enough data\" first_failing_seed={first_failing_seed}")