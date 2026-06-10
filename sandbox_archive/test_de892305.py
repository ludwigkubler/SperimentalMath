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

def generate_k_regular_graph(n, k):
    if 2 * k > n:
        return None
    
    edges = [[] for _ in range(n)]
    added_edges = set()
    
    def add_edge(i, j):
        if (i, j) not in added_edges and (j, i) not in added_edges:
            edges[i].append(j)
            edges[j].append(i)
            added_edges.add((i, j))
            added_edges.add((j, i))
    
    for i in range(n):
        neighbors = random.sample(range(n), k - len(edges[i]))
        for neighbor in neighbors:
            add_edge(i, neighbor)
    
    return edges

def count_simple_loops(edges):
    n = len(edges)
    visited = [False] * n
    loops = 0
    
    def dfs(node, parent):
        nonlocal loops
        if visited[node]:
            loops += 1
            return True
        visited[node] = True
        for neighbor in edges[node]:
            if neighbor != parent and dfs(neighbor, node):
                return True
        visited[node] = False
        return False
    
    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
    
    return loops

def communication_complexity_rank_variance(edges):
    n = len(edges)
    rank_matrix = [[0] * n for _ in range(n)]
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank = m
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                rank -= 1
        
        return rank
    
    for i in range(n):
        for j in range(i + 1, n):
            rank_matrix[i][j] = rank_matrix[j][i] = gaussian_elimination([row[:] for row in edges])[i]
    
    variance = sum(sum(row) ** 2 for row in rank_matrix) / (n * (n - 1))
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    m_loop_sum = 0
    R_var_sum = 0
    instances_tested = 0
    
    for n in n_values:
        k = random.randint(2, min(n - 1, 8))
        G = generate_k_regular_graph(n, k)
        if G is None:
            continue
        
        m_loop = count_simple_loops(G)
        R_var = communication_complexity_rank_variance(G)
        
        if m_loop == 0 or R_var == 0:
            continue
        
        m_loop_sum += m_loop
        R_var_sum += R_var
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_m_loop = m_loop_sum / instances_tested
    mean_R_var = R_var_sum / instances_tested
    
    # Pearson correlation coefficient calculation
    covariance = sum((m_loop - mean_m_loop) * (R_var - mean_R_var) for m_loop, R_var in zip(m_loop_values, R_var_values))
    variance_m_loop = sum((m_loop - mean_m_loop) ** 2 for m_loop in m_loop_values)
    variance_R_var = sum((R_var - mean_R_var) ** 2 for R_var in R_var_values)
    
    if variance_m_loop == 0 or variance_R_var == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_m_loop) * math.sqrt(variance_R_var))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr_coeff >= 0.7,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")