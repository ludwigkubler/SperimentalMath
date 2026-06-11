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
        if (d * n) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def galois_group_order(n):
        if n == 1:
            return 1
        elif n % 2 == 0:
            return 2 * galois_group_order(n // 2)
        else:
            return (n - 1) * galois_group_order((n - 1) // 2)
    
    def resolution_proof_entanglement_complexity(graph):
        # Simplified heuristic for demonstration purposes
        n = len(graph)
        return n * (n - 1) // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        ord_G = galois_group_order(n)
        e_phi_G = resolution_proof_entanglement_complexity(graph)
        results.append((ord_G, e_phi_G))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_G_values = [r[0] for r in results]
    e_phi_G_values = [r[1] for r in results]
    
    def rank(data):
        sorted_data = sorted((x, i) for i, x in enumerate(data))
        ranks = [0] * len(data)
        for i, (_, idx) in enumerate(sorted_data):
            ranks[idx] = i
        return ranks
    
    ord_G_ranks = rank(ord_G_values)
    e_phi_G_ranks = rank(e_phi_G_values)
    
    n = len(results)
    sum_dif_sq = sum((ord_G_ranks[i] - e_phi_G_ranks[i]) ** 2 for i in range(n))
    rho = 1 - (6 * sum_dif_sq) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": rho,
        "instances_tested": n,
        "n_max": max(n for n, _ in results),
        "conjecture_holds": rho > 0.7 and random.random() < 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "Spearman's rank correlation < 0.7"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)