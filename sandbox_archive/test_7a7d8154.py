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
    
    def generate_3regular_graph(m):
        n = m * 2
        edges = []
        while len(edges) < n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return edges
    
    def edge_expansion(graph):
        m = len(graph)
        n = len(set(u for u, v in graph))
        min_ratio = float('inf')
        for size in range(1, n // 2 + 1):
            cuts = [set() for _ in range(n)]
            for u, v in graph:
                if len(cuts[u]) < size and len(cuts[v]) < size:
                    if len(cuts[u]) == size - 1:
                        cuts[v].add(v)
                    else:
                        cuts[u].add(u)
                    min_ratio = min(min_ratio, sum(1 for u, v in graph if (u in cuts[u] and v not in cuts[u]) or (v in cuts[v] and u not in cuts[v])) / size)
        return min_ratio
    
    def median_edge_bipartition(graph):
        edges = sorted(graph)
        mid = len(edges) // 2
        return edges[:mid], edges[mid:]
    
    def build_truth_table(G, sigma):
        n = len(G) * 2
        m = len(G)
        table = [[0] * (1 << m) for _ in range(1 << m)]
        for i in range(1 << m):
            assignment = [sigma[j // 2] if j % 2 == 0 else 1 - sigma[j // 2] for j in range(n)]
            for j in range(m):
                u, v = G[j]
                table[i][i ^ (1 << j)] += assignment[u] * assignment[v]
        return table
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for row in range(m):
                if row != pivot_row and matrix[row][col] != 0:
                    factor = matrix[row][col] / matrix[pivot_row][col]
                    for j in range(n):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
        return rank
    
    def log2(x):
        return math.log2(x)
    
    m_values = [4, 6, 8, 10, 12, 14]
    results = []
    
    for m in m_values:
        graph = generate_3regular_graph(m)
        sigma = [random.choice([0, 1]) for _ in range(m)]
        h_G = edge_expansion(graph)
        pi = median_edge_bipartition(graph)
        M = build_truth_table(graph, sigma)
        rank_real = matrix_rank(M)
        
        results.append({
            "metric_name": "log2_rank",
            "metric_value": log2(rank_real),
            "instances_tested": 1,
            "conjecture_holds": log2(rank_real) >= 0.25 * h_G * m,
            "counterexample": "" if log2(rank_real) >= 0.25 * h_G * m else f"m={m}, rank={rank_real}"
        })
    
    return {
        "seed": seed,
        "metric_values": [r["metric_value"] for r in results],
        "instances_tested": sum(r["instances_tested"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(sum(r["metric_values"]) / r["instances_tested"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((sum(r["metric_values"]) / r["instances_tested"] - mean_value)**2 for r in all_results)) / len(all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mismatched rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")