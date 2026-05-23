# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def tree_width(graph):
        n = len(graph)
        if n == 0:
            return -1
        edges = [set() for _ in range(n)]
        for u, v in graph:
            edges[u].add(v)
            edges[v].add(u)
        
        def dfs(node, parent):
            max_size = 0
            sizes = []
            for neighbor in edges[node]:
                if neighbor != parent:
                    size = dfs(neighbor, node) + 1
                    sizes.append(size)
                    max_size = max(max_size, size)
            sizes.sort(reverse=True)
            return max_size
        
        return dfs(0, -1)
    
    def k_clique_instance(n):
        graph = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    graph.append((i, j))
        return graph
    
    def config_space_rank(graph):
        n = len(graph)
        vertices = list(range(n))
        edges = set(graph)
        
        def homology_group(vertices, edges):
            m = len(edges)
            if m == 0:
                return 1
            matrix = [[0] * (m + 1) for _ in range(m)]
            for i, (u, v) in enumerate(edges):
                matrix[i][i] = -1
                matrix[i][vertices.index(u)] = 1
                matrix[i][vertices.index(v)] = 1
            
            return gaussian_elimination(matrix)
        
        rank = homology_group(vertices, edges)
        return rank
    
    k = 3
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = k_clique_instance(n)
    tw = tree_width(graph)
    rank = config_space_rank(graph)
    
    if tw == -1:
        return {
            "metric_name": "rank/tw_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = Fraction(rank, tw)
    return {
        "metric_name": "rank/tw_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * tw + 0.1,
        "counterexample": "" if rank <= 2 * tw + 0.1 else f"Ratio {rank}/{tw} > 2*{tw}+0.1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough seeds supported\" first_failing_seed=1")
    else:
        print("RESULT: INCONCLUSIVE some results are None due to undefined mapping")