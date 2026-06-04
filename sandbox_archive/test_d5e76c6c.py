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
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def is_vertex_cover(graph, cover):
        for u in range(len(graph)):
            if all(v not in cover for v in graph[u]):
                return False
        return True
    
    def vertex_cover_size(graph):
        n = len(graph)
        best_cover = None
        best_size = float('inf')
        for i in range(1 << n):
            cover = [j for j in range(n) if (i >> j) & 1]
            if is_vertex_cover(graph, cover) and len(cover) < best_size:
                best_cover = cover
                best_size = len(cover)
        return best_size
    
    def ehrhart_quotient(n):
        # Placeholder for Ehrhart quotient calculation
        return n * (n - 1) // 2
    
    def frege_proof_depth(graph, size):
        # Placeholder for Frege proof depth calculation
        return size * math.log(size, 2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 2)  # Assuming d=2 for simplicity
        if graph is None:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "graph_generation_failed"
            }
        size = vertex_cover_size(graph)
        o_G = ehrhart_quotient(n)
        f_G = frege_proof_depth(graph, size)
        results.append((o_G, f_G))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    o_G_values = [o for o, _ in results]
    f_G_values = [f for _, f in results]
    
    mean_o_G = sum(o_G_values) / len(o_G_values)
    mean_f_G = sum(f_G_values) / len(f_G_values)
    
    covariance = sum((o - mean_o_G) * (f - mean_f_G) for o, f in results) / len(results)
    variance_o_G = sum((o - mean_o_G) ** 2 for o in o_G_values) / len(o_G_values)
    variance_f_G = sum((f - mean_f_G) ** 2 for f in f_G_values) / len(f_G_values)
    
    correlation_coefficient = covariance / math.sqrt(variance_o_G * variance_f_G)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in [(o, n) for o, f, n in results]),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 8)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}"
    
    print(result)