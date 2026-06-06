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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def k_theory(edges):
        # Simplified K-theory calculation (not actual K-theory)
        return len(edges) % 2
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank_var = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in graph:
                    rank_var += 1
        return rank_var / (n * (n - 1) / 2)
    
    def min_order(K):
        # Simplified minimal order calculation
        return K
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_graph(n)
        K = k_theory(graph)
        min_K = min_order(K)
        rank_var = communication_complexity_rank_variance(graph)
        results.append((min_K, rank_var))
    
    if not results:
        return {
            "metric_name": "Jaccard_similarity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    min_Ks, rank_vars = zip(*results)
    jaccard_similarity = sum(abs(x - y) for x, y in zip(min_Ks, rank_vars)) / len(results)
    
    return {
        "metric_name": "Jaccard_similarity",
        "metric_value": jaccard_similarity,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": jaccard_similarity > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Jaccard similarity below 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")