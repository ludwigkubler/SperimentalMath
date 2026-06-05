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

def generate_graph(n, m):
    if n * (n - 1) // 2 < m:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = {i: set() for i in range(n)}
    edges_added = 0
    
    while edges_added < m:
        u, v = random.sample(range(n), 2)
        if u not in G[v]:
            G[u].add(v)
            G[v].add(u)
            edges_added += 1
    
    return G

def incidence_matrix(G):
    n = len(G)
    m = sum(len(neighbors) for neighbors in G.values()) // 2
    M = [[0] * (n + m) for _ in range(n)]
    
    for u, neighbors in enumerate(G.items()):
        for v in neighbors[1]:
            M[u][v] += 1
    
    return M

def gaussian_elimination(M):
    n = len(M)
    m = len(M[0])
    rank = 0
    pivot_col = 0
    
    for i in range(n):
        if pivot_col >= m:
            break
        
        max_row = i
        for r in range(i + 1, n):
            if abs(M[r][pivot_col]) > abs(M[max_row][pivot_col]):
                max_row = r
        
        M[i], M[max_row] = M[max_row], M[i]
        
        if M[i][pivot_col] == 0:
            pivot_col += 1
            continue
        
        rank += 1
        for j in range(m):
            M[i][j] /= M[i][pivot_col]
        
        for r in range(n):
            if r != i and M[r][pivot_col] != 0:
                factor = -M[r][pivot_col]
                for j in range(m):
                    M[r][j] += factor * M[i][j]
        
        pivot_col += 1
    
    return rank

def min_invariant_generators(G):
    n = len(G)
    M = incidence_matrix(G)
    
    # Add identity matrix to the right of M
    for i in range(n):
        M[i].extend([0] * (n - i))
        M[i][i + n] = 1
    
    rank = gaussian_elimination(M)
    return rank

def communication_complexity_rank(G):
    n = len(G)
    m = sum(len(neighbors) for neighbors in G.values()) // 2
    rank = 0
    
    # Compute the adjacency matrix
    A = [[0] * n for _ in range(n)]
    for u, neighbors in enumerate(G.items()):
        for v in neighbors[1]:
            A[u][v] = 1
    
    # Perform Gaussian elimination on A
    rank_A = gaussian_elimination(A)
    
    return rank_A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n - 1, n * (n - 1) // 2)
        G = generate_graph(n, m)
        
        min_gen = min_invariant_generators(G)
        rank_comm = communication_complexity_rank(G)
        
        results.append({
            "n": n,
            "m": m,
            "min_gen": min_gen,
            "rank_comm": rank_comm
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    min_gen_values = [r["min_gen"] for r in results]
    rank_comm_values = [r["rank_comm"] for r in results]
    
    mean_min_gen = sum(min_gen_values) / len(min_gen_values)
    mean_rank_comm = sum(rank_comm_values) / len(rank_comm_values)
    
    abs_diffs = [abs(m - n) for m, n in zip(min_gen_values, rank_comm_values)]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    
    correlation_coefficient = 0
    if mean_rank_comm != 0:
        covariance = sum((m - mean_min_gen) * (n - mean_rank_comm) for m, n in zip(min_gen_values, rank_comm_values))
        variance_min_gen = sum((m - mean_min_gen) ** 2 for m in min_gen_values)
        variance_rank_comm = sum((n - mean_rank_comm) ** 2 for n in rank_comm_values)
        correlation_coefficient = covariance / (math.sqrt(variance_min_gen) * math.sqrt(variance_rank_comm))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")