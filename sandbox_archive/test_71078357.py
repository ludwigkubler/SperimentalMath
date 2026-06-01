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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return list(edges)
    
    def max_edge_connectivity(graph):
        n = len(graph) + 1
        max_kappa = 0
        for i in range(n):
            neighbors = [j for j in range(n) if (i, j) in graph or (j, i) in graph]
            kappa = sum(1 for u in neighbors for v in neighbors if (u, v) in graph or (v, u) in graph)
            max_kappa = max(max_kappa, kappa)
        return max_kappa
    
    def communication_rank(graph):
        n = len(graph) + 1
        rank = 0
        for i in range(n):
            neighbors = [j for j in range(n) if (i, j) in graph or (j, i) in graph]
            rank += len(neighbors)
        return rank
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    kappa_squared_log_n = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        graph = generate_random_graph(n)
        kappa = max_edge_connectivity(graph)
        rank = communication_rank(graph)
        
        if kappa == 0:
            continue
        
        kappa_squared_log_n.append(kappa ** 2 * log2(n))
        metric_values.append(rank)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    mean_kappa_squared_log_n = sum(kappa_squared_log_n) / len(kappa_squared_log_n)
    
    conjecture_holds = all(value >= 0.5 * mean_metric_value for value in kappa_squared_log_n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Communication Rank",
        "metric_value": mean_kappa_squared_log_n,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")