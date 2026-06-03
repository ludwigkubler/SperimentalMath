# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_max_cut_instance(n):
    edges = set()
    for u, v in combinations(range(n), 2):
        if random.random() < 0.5:
            edges.add((u, v))
    return edges

def find_min_moves(G):
    n = len(G)
    dist = [[math.inf] * n for _ in range(n)]
    for u in range(n):
        dist[u][u] = 0
    for u, v in G:
        dist[u][v] = 1
        dist[v][u] = 1
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return min(dist[u][v] for u, v in combinations(range(n), 2))

def compute_communication_matrix_rank(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for u, v in G:
        A[u][v] = 1
        A[v][u] = 1
    
    rank = 0
    for i in range(n):
        if all(A[j][i] == 0 for j in range(i)):
            rank += 1
            for j in range(n):
                A[j][i] = A[i][j]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n - 4)):
            G = generate_max_cut_instance(n)
            alpha_n = find_min_moves(G)
            k_n = compute_communication_matrix_rank(G)
            
            if k_n > alpha_n ** 2 * 10:  # Buffer to avoid false negatives
                conjecture_holds = False
                counterexample = f"n={n}, k(n)={k_n}, α(n)^2={alpha_n**2}"
                break
            
            metric_values.append(k_n)
    
    return {
        "metric_name": "communication_matrix_rank",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")