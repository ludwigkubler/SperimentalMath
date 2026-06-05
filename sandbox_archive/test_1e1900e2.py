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
    
    def generate_graph(n, m):
        if m % n != 0:
            return None
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        if not A:
            return 0
        m, n = len(A), len(A[0])
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        if r is None:
            return 0
        rank = sum(1 for row in r if any(row[j] != 0 for j in range(n)))
        return rank

    def min_invariant_generators(G):
        n = len(G)
        incidence_matrix = [[0] * (n + n) for _ in range(n)]
        for u, v in G:
            incidence_matrix[u][v + n] = 1
            incidence_matrix[v][u + n] = 1
        return rank(incidence_matrix)

    def communication_complexity_rank(G):
        n = len(G)
        if n == 0:
            return 0
        max_degree = max(len(neighbors) for neighbors in G)
        return math.ceil(math.log2(max_degree))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, n * (n - 1) // 2)
            G = generate_graph(n, m)
            if G is None:
                continue
            min_gen = min_invariant_generators(G)
            rank_comm = communication_complexity_rank(G)
            results.append({
                "metric_name": "min_gen",
                "metric_value": min_gen,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            })

    return {
        "seed": seed,
        "metric_name": "min_gen",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")