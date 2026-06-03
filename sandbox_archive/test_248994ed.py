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
    
    def generate_graph(n):
        if n == 1:
            return {0: []}
        max_degree = min(2 * (n - 1), 30)
        degrees = [random.randint(1, max_degree) for _ in range(n)]
        graph = {i: [] for i in range(n)}
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < degrees[i] and len(graph[j]) < degrees[j]:
                    edge = (min(i, j), max(i, j))
                    if edge not in edges_used:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_used.add(edge)
        return graph
    
    def max_degree(graph):
        return max(len(neighbors) for neighbors in graph.values())
    
    def grothendieck_teichmueller_rank(graph):
        n = len(graph)
        if n == 1:
            return 0
        rank = 0
        for i in range(n):
            rank += len(graph[i])
        return rank // 2
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    log_degrees = []
    sqrt_ns = []
    
    for n in n_values:
        graph = generate_graph(n)
        d_G = max_degree(graph)
        r_G = grothendieck_teichmueller_rank(graph)
        ranks.append(r_G)
        log_degrees.append(math.log(d_G))
        sqrt_ns.append(math.sqrt(n))
    
    corr_log_d_r = correlation(log_degrees, ranks)
    corr_sqrt_n_r = correlation(sqrt_ns, ranks)
    
    return {
        "metric_name": "Correlation",
        "metric_value": corr_sqrt_n_r,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": corr_log_d_r >= 0.7 and corr_sqrt_n_r <= 0.5,
        "counterexample": "" if corr_log_d_r >= 0.7 and corr_sqrt_n_r <= 0.5 else f"Correlation with log d(G) = {corr_log_d_r}, Correlation with √n = {corr_sqrt_n_r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")