# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and graph[u][v] == 0:
                graph[u][v] = 1
                graph[v][u] = 1
                edges_added += 1
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        visited = [False] * n
        width = 0
        
        def dfs(u, level):
            nonlocal width
            if visited[u]:
                return
            visited[u] = True
            for v in range(n):
                if graph[u][v] == 1 and not visited[v]:
                    dfs(v, level + 1)
            width = max(width, level)
        
        for u in range(n):
            if not visited[u]:
                dfs(u, 0)
        
        return width
    
    def order_of_quotient_space(graph):
        n = len(graph)
        # Simplified model of the quotient space order
        return sum(1 for row in graph for val in row if val == 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        width = circuit_monotone_width(graph)
        order = order_of_quotient_space(graph)
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    def pearsons_correlation(x, y):
        if not x or not y:
            return 0.0
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_dev_x = (sum((xi - mean_x) ** 2 for xi in x) / len(x)) ** 0.5
        std_dev_y = (sum((yi - mean_y) ** 2 for yi in y) / len(y)) ** 0.5
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation_coefficient = pearsons_correlation([r[0] for r in results], [r[1] for r in results])
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "Pearson's correlation coefficient < 0.5"
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Pearson's correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient support")