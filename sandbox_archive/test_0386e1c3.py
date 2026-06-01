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
        if (n * d) % 2 != 0 or d < 1 or n < d + 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def is_planar(graph):
        n = len(graph)
        if n <= 4:
            return True
        for v in range(n):
            neighbors = graph[v]
            for u in neighbors:
                for w in graph[u]:
                    if w != v and (v, w) not in graph[u] and (u, v) not in graph[w]:
                        return False
        return True
    
    def topological_degree(graph):
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph]
        return max(degrees), min(degrees)
    
    def frege_proof_size(graph):
        n = len(graph)
        if not is_planar(graph):
            return None
        # Simplified Frege proof size estimation based on number of edges
        m = sum(len(neighbors) for neighbors in graph) // 2
        return m
    
    n_max = 40
    instances_tested = 0
    correlation_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            td_max, td_min = topological_degree(graph)
            f_size = frege_proof_size(graph)
            if f_size is not None:
                instances_tested += 1
                correlation_values.append((td_max + td_min) / 2 - f_size)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = sum(correlation_values) / len(correlation_values)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) <= 2,
        "counterexample": "" if abs(correlation) <= 2 else f"abs(correlation) = {abs(correlation)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 5 for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if abs(r["metric_value"]) > 5)
        print(f"RESULT: FALSIFIED counterexample='abs(correlation) > 5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")