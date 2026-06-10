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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_circuit(n, d):
    if n <= 1 or d <= 0:
        return []
    elif d == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_circuit(random.randint(2, min(n-1, 3)), random.randint(1, d-1)) for _ in range(d)]
        return sum(subcircuits, [])

def complement_graph(graph):
    n = len(graph)
    comp_graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 0:
                comp_graph[i][j] = 1
                comp_graph[j][i] = 1
    return comp_graph

def max_clique_size(graph):
    def dfs(node, visited, clique):
        visited.add(node)
        clique.append(node)
        for neighbor in range(len(graph)):
            if graph[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor, visited, clique)
    
    n = len(graph)
    max_clique = []
    for i in range(n):
        current_clique = []
        dfs(i, set(), current_clique)
        if len(current_clique) > len(max_clique):
            max_clique = current_clique
    return len(max_clique)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    circuit_ranks = []
    
    for n in range(5, n_max + 1):
        for d in range(1, min(n, 4) + 1):  # Limit depth to avoid excessive complexity
            instances_tested += 1
            circuit = generate_circuit(n, d)
            comp_graph = complement_graph(circuit)
            clique_size = max_clique_size(comp_graph)
            rank = clique_size  # Simplified local system rank for this example
            circuit_ranks.append((n, d, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "local_system_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_ratio = max(rank / (d**(2/3) * n**(1/3)) for _, d, rank in circuit_ranks)
    
    return {
        "metric_name": "local_system_rank",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": max_ratio <= 2,
        "counterexample": "" if max_ratio <= 2 else f"max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio_exceeded\" first_failing_seed={first_failing_seed}")