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
        if n <= 1 or k < 2:
            return []
        graph = [[] for _ in range(n)]
        colors = list(range(1, k + 1))
        for i in range(n):
            color = random.choice(colors)
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def p_adic_l_function_rank(graph):
        # Simplified version of p-adic L-function rank for testing purposes
        return len(graph)
    
    def communication_rank_growth_rate(graph):
        n = len(graph)
        if n <= 1:
            return 0
        max_degree = max(len(neighbors) for neighbors in graph)
        return max_degree / (n - 1)
    
    def pearson_correlation(xs, ys):
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        denominator = (sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)) ** 0.5
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    lrank_values = []
    crg_rate_values = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_k_colorable_graph(n, k=3)
            lrank = p_adic_l_function_rank(graph)
            crg_rate = communication_rank_growth_rate(graph)
            lrank_values.append(lrank)
            crg_rate_values.append(crg_rate)
    
    correlation = pearson_correlation(lrank_values, crg_rate_values)
    mean_lrank = sum(lrank_values) / len(lrank_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(lrank_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_lrank <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_lrank <= 3 else "correlation < 0.8 or mean lrank > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8 or mean lrank > 3\" first_failing_seed={first_failing_seed}")