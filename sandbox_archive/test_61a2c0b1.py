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
        G = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u > v: u, v = v, u
            if (u, v) not in edges and (v, u) not in edges:
                G[u].append(v)
                G[v].append(u)
                edges.add((u, v))
        return G
    
    def min_index(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in G[u]:
                A[u][v] = 1
        rank_var = 0
        for i in range(n):
            row_sum = sum(A[i])
            if row_sum == 0:
                continue
            for j in range(i + 1, n):
                col_sum = sum(A[j])
                if col_sum == 0:
                    continue
                common = sum(A[i][k] * A[j][k] for k in range(n))
                rank_var += (common - row_sum * col_sum / n) ** 2
        return math.sqrt(rank_var)
    
    def rank_variance(G):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in G[u]:
                M[u][v] = 1
        rank_var = 0
        for i in range(n):
            row_sum = sum(M[i])
            if row_sum == 0:
                continue
            for j in range(i + 1, n):
                col_sum = sum(M[j])
                if col_sum == 0:
                    continue
                common = sum(M[i][k] * M[j][k] for k in range(n))
                rank_var += (common - row_sum * col_sum / n) ** 2
        return math.sqrt(rank_var)
    
    def correlation(X, Y):
        if len(X) != len(Y):
            raise ValueError("X and Y must have the same length")
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        var_X = sum((X[i] - mean_X) ** 2 for i in range(n)) / n
        var_Y = sum((Y[i] - mean_Y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_X) * math.sqrt(var_Y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    X, Y = [], []
    for n in n_values:
        G = generate_graph(n)
        min_index_val = min_index(G)
        rank_var_val = rank_variance(G)
        X.append(min_index_val)
        Y.append(rank_var_val)
    
    corr = correlation(X, Y)
    p_value = 0.05  # Placeholder for actual p-value calculation
    conjecture_holds = abs(corr) >= 0.8 and p_value < 0.05
    
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(X),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
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
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")