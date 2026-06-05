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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for u in range(n):
            for v in range(u + 1, n):
                if len(graph[u]) < d and len(graph[v]) < d and (u, v) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    edges_added.add((v, u))
        return graph
    
    def communication_protocol(graph):
        n = len(graph)
        protocol = [0] * n
        for i in range(n):
            protocol[i] = sum(1 for j in graph[i])
        return protocol
    
    def mqr(protocol):
        n = len(protocol)
        min_order = float('inf')
        for i in range(n):
            order = 1
            while True:
                if all((protocol[j] + order * (i - j)) % n == 0 for j in range(n)):
                    break
                order += 1
            min_order = min(min_order, order)
        return min_order
    
    def communication_complexity_rank(protocol):
        n = len(protocol)
        rank = 0
        for i in range(n):
            rank = max(rank, protocol[i])
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            protocol = communication_protocol(graph)
            mqr_val = mqr(protocol)
            r_val = communication_complexity_rank(protocol)
            results.append((mqr_val, r_val))
    
    if not results:
        return {
            "metric_name": "mqr/r",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mqr_values = [r[0] for r in results]
    r_values = [r[1] for r in results]
    mean_mqr_over_r = sum(mqr_values) / sum(r_values)
    instances_tested = len(results)
    n_max = max(n for _, _ in results)
    
    conjecture_holds = all(mqr_val >= r_val for mqr_val, r_val in results)
    counterexample = "" if conjecture_holds else "mqr/r < 1.0"
    
    return {
        "metric_name": "mqr/r",
        "metric_value": mean_mqr_over_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mqr/r < 1.0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")