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
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = Fraction(-matrix[j][i], matrix[i][i])
        for j in range(i, n):
            if i != j:
                matrix[j][i] = 0
            for k in range(i+1, n):
                matrix[j][k] += factor * matrix[i][k]
    return matrix

def communication_complexity_rank_variance(G):
    n = len(G)
    edges = []
    for u in range(n):
        for v in range(u+1, n):
            if G[u][v]:
                edges.append((u, v))
    
    m = len(edges)
    rank_matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i+1, m):
            u, v = edges[i]
            x, y = edges[j]
            if (u == x and v == y) or (u == y and v == x):
                rank_matrix[i][j] = rank_matrix[j][i] = 1
            else:
                rank_matrix[i][j] = rank_matrix[j][i] = 0
    
    rank_matrix = gaussian_elimination(rank_matrix)
    
    # Calculate rank variance
    rank_counts = [sum(row) for row in rank_matrix]
    mean_rank = sum(rank_counts) / n
    variance = sum((x - mean_rank) ** 2 for x in rank_counts) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k = 3  # Regularity of the graph
    n_max = 40
    instances_tested = 0
    
    m_loop_values = []
    R_var_values = []
    
    for n in range(5, n_max + 1):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.randint(0, k-1) == 0:
                    G[i][j] = G[j][i] = 1
        
        # Count minimal number of simple loops
        visited = [False] * n
        loop_count = 0
        for u in range(n):
            if not visited[u]:
                stack = [u]
                while stack:
                    v = stack.pop()
                    if not visited[v]:
                        visited[v] = True
                        for w in range(n):
                            if G[v][w] and not visited[w]:
                                stack.append(w)
                loop_count += 1
        
        m_loop_values.append(loop_count)
        
        # Calculate communication complexity rank variance
        R_var = communication_complexity_rank_variance(G)
        R_var_values.append(R_var)
        
        instances_tested += n
    
    if len(m_loop_values) != len(R_var_values):
        return {
            "metric_name": "m_loop vs R_var",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "m_loop and R_var lists have different lengths"
        }
    
    correlation_coefficient = sum((m_loop_values[i] - mean_m_loop) * (R_var_values[i] - mean_R_var) for i in range(len(m_loop_values))) / len(m_loop_values)
    mean_m_loop = sum(m_loop_values) / len(m_loop_values)
    mean_R_var = sum(R_var_values) / len(R_var_values)
    
    return {
        "metric_name": "m_loop vs R_var",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")