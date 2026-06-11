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
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = random.randint(1, 10)
        return G
    
    def min_distance_separating_set(G):
        n = len(G)
        visited = [False] * n
        dist = [-1] * n
        queue = []
        
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                dist[i] = 0
                queue.append(i)
                
                while queue:
                    u = queue.pop(0)
                    for v in range(n):
                        if G[u][v] > 0 and not visited[v]:
                            visited[v] = True
                            dist[v] = dist[u] + 1
                            queue.append(v)
        
        return max(dist) if any(d != -1 for d in dist) else float('inf')
    
    def quotient_space_dimension(G, mdss):
        n = len(G)
        quotient_space = [0] * (n // mdss)
        for i in range(n):
            quotient_space[i // mdss] += sum(G[i])
        return max(quotient_space)
    
    def rank_variance(G):
        n = len(G)
        total = 0
        for row in G:
            total += sum(row)
        mean = total / (n * n)
        variance = sum((sum(row) - mean) ** 2 for row in G) / (n * n)
        return variance
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    for j in range(i, n):
                        A[k][j] -= A[i][j] * A[k][i]
        return A
    
    def matrix_rank(A):
        rank = 0
        A_copy = [row[:] for row in A]
        gaussian_elimination(A_copy)
        for row in A_copy:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        mdss = min_distance_separating_set(G)
        if mdss == float('inf'):
            continue
        dim_quotient_space = quotient_space_dimension(G, mdss)
        rank_var = rank_variance(G)
        rank = matrix_rank(G)
        
        results.append({
            "n": n,
            "dim_quotient_space": dim_quotient_space,
            "rank_var": rank_var,
            "rank": rank
        })
    
    if len(results) < 30:
        return {
            "metric_name": "dimension_of_quotient_space",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_dim = sum(r["dim_quotient_space"] for r in results) / len(results)
    std_dim = math.sqrt(sum((r["dim_quotient_space"] - mean_dim) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["dim_quotient_space"] - (math.sqrt(r["n"]) * 0.9)) < 0.1 and abs(r["rank_var"] - (r["rank"] ** 2 / r["n"])) < 0.3) / len(results)
    
    return {
        "metric_name": "dimension_of_quotient_space",
        "metric_value": mean_dim,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_dim = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dim = math.sqrt(sum((r["metric_value"] - mean_dim) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dim} std={std_dim} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dim} std={std_dim} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")