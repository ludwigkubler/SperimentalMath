# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_random_k_clique_free_graph(n, k):
    if n < k + 1:
        return None
    G = {i: set() for i in range(n)}
    edges_added = 0
    while edges_added < k * (n - k) // 2:
        u, v = random.sample(range(n), 2)
        if u not in G[v] and v not in G[u]:
            G[u].add(v)
            G[v].add(u)
            edges_added += 1
    return G

def alexander_defect_invariant(G):
    n = len(G)
    M = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if j in G[i]:
            M[i][j] = M[j][i] = 1
    return max(sum(row) for row in M)

def communication_complexity_rank(G):
    n = len(G)
    rank = {}
    for u in range(n):
        for v in range(u + 1, n):
            if u not in G[v] and v not in G[u]:
                rank[(u, v)] = 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_k_clique_free_graph(n, 2)
        if G is None:
            continue
        defect = alexander_defect_invariant(G)
        rank = communication_complexity_rank(G)
        
        if defect == 0 or len(rank) == 0:
            continue
        
        results.append((defect, sum(rank.values())))
    
    if not results:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def calculate_spearman_rank_correlation(defects, ranks):
        n = len(defects)
        sorted_defects = sorted(range(n), key=lambda i: defects[i])
        sorted_ranks = sorted(range(n), key=lambda i: ranks[i])
        
        d_squared_sum = sum((sorted_defects[i] - sorted_ranks[i]) ** 2 for i in range(n))
        rho_numerator = n * (n**2 - 1) - 6 * d_squared_sum
        rho_denominator = (n**2 - 1) * (2 * n**2 - 9 * n + 7)
        
        return rho_numerator / rho_denominator
    
    defects, ranks = zip(*results)
    rho = calculate_spearman_rank_correlation(defects, ranks)
    
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": abs(rho),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(rho) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")