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
        return [list(edges)]
    
    def communication_rank(graph):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(graph)
    
    def min_order_kneser(G):
        n = len(G[0])
        for k in range(1, n + 1):
            K = generate_kneser_graph(n, k)
            if contains_subgraph(K, G):
                return k
        return None
    
    def generate_kneser_graph(n, k):
        vertices = list(range(n))
        edges = []
        for comb in itertools.combinations(vertices, k):
            for i in range(k):
                for j in range(i + 1, k):
                    if comb[i] < comb[j]:
                        edges.append((comb[i], comb[j]))
        return [edges]
    
    def contains_subgraph(K, G):
        K_edges = set(tuple(sorted(e)) for e in K[0])
        G_edges = set(tuple(sorted(e)) for e in G[0])
        return K_edges.issubset(G_edges)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    ranks = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        rank = communication_rank(graph)
        min_order = min_order_kneser(graph)
        if min_order is not None:
            min_orders.append(min_order)
            ranks.append(rank)
    
    if len(min_orders) < 30 or len(ranks) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(min_orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    corr = pearson_correlation(min_orders, ranks)
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": corr > 0.7 and all(r >= 0 for r in ranks),
        "counterexample": "" if corr > 0.7 and all(r >= 0 for r in ranks) else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None and r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")