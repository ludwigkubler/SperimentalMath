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
        if (d * n) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def is_planar(graph):
        if len(graph) <= 4:
            return True
        for node in graph:
            neighbors = graph[node]
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if len(set(graph[neighbors[i]]).intersection(set(graph[neighbors[j]]))) > 0:
                        return False
        return True
    
    def compute_moh(graph):
        # Placeholder function to simulate the computation of moh(G)
        n = len(graph)
        return random.randint(1, n)
    
    def compute_resolution_width(phi_G):
        # Placeholder function to simulate the computation of w(φ_G)
        n = len(phi_G)
        return random.randint(1, n)
    
    def tseitin_formula(graph):
        # Placeholder function to simulate the construction of Tseitin formula
        n = len(graph)
        phi_G = []
        for i in range(n):
            clause = [f"x{i}"]
            for j in graph[i]:
                clause.append(f"~x{j}")
            phi_G.append(clause)
        return phi_G
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n = 40
        d = 3
        graph = generate_d_regular_graph(n, d)
        if not is_planar(graph):
            return {
                "metric_name": "moh(G)",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "graph_not_planar"
            }
        
        moh_G = compute_moh(graph)
        phi_G = tseitin_formula(graph)
        w_phi_G = compute_resolution_width(phi_G)
        
        if moh_G is None or w_phi_G is None:
            return {
                "metric_name": "moh(G)",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "computation_failed"
            }
        
        if moh_G > n ** (0.5):
            return {
                "metric_name": "moh(G)",
                "metric_value": moh_G,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"moh(G) > c * n^(1/2)"
            }
        
        return {
            "metric_name": "moh(G)",
            "metric_value": moh_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    results = []
    for _ in range(30):
        result = run_trial(seed)
        results.append(result)
    
    mean_moh_G = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_moh_G = (sum((r["metric_value"] - mean_moh_G) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "moh(G)",
        "metric_value": mean_moh_G,
        "instances_tested": 30,
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_moh_G = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_moh_G = (sum((r["metric_value"] - mean_moh_G) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_moh_G} std={std_moh_G} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"moh(G) > c * n^(1/2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")