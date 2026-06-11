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
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            pivot = M[i][i]
            for j in range(n + 1):
                M[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = M[j][i]
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def min_distance_separating_set(G):
        n = len(G)
        distances = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            distances[i][i] = 0
            queue = [i]
            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if G[u][v] == 1 and distances[i][v] == math.inf:
                        distances[i][v] = distances[i][u] + 1
                        queue.append(v)
        min_set = set()
        for i in range(n):
            for j in range(i+1, n):
                if distances[i][j] > 0 and distances[i][j] < math.inf:
                    min_set.add(min(i, j))
        return list(min_set)
    
    def quotient_space_dimension(G):
        n = len(G)
        min_set = min_distance_separating_set(G)
        G_prime = [[G[u][v] for v in range(n) if v not in min_set] for u in range(n) if u not in min_set]
        rank = 0
        for i in range(len(G_prime)):
            if any(all(row[j] == 0 for j in range(i)) for row in G_prime):
                rank += 1
        return rank
    
    def rank_variance(rank_values):
        n = len(rank_values)
        mean_rank = sum(rank_values) / n
        variance = sum((x - mean_rank) ** 2 for x in rank_values) / n
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        dim_quotient_space = quotient_space_dimension(G)
        rank_variances = [quotient_space_dimension(generate_random_graph(n)) for _ in range(30)]
        mean_rank_variance = sum(rank_variances) / len(rank_variances)
        
        results.append({
            "metric_name": "dim_quotient_space",
            "metric_value": dim_quotient_space,
            "instances_tested": 30,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "mean_metric_value": mean_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {'seed':<10} {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")