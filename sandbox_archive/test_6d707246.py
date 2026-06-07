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

def generate_k_regular_graph(n, k):
    if (n * k) % 2 != 0:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    adj_list = [[] for _ in range(n)]
    degree_count = [0] * n
    
    while any(d < k for d in degree_count):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u == v or v in adj_list[u]:
            continue
        
        adj_list[u].append(v)
        adj_list[v].append(u)
        degree_count[u] += 1
        degree_count[v] += 1
    
    return adj_list

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        
        if pivot_row == -1:
            continue
        
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        for r in range(rows):
            if r != rank and matrix[r][col] != 0:
                factor = matrix[r][col] / matrix[rank][col]
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[rank][c]
        
        rank += 1
    
    return rank

def communication_complexity_rank(graph, subset):
    subgraph = [graph[i] for i in subset if any(j in subset for j in graph[i])]
    matrix = [[0] * len(subgraph) for _ in range(len(subgraph))]
    
    for i in range(len(subgraph)):
        for j in range(i + 1, len(subgraph)):
            if subgraph[j] and j in subgraph[i]:
                matrix[i][j] = 1
                matrix[j][i] = 1
    
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = min(2 * (n - 1), n // 2)  # Ensure the graph is regular
        graph = generate_k_regular_graph(n, k)
        
        total_rank = 0
        for subset_size in range(1, n + 1):
            subsets = list(itertools.combinations(range(n), subset_size))
            for subset in subsets:
                rank = communication_complexity_rank(graph, subset)
                if rank == 0:
                    continue
                total_rank += rank
        
        mli = len(graph) * (len(graph) - 1) / 2
        variance = total_rank / n_values.count(n) / n_values.count(n) if n_values.count(n) > 0 else 0
        
        results.append({
            "n": n,
            "mli": mli,
            "variance": variance
        })
    
    mean_mli = sum(result["mli"] for result in results) / len(results)
    mean_variance = sum(result["variance"] for result in results) / len(results)
    
    conjecture_holds = all(result["mli"] >= 10 * result["variance"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of mli to variance",
        "metric_value": mean_mli / mean_variance,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")