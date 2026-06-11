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
        if (n * d) % 2 != 0 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and adj_matrix[u][v] == 0:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
                edges_added += 1
        return adj_matrix
    
    def coset_enumeration(adj_matrix):
        n = len(adj_matrix)
        group = []
        for i in range(n):
            group.append(i)
        for j in range(1, n):
            if all(all(adj_matrix[i][k] == adj_matrix[j][i] for k in range(n)) for i in range(n)):
                group.append(j)
        return len(group)
    
    def communication_complexity_rank_variance(adj_matrix):
        n = len(adj_matrix)
        rank_var = 0
        for i in range(n):
            row_sum = sum(adj_matrix[i])
            if row_sum > 0:
                rank_var += (row_sum / n) ** 2
        return rank_var
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, mean_val):
        return math.sqrt(sum((x - mean_val) ** 2 for x in lst) / len(lst))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = (n * (n - 1)) // 2
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        aut_group_size = coset_enumeration(graph)
        rank_var = communication_complexity_rank_variance(graph)
        results.append((aut_group_size, rank_var))
    
    if not results:
        return {
            "metric_name": "Aut(G) vs r(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    aut_group_sizes, rank_vars = zip(*results)
    mean_aut_group_size = mean(aut_group_sizes)
    mean_rank_var = mean(rank_vars)
    std_aut_group_size = std(aut_group_sizes, mean_aut_group_size)
    std_rank_var = std(rank_vars, mean_rank_var)
    
    correlation_coefficient = sum((a - mean_aut_group_size) * (b - mean_rank_var) for a, b in zip(aut_group_sizes, rank_vars)) / (len(results) * std_aut_group_size * std_rank_var)
    
    return {
        "metric_name": "Aut(G) vs r(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 2 * math.log(len(results)) ** 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = mean([result["metric_value"] for result in results])
        std_value = std([result["metric_value"] for result in results], mean_value)
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")