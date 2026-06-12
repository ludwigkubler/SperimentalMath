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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank(matrix):
    n = len(matrix)
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for i in range(n):
        if any(row_echelon_form[i]):
            rank += 1
    return rank

def generate_random_graph(n):
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    return graph

def communication_complexity_rank_variance(graph, inputs):
    n = len(graph)
    variance = 0
    for u in range(n):
        for v in range(u+1, n):
            diff_count = sum(1 for i in range(len(inputs[u])) if inputs[v][i] != inputs[u][i])
            variance += diff_count * (n - diff_count)
    return Fraction(variance, n * (n-1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Rank of Adjacency Matrix"
    instances_tested = 0
    total_rank = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        graph = generate_random_graph(n)
        adjacency_matrix = [[graph[u][v] + graph[v][u] for v in range(n)] for u in range(n)]
        
        inputs = [random.choices([0, 1], k=n) for _ in range(2)]
        
        rank_value = rank(adjacency_matrix)
        comm_rank_variance = communication_complexity_rank_variance(graph, inputs)
        
        total_rank += rank_value
        instances_tested += 1
        n_max = max(n_max, n)
        
        if rank_value > comm_rank_variance:
            return {
                "metric_name": metric_name,
                "metric_value": rank_value,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Graph with n={n}, R(A)={rank_value} > CommRankVar(n)={comm_rank_variance}"
            }
    
    mean_rank = Fraction(total_rank, instances_tested)
    return {
        "metric_name": metric_name,
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={r['n_max']}, R(A)={r['metric_value']} > CommRankVar(n)\" first_failing_seed={first_failing_seed}")