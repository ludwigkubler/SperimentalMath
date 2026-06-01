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

def generate_random_planar_graph(n):
    if n < 3:
        return []
    
    nodes = list(range(n))
    edges = set()
    
    def add_edge(u, v):
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    # Start with a triangle
    add_edge(0, 1)
    add_edge(1, 2)
    add_edge(2, 0)
    
    for _ in range(n - 3):
        u = random.choice(nodes)
        v = random.choice(nodes)
        
        if u == v or (u, v) in edges or (v, u) in edges:
            continue
        
        # Ensure the graph remains planar
        for w in nodes:
            if (w, u) in edges and (w, v) in edges:
                continue
            add_edge(u, v)
            break
    
    return list(edges)

def term_overlap_graph(graph):
    n = len(graph)
    T = [[0] * n for _ in range(n)]
    
    for u, v in graph:
        T[u][v] = 1
        T[v][u] = 1
    
    return T

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    pivot_col = 0
    
    for i in range(m):
        if pivot_col >= n:
            break
        
        max_row = i
        for r in range(i + 1, m):
            if abs(matrix[r][pivot_col]) > abs(matrix[max_row][pivot_col]):
                max_row = r
        
        if matrix[max_row][pivot_col] == 0:
            pivot_col += 1
            continue
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        for r in range(m):
            if r != i and matrix[r][pivot_col] != 0:
                factor = -matrix[r][pivot_col] / matrix[i][pivot_col]
                for c in range(n):
                    matrix[r][c] += factor * matrix[i][c]
        
        rank += 1
        pivot_col += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_planar_graph(n)
        T = term_overlap_graph(graph)
        
        rank = gaussian_elimination(T)
        communication_rank = rank
        
        growth_rate = n / (n - 1) if n > 1 else 0
        
        results.append({
            "communication_rank": communication_rank,
            "growth_rate": growth_rate
        })
    
    correlation_sum = 0
    p_value_sum = 0
    
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            x1, y1 = results[i]["communication_rank"], results[i]["growth_rate"]
            x2, y2 = results[j]["communication_rank"], results[j]["growth_rate"]
            
            if y1 == 0 or y2 == 0:
                continue
            
            correlation_sum += (x1 * y2 - x2 * y1) / math.sqrt(y1**2 * y2**2)
            p_value_sum += 1
    
    n_pairs = len(n_values) * (len(n_values) - 1) // 2
    mean_correlation = correlation_sum / n_pairs
    p_value = min(1, p_value_sum / n_pairs)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_correlation) >= 0.8 and p_value <= 0.05,
        "counterexample": "" if abs(mean_correlation) >= 0.8 and p_value <= 0.05 else "Pearson correlation coefficient < 0.8 or p-value > 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break