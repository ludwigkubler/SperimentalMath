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
    
    def generate_d_regular_circuit(d, D):
        if d <= 1 or D < 2:
            return None
        n = 2 * (d - 1) * D
        circuit = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d - 1) == 0:
                    circuit[i].append(j)
                    circuit[j].append(i)
        return circuit
    
    def construct_tropical_graph(circuit):
        graph = {}
        for node, neighbors in enumerate(circuit):
            for neighbor in neighbors:
                if (node, neighbor) not in graph and (neighbor, node) not in graph:
                    graph[(node, neighbor)] = 1
        return graph
    
    def min_representation_size(graph):
        visited = [False] * len(graph)
        size = 0
        
        def dfs(node):
            nonlocal size
            if visited[node]:
                return
            visited[node] = True
            for neighbor in graph:
                if node in neighbor and not visited[neighbor]:
                    dfs(neighbor)
            size += 1
        
        for node in range(len(graph)):
            if not visited[node]:
                dfs(node)
        
        return size
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    d_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for d in d_values:
        D = int(math.log(d, 2)) + 1
        circuit = generate_d_regular_circuit(d, D)
        if circuit is None:
            continue
        
        graph = construct_tropical_graph(circuit)
        size = min_representation_size(graph)
        
        results.append((D, size))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": -1,
            "instances_tested": len(results),
            "n_max": max(d for d, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    D_values = [d for d, _ in results]
    size_values = [size for _, size in results]
    corr_coeff = correlation_coefficient(D_values, size_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(d for d, _ in results),
        "conjecture_holds": corr_coeff >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / sum(1 for r in results if r["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["instances_tested"] >= 30 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")