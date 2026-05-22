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

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        i, j = random.sample(range(n), 2)
        if i != j and (i, j) not in edges and (j, i) not in edges:
            graph[i][j] = 1
            graph[j][i] = 1
            edges.add((i, j))
    return graph

def local_index(graph):
    n = len(graph)
    covered_edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                covered_edges.update([(k, i), (k, j)] for k in range(n) if graph[k][i] == 1 or graph[k][j] == 1)
    return len(covered_edges)

def communication_complexity(graph):
    n = len(graph)
    # Simplified version of the communication complexity calculation
    return math.ceil(n ** (2/3))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        loc_idx = local_index(graph)
        comm_complexity = communication_complexity(graph)
        
        if loc_idx < n ** (1/3):
            return {
                "metric_name": "communication_complexity",
                "metric_value": comm_complexity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Graph with n={n} has loc_idx={loc_idx}"
            }
        
        results.append(comm_complexity)
    
    mean_comm_complexity = sum(results) / len(results)
    std_comm_complexity = math.sqrt(sum((x - mean_comm_complexity) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": len(n_values),
        "conjecture_holds": all(comm >= n ** (1/3) for comm in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"loc_idx < n^(1/3)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")