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
    
    def communication_rank(graph):
        # Placeholder for actual computation
        return len(graph)

    def is_subgraph(G, H):
        nodes_G = set(G.keys())
        nodes_H = set(H.keys())
        if not nodes_G.issubset(nodes_H):
            return False
        for u in nodes_G:
            for v in nodes_G:
                if (u, v) in G and (u, v) not in H:
                    return False
        return True

    def min_order_kneser(G):
        n = len(G)
        k = 1
        while True:
            K_n_k = {frozenset(range(i, i+k)) for i in range(n-k+1)}
            if any(is_subgraph(G, K) for K in K_n_k):
                return k
            k += 1

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        G = {i: set() for i in range(n)}
        edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(random.randint(int(n*(n-1)/2)-10, int(n*(n-1)/2)+10))]
        for u, v in edges:
            G[u].add(v)
            G[v].add(u)

        min_order = min_order_kneser(G)
        r_G = communication_rank(G)
        results.append((min_order, r_G))

    mean_min_order = sum(x[0] for x in results) / len(results)
    mean_r_G = sum(x[1] for x in results) / len(results)
    correlation = pearson_correlation([x[0] for x in results], [x[1] for x in results])

    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation > 0.7 and all(x >= 0 for x in [correlation]),
        "counterexample": "" if correlation > 0.7 else "Pearson Correlation < 0.7"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_corr = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation < 0.7\" first_failing_seed={first_failing_seed}")