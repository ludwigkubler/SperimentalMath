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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, cols):
                matrix[i][j] /= pivot
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, cols):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def communication_complexity_rank(G):
        n = len(G)
        edges = [(u, v) for u in range(n//2) for v in range(n//2, n)]
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = 1
            B[v][u] = 1
        H = [A[i] + B[i] for i in range(n)]
        return gaussian_elimination(H)
    
    def minimal_hodge_arcs(A, B, edges):
        n = len(A)
        H = [[0] * n for _ in range(n)]
        for u, v in edges:
            H[u][v] = 1
            H[v][u] = 1
        return gaussian_elimination(H)
    
    def generate_bipartite_graph(n, delta):
        A = [set() for _ in range(n//2)]
        B = [set() for _ in range(n//2)]
        edges = []
        for u in range(n//2):
            for v in range(n//2, n):
                if len(A[u]) < delta and len(B[v]) < delta:
                    A[u].add(v)
                    B[v].add(u)
                    edges.append((u, v))
        return A, B, edges
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_arcs = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            A, B, edges = generate_bipartite_graph(n, random.randint(2, min(n//2 - 1, delta)))
            hodge_arcs = minimal_hodge_arcs(A, B, edges)
            rank = communication_complexity_rank((A, B))
            total_hodge_arcs += hodge_arcs
            total_rank += rank
            instances_tested += 1
    
    mean_hodge_arcs = total_hodge_arcs / instances_tested
    mean_rank = total_rank / instances_tested
    ratio_mean = mean_hodge_arcs / mean_rank if mean_rank != 0 else float('inf')
    
    conjecture_holds = ratio_mean >= 0.5 and all(0.1 <= rank <= 2 * hodge_arcs for hodge_arcs, rank in zip(hodge_arcs_list, rank_list))
    
    return {
        "metric_name": "Ratio of Hodge Arcs to Rank",
        "metric_value": ratio_mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["metric_value"] < 0.1 or r["rank"] > 2 * r["hodge_arcs"] for r in results):
        print(f"RESULT: FALSIFIED counterexample='ratio_too_low' first_failing_seed={seeds[next(i for i, r in enumerate(results) if r['metric_value'] < 0.1 or r['rank'] > 2 * r['hodge_arcs'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")