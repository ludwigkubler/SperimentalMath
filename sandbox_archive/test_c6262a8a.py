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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0:
            return None
        edges = []
        for i in range(n):
            neighbors = random.sample(range(n), k - 1)
            while any(j in edges[i] for j in neighbors):
                neighbors = random.sample(range(n), k - 1)
            for j in neighbors:
                edges.append((i, j))
        return edges

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = rank
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            A[rank], A[pivot_row] = A[pivot_row], A[rank]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank

    def communication_complexity_rank_variance(A):
        m, n = len(A), len(A[0])
        rank = gaussian_elimination(A)
        return (m - rank) / m

    def homotopy_group(G):
        # This is a placeholder for the actual computation of π_1(G).
        # For simplicity, we assume it returns a value proportional to n.
        return sum(1 for u in G for v in G if u != v and (u, v) in G or (v, u) in G)

    def count_simple_loops(G):
        loops = 0
        visited = [False] * len(G)
        stack = []
        for i in range(len(G)):
            if not visited[i]:
                stack.append(i)
                while stack:
                    node = stack.pop()
                    visited[node] = True
                    for neighbor in G[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
                        elif neighbor != stack[-1]:
                            loops += 1
        return loops

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        k = random.randint(2, min(n - 1, 3))
        G = generate_k_regular_graph(n, k)
        if G is None:
            continue
        
        m_loop_G = count_simple_loops(G)
        R_var_G = communication_complexity_rank_variance(G)
        homotopy_G = homotopy_group(G)
        
        metrics.append({
            "n": n,
            "m_loop_G": m_loop_G,
            "R_var_G": R_var_G,
            "homotopy_G": homotopy_G
        })
    
    if len(metrics) < 30:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(metric["n"] for metric in metrics),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    m_loop_values = [metric["m_loop_G"] for metric in metrics]
    R_var_values = [metric["R_var_G"] for metric in metrics]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    correlation_coefficient = pearson_correlation(m_loop_values, R_var_values)
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(metric["n"] for metric in metrics),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{r['metric_value']:.2f}\" first_failing_seed={seed}")
                break