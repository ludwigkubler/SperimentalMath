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

def random_k_clique_free_graph(n, k):
    G = {i: set() for i in range(n)}
    edges_added = 0
    while edges_added < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if len(G[u]) >= k or len(G[v]) >= k:
            continue
        G[u].add(v)
        G[v].add(u)
        edges_added += 1
    return G

def alexander_defect_invariant(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in G[u]:
            A[u][v] = -1
            A[v][u] = -1
    for i in range(n):
        A[i][i] = 1
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        defect = 0
        for row in A:
            defect += sum(abs(x) for x in row)
        return defect
    
    return gaussian_elimination(A)

def communication_complexity_rank(G):
    n = len(G)
    rank = 0
    for u in range(n):
        for v in G[u]:
            if u < v and (u, v) not in rank:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = random_k_clique_free_graph(n, k=2)
            defect = alexander_defect_invariant(G)
            rank = communication_complexity_rank(G)
            metric_value.append((defect, rank))
            instances_tested += 1
    
    if not metric_value:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric"
        }
    
    def spearman_rank_correlation(data):
        ranks = {x: i + 1 for i, x in enumerate(sorted(set(x[0] for x in data)))}
        rank_data = [(ranks[x[0]], ranks[x[1]]) for x in data]
        n = len(rank_data)
        d_squared_sum = sum((x[0] - x[1]) ** 2 for x in rank_data)
        rho_numerator = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
        return rho_numerator
    
    rho = spearman_rank_correlation(metric_value)
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": abs(rho),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(rho) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_value = (sum((x["metric_value"] - mean_value) ** 2 for x in results if x["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")