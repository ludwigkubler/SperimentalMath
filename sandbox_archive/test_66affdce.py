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

# Helper functions for graph operations
def configuration_model(n, m):
    if 3 * n != 2 * m:
        raise ValueError("Invalid number of edges for a 3-regular graph")
    
    vertices = list(range(n))
    edges = []
    degrees = [0] * n
    
    while len(edges) < m:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and degrees[u] < 3 and degrees[v] < 3 and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    
    return edges

def edge_expansion(graph):
    n = len(graph)
    m = len(graph) // 2
    cuts = [set() for _ in range(n)]
    
    for u, v in graph:
        cuts[u].add(v)
        cuts[v].add(u)
    
    min_cut_size = float('inf')
    for size in range(1, n // 2 + 1):
        for S in combinations(range(n), size):
            cut_size = sum(len(cuts[v] & set(S)) for v in S) / len(S)
            if cut_size < min_cut_size:
                min_cut_size = cut_size
    
    return min_cut_size

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def rank_real(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    
    def gaussian_elimination(A):
        rows, cols = len(A), len(A[0])
        r, c = 0, 0
        while r < rows and c < cols:
            if A[r][c] == 0:
                swap_row = r + 1
                while swap_row < rows and A[swap_row][c] == 0:
                    swap_row += 1
                if swap_row == rows:
                    c += 1
                    continue
                for k in range(cols):
                    A[r][k], A[swap_row][k] = A[swap_row][k], A[r][k]
            pivot = A[r][c]
            for k in range(c, cols):
                A[r][k] /= pivot
            for i in range(rows):
                if i != r:
                    factor = A[i][c]
                    for k in range(c, cols):
                        A[i][k] -= factor * A[r][k]
            r += 1
            c += 1
    
    gaussian_elimination(A)
    
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [4, 6, 8, 10, 12, 14]
    results = []
    
    for m in m_values:
        graph_edges = configuration_model(m, 3 * m // 2)
        graph = set(graph_edges)
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            sigma = {v: random.choice([0, 1]) for v in range(m)}
            if sum(sigma.values()) % 2 == 0:
                continue
            
            h_G = edge_expansion(graph)
            n = len(graph_edges)
            
            # Construct the Tseitin function truth table
            def tseitin(v):
                return sigma[v]
            
            truth_table = []
            for i in range(1 << (n // 2)):
                row = [tseitin(i)]
                for j in range(n // 2, n):
                    row.append(tseitin(j))
                truth_table.append(row)
            
            # Compute the rank of the real matrix
            M_G_sigma_pi = [[0] * (1 << ((n + 1) // 2)) for _ in range(1 << (n // 2))]
            for i in range(1 << (n // 2)):
                for j in range(1 << ((n + 1) // 2)):
                    M_G_sigma_pi[i][j] = truth_table[i][j]
            
            rank_value = rank_real(M_G_sigma_pi)
            results.append({
                "m": m,
                "h_G": h_G,
                "rank_value": rank_value
            })
    
    if not results:
        return {
            "metric_name": "log2_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_rank_values = [math.log2(result["rank_value"]) for result in results]
    h_G_m_values = [result["h_G"] * result["m"] for result in results]
    
    mean_log2_rank = sum(log2_rank_values) / len(log2_rank_values)
    std_log2_rank = math.sqrt(sum((x - mean_log2_rank) ** 2 for x in log2_rank_values) / len(log2_rank_values))
    
    slope, intercept = linear_regression(h_G_m_values, log2_rank_values)
    p_value = t_test_slope(slope, intercept, h_G_m_values, log2_rank_values)
    
    conjecture_holds = all(x >= 0.25 * y for x, y in zip(log2_rank_values, h_G_m_values)) and slope >= 0.25 and p_value < 0.01
    
    return {
        "metric_name": "log2_rank",
        "metric_value": mean_log2_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "slope < 0.25 or p-value >= 0.01"
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

def t_test_slope(slope, intercept, x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    ssr = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    sse = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    mse = sse / (n - 2)
    se_slope = math.sqrt(mse * (1 / n + (mean_x ** 2 / sum((xi - mean_x) ** 2 for xi in x))))
    
    t_stat = slope / se_slope
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-2))
    
    return p_value

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_log2_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_log2_rank = math.sqrt(sum((r["metric_value"] - mean_log2_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log2_rank} std={std_log2_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope < 0.25 or p-value >= 0.01\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")