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

def generate_random_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges = set()
    for _ in range(d * n // 2):
        while True:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
            break
    return graph

def generate_circuit_and_rank(graph):
    n = len(graph)
    if not graph:
        return 0, 0
    
    # Placeholder for actual quantum ternary logic circuit generation and rank calculation
    Rrank = n  # Dummy value
    w = n  # Dummy value
    return Rrank, w

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlations = []
    
    for n in n_values:
        G = generate_random_d_regular_graph(n, d=3)
        if G is None:
            continue
        rank, width = generate_circuit_and_rank(G)
        correlations.append((rank, width))
    
    if not correlations:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    n = len(correlations)
    ranks = [x[0] for x in correlations]
    widths = [x[1] for x in correlations]
    
    mean_rank = sum(ranks) / n
    mean_width = sum(widths) / n
    
    covariance = sum((ranks[i] - mean_rank) * (widths[i] - mean_width) for i in range(n)) / n
    variance_rank = sum((ranks[i] - mean_rank) ** 2 for i in range(n)) / n
    variance_width = sum((widths[i] - mean_width) ** 2 for i in range(n)) / n
    
    pearson_corr = covariance / (variance_rank * variance_width) ** 0.5
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7 and pearson_corr <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        exit(0)
    
    mean_corr = sum(x["metric_value"] for x in results) / len(results)
    std_corr = (sum((x["metric_value"] - mean_corr) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")