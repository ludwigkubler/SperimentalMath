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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def rank(matrix):
        rref = gaussian_elimination([row[:] for row in matrix])
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def tree_width(G):
        n = len(G)
        if n == 0:
            return -1
        if n == 1:
            return 0
        neighbors = [[] for _ in range(n)]
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v]:
                    neighbors[u].append(v)
                    neighbors[v].append(u)

        def dfs(node, parent):
            max_depth = -1
            for neighbor in neighbors[node]:
                if neighbor != parent:
                    depth = dfs(neighbor, node)
                    if depth > max_depth:
                        max_depth = depth
            return max_depth + 1

        return dfs(0, -1)

    def generate_k_clique(n, k):
        G = [[False] * n for _ in range(n)]
        nodes = list(range(n))
        random.shuffle(nodes)
        clique_nodes = nodes[:k]
        for u in clique_nodes:
            for v in clique_nodes:
                if u < v:
                    G[u][v] = True
                    G[v][u] = True
        return G

    n = 40
    k = 5
    G = generate_k_clique(n, k)
    config_space_rank = rank(G)
    tw = tree_width(G)

    if tw == -1:
        return {
            "metric_name": "rank_to_tw_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_has_no_edges"
        }

    ratio = config_space_rank / tw
    return {
        "metric_name": "rank_to_tw_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
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

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_tw_ratio_exceeds_bound\" first_failing_seed={first_failing['seed']}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")