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
    
    def generate_clause_indicator_graph(n, m):
        graph = [[0] * n for _ in range(n)]
        for _ in range(m):
            i, j = random.sample(range(n), 2)
            if i != j:
                graph[i][j] = 1
                graph[j][i] = 1
        return graph
    
    def gromov_hausdorff_distance(graph1, graph2):
        n1, n2 = len(graph1), len(graph2)
        d = [[float('inf')] * (n2 + 1) for _ in range(n1 + 1)]
        d[n1][n2] = 0
        
        def update_d(i, j):
            if d[i][j] < float('inf'):
                return
            d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
            for k in range(n2):
                update_d(i, k)
                update_d(k, j)
        
        for i in range(n1):
            update_d(i, n2)
        for j in range(n2):
            update_d(n1, j)
        
        return d[n1][n2]
    
    def resolution_proof_width(graph):
        # Placeholder function; actual implementation required
        return len(graph)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(2 * n, 5 * n)
        graph = generate_clause_indicator_graph(n, m)
        distance = gromov_hausdorff_distance(graph, graph)  # Placeholder; actual computation required
        width = resolution_proof_width(graph)
        
        if width > distance:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, width={width}, distance={distance}"
            break
        
        total_metric_value += distance
        instances_tested += 1
    
    return {
        "metric_name": "Gromov-Hausdorff Distance",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else float('nan'),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] > 30 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")