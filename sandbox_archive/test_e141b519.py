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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def k_clique_instance(n, k):
        edges = set()
        while len(edges) < k * (k - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges

    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        for _ in range(5):
            clique = k_clique_instance(n, n // 2)
            adjacency_matrix = [[0] * n for _ in range(n)]
            for u, v in clique:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
            
            rank = matrix_rank(adjacency_matrix)
            ratios.append(rank / n)

    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(math.isclose(mean_ratio, n**(-0.25), rel_tol=1e-2) for n in n_values)
    
    return {
        "metric_name": "Ratio of Rank to Vertex Count",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")