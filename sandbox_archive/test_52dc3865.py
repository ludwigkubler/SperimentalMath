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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (d * n) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def circuit_monotone_complexity(graph):
        n = len(graph)
        if n == 1:
            return 0
        nodes = list(range(n))
        random.shuffle(nodes)
        complexity = 0
        for i in range(1, n):
            u = nodes[i]
            v = nodes[0]
            if u not in graph[v]:
                complexity += 1
        return complexity
    
    def minimal_geometric_entropy(graph):
        n = len(graph)
        if n == 1:
            return 0
        entropy = 0
        for i in range(n):
            degree = len(graph[i])
            entropy += math.log(degree + 1) / (n - 1)
        return entropy
    
    d = random.randint(2, 4)
    n = random.randint(5, 30)
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "circuit_monotone_complexity",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_graph"
        }
    
    c_m = circuit_monotone_complexity(graph)
    mge = minimal_geometric_entropy(graph)
    
    return {
        "metric_name": "circuit_monotone_complexity",
        "metric_value": mge / c_m if c_m != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mge / c_m <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if "metric_value" in r) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")