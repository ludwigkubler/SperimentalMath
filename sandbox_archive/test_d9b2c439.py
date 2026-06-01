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
    
    def generate_planar_graph(n):
        if n < 3:
            return []
        nodes = list(range(n))
        edges = set()
        while len(edges) < n - 1:
            u, v = random.sample(nodes, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return [nodes, edges]
    
    def term_overlap_graph(G):
        nodes, edges = G
        n = len(nodes)
        T = [[0] * n for _ in range(n)]
        for u, v in edges:
            T[u][v] = 1
            T[v][u] = 1
        return T
    
    def min_rank(T):
        n = len(T)
        rank = 0
        for i in range(n):
            if any(T[i][j] != 0 for j in range(i)):
                rank += 1
                for j in range(n):
                    if T[j][i] != 0:
                        for k in range(n):
                            T[j][k] -= T[i][k]
        return rank
    
    def communication_complexity(G):
        nodes, edges = G
        n = len(nodes)
        cc = 0
        for u in range(n):
            for v in range(u + 1, n):
                if (u, v) not in edges and (v, u) not in edges:
                    cc += 1
        return cc
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            G = generate_planar_graph(n)
            T = term_overlap_graph(G)
            r_T_G = min_rank(T)
            growth_rate_G = communication_complexity(G)
            results.append((r_T_G, growth_rate_G))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No results generated"
        }
    
    r_values, growth_rate_values = zip(*results)
    correlation_coefficient = pearson_correlation(r_values, growth_rate_values)
    p_value = None  # Not computable without statistical tests
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
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
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no clear support or refutation")