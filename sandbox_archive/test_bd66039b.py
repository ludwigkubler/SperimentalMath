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
    
    def generate_max_cut_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def find_min_moves(G):
        n = len(G)
        dist = [[float('inf')] * n for _ in range(n)]
        for u in range(n):
            dist[u][u] = 0
        for u, v in G:
            dist[u][v] = 1
            dist[v][u] = 1
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return min(dist[u][v] for u, v in G)
    
    def compute_communication_matrix_rank(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                for j in range(i + 1, n):
                    if any(A[k][j] != A[k][i] for k in range(i)):
                        for k in range(i, n):
                            A[k][j] ^= A[k][i]
                        rank += 1
                        break
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            G = generate_max_cut_instance(n)
            alpha_n = find_min_moves(G)
            k_n = compute_communication_matrix_rank(G)
            results.append((n, alpha_n, k_n))
    
    if not results:
        return {
            "metric_name": "communication_matrix_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_k_n = sum(k_n for _, _, k_n in results) / len(results)
    max_n = max(n for n, _, _ in results)
    conjecture_holds = all(k_n <= alpha_n**2 for _, alpha_n, k_n in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_matrix_rank",
        "metric_value": mean_k_n,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_k_n = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_k_n = math.sqrt(sum((result["metric_value"] - mean_k_n)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_k_n:.2f} std={std_k_n:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")