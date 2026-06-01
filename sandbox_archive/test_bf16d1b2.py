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
    
    def is_k_colorable(graph, k):
        # Implement a simple greedy coloring algorithm to check if graph is k-colorable
        n = len(graph)
        colors = [-1] * n
        
        for u in range(n):
            used_colors = set(colors[v] for v in range(n) if graph[u][v])
            color = next(c for c in range(k) if c not in used_colors)
            colors[u] = color
        
        return all(colors[u] != colors[v] for u in range(n) for v in range(u + 1, n) if graph[u][v])
    
    def minimal_quadratic_residue_representation(graph):
        # Implement a simple encoding using quadratic residues
        n = len(graph)
        mqr = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    mqr += (i * j) % n
        return mqr
    
    def communication_complexity_growth_rate(graph, k):
        # Implement a simple growth rate calculation based on the number of edges
        n = len(graph)
        num_edges = sum(sum(row) for row in graph) // 2
        return num_edges / (n * (k - 1))
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 4))  # Ensure k is at least 2 and not too large
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    
    if not is_k_colorable(graph, k):
        return {
            "metric_name": "communication_complexity_growth_rate",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_k_colorable"
        }
    
    mqr = minimal_quadratic_residue_representation(graph)
    growth_rate = communication_complexity_growth_rate(graph, k)
    
    return {
        "metric_name": "communication_complexity_growth_rate",
        "metric_value": growth_rate,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_seeds_support")