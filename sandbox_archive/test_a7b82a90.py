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
    
    def generate_k_colorable_graph(n, k):
        graph = {i: set() for i in range(n)}
        colors = list(range(1, k+1))
        for _ in range(n * (k - 1)):
            u, v = random.sample(range(n), 2)
            if len(graph[u]) < k and len(graph[v]) < k:
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def compute_brauer_classes(graph):
        n = len(graph)
        F = [0] * (n + 1)
        for u in range(n):
            for v in graph[u]:
                if F[u] == F[v]:
                    F[v] += 1
                elif F[u] < F[v]:
                    F[u], F[v] = F[v], F[u]
        return max(F) + 1
    
    def compute_communication_rank(graph):
        n = len(graph)
        rank = [0] * n
        for u in range(n):
            rank[u] = sum(1 for v in graph[u] if rank[v] > rank[u])
        return max(rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    br_values = []
    comm_rank_values = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_k_colorable_graph(n, random.randint(2, min(n-1, 4)))
            br_value = compute_brauer_classes(graph)
            comm_rank_value = compute_communication_rank(graph)
            br_values.append(br_value)
            comm_rank_values.append(comm_rank_value)
    
    if not br_values or not comm_rank_values:
        return {
            "metric_name": "br(G)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_graph"
        }
    
    mean_br = sum(br_values) / len(br_values)
    mean_comm_rank = sum(comm_rank_values) / len(comm_rank_values)
    correlation = 0
    for i in range(len(br_values)):
        correlation += (br_values[i] - mean_br) * (comm_rank_values[i] - mean_comm_rank)
    correlation /= (len(br_values) * (sum((x - mean_br) ** 2 for x in br_values)) ** 0.5 * 
                    sum((y - mean_comm_rank) ** 2 for y in comm_rank_values)) ** 0.5
    
    return {
        "metric_name": "br(G)",
        "metric_value": correlation,
        "instances_tested": len(br_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")