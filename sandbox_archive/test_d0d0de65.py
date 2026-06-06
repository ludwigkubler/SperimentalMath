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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def circuit_monotone_width(G):
        n = len(G)
        max_width = 0
        for i in range(n):
            width = 0
            visited = [False] * n
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    width += 1
                    for neighbor in G[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
            max_width = max(max_width, width)
        return max_width
    
    def minimal_hodge_cohomology(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        
        return gaussian_elimination(A)
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        
        G = [[] for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                G[u].append(v)
                G[v].append(u)
                edges.add((u, v))
        
        return G
    
    n_max = 40
    instances_tested = 30
    h_values = []
    w_values = []
    
    for _ in range(instances_tested):
        d = random.randint(2, min(n_max - 1, 5))  # Ensure d is at least 2 and n_max >= 40
        n = d * (d + 1) // 2
        G = generate_d_regular_graph(d, n)
        
        h = minimal_hodge_cohomology(G)
        w = circuit_monotone_width(G)
        
        h_values.append(h)
        w_values.append(w)
    
    correlation_coefficient = sum((h - mean_h) * (w - mean_w) for h, w in zip(h_values, w_values)) / instances_tested
    mean_h = sum(h_values) / instances_tested
    mean_w = sum(w_values) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(1.2 * w <= h <= 0.8 * w for h, w in zip(h_values, w_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation: {correlation_coefficient}, h(G) not in [1.2 * w(G), 0.8 * w(G)] for some G"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")