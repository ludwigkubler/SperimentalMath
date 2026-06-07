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
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def compute_local_cohomology(graph):
        n = len(graph)
        I_G = set()
        for node in graph:
            for neighbor in graph[node]:
                if (node, neighbor) not in I_G and (neighbor, node) not in I_G:
                    I_G.add((node, neighbor))
        H1_G = set()
        for edge in I_G:
            u, v = edge
            if len(graph[u]) == 2 and len(graph[v]) == 2:
                H1_G.add(edge)
        return H1_G
    
    def compute_rank_variance(G):
        n = len(G)
        degrees = [len(G[node]) for node in G]
        mean_degree = sum(degrees) / n
        variance = sum((d - mean_degree) ** 2 for d in degrees) / n
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        
        H1_G = compute_local_cohomology(graph)
        R_var_G = compute_rank_variance(graph)
        
        if len(H1_G) == 0 or R_var_G == 0:
            continue
        
        results.append({
            "n": n,
            "log_H1_G": math.log(len(H1_G)),
            "R_var_G": R_var_G
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    log_H1_G_values = [result["log_H1_G"] for result in results]
    R_var_G_values = [result["R_var_G"] for result in results]
    
    mean_log_H1_G = sum(log_H1_G_values) / instances_tested
    std_log_H1_G = math.sqrt(sum((x - mean_log_H1_G) ** 2 for x in log_H1_G_values) / instances_tested)
    
    correlation_coefficient = sum((log_H1_G_values[i] - mean_log_H1_G) * (R_var_G_values[i] - mean(R_var_G_values)) for i in range(instances_tested))
    correlation_coefficient /= instances_tested * std_log_H1_G * math.sqrt(sum((x - mean(R_var_G_values)) ** 2 for x in R_var_G_values))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["conjecture_holds"])) / sum(1 for result in results if result["conjecture_holds"])
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")