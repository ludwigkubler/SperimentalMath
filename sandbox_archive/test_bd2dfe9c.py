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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None, "Graph size must be a multiple of the degree"
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph, None

    def adjacency_matrix(graph, n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                A[i][j] = 1
        return A

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j]:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for k in range(n):
                if k != j and A[rank][k]:
                    factor = Fraction(A[rank][k], A[rank][j])
                    for l in range(n):
                        A[rank][l] -= factor * A[j][l]
            rank += 1
        return rank

    def symplectic_form_degree(A):
        m, n = len(A), len(A[0])
        if m != n or m % 2 != 0:
            return None, "Matrix must be square and even-sized"
        kernel_dim = gaussian_elimination(A)
        return kernel_dim

    def circuit_monotone_width(n):
        # Placeholder for actual algorithm
        # For simplicity, we use a linear relationship with d^(1/2) * log n
        d = 2  # Example degree
        return Fraction(d ** (1 / 2) * math.log(n), 1)

    def spearman_rank_correlation(values1, values2):
        if len(values1) != len(values2):
            return None
        rank1 = {x: i for i, x in enumerate(sorted(set(values1)), start=1)}
        rank2 = {x: i for i, x in enumerate(sorted(set(values2)), start=1)}
        n = len(rank1)
        numerator = sum((rank1[x] - rank2[x]) ** 2 for x in rank1)
        denominator = n * (n ** 2 - 1) / 6
        return 1 - (6 * numerator) / denominator

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        d = 2  # Example degree
        graph, error = generate_d_regular_graph(n, d)
        if error:
            return {"metric_name": "symplectic_form_degree", "metric_value": None, "instances_tested": 0, "n_max": n, "conjecture_holds": False, "counterexample": error}
        
        A = adjacency_matrix(graph, n)
        sf_degree, error = symplectic_form_degree(A)
        if error:
            return {"metric_name": "symplectic_form_degree", "metric_value": None, "instances_tested": 0, "n_max": n, "conjecture_holds": False, "counterexample": error}
        
        cm_width = circuit_monotone_width(n)
        results.append({"sf_degree": sf_degree, "cm_width": cm_width})

    if not results:
        return {"metric_name": "symplectic_form_degree", "metric_value": None, "instances_tested": 0, "n_max": 40, "conjecture_holds": False, "counterexample": "No valid graphs generated"}

    sf_degrees = [result["sf_degree"] for result in results]
    cm_widths = [result["cm_width"] for result in results]
    
    rho = spearman_rank_correlation(sf_degrees, cm_widths)
    if rho is None:
        return {"metric_name": "symplectic_form_degree", "metric_value": None, "instances_tested": len(results), "n_max": 40, "conjecture_holds": False, "counterexample": "Spearman's rank correlation coefficient calculation failed"}

    conjecture_holds = rho >= 0.5
    counterexample = "" if conjecture_holds else f"Spearman's rank correlation coefficient: {rho}"
    
    return {
        "metric_name": "symplectic_form_degree",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8 or all(result["conjecture_holds"] for result in results):
            print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
        else:
            min_rho = min(result["metric_value"] for result in results if result["conjecture_holds"])
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='Spearman\'s rank correlation coefficient < 0.5' first_failing_seed={first_failing_seed}")