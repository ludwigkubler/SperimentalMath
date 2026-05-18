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
    def generate_random_3regular_graph(n):
        while True:
            edges = set()
            for _ in range(n * 3 // 2):
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
            adj = [set() for _ in range(n)]
            for u, v in edges:
                adj[u].add(v)
                adj[v].add(u)
            if all(len(neighbors) == 3 for neighbors in adj):
                return adj

    def laplacian_matrix(adj):
        n = len(adj)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = len(adj[i])
            L[i][i] = degree
            for j in adj[i]:
                L[i][j] = -1
        return L

    def max_cut_exact(adj):
        n = len(adj)
        best_cut_value = 0

        def dfs(node, visited, cut_set):
            visited[node] = True
            cut_set.add(node)
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited, cut_set)

        for start_node in range(n):
            visited = [False] * n
            cut_set = set()
            dfs(start_node, visited, cut_set)
            cut_value = sum(len(adj[v]) - len(cut_set.intersection(adj[v])) for v in cut_set) / 2
            best_cut_value = max(best_cut_value, cut_value)

        return best_cut_value

    def spectral_norm(A):
        n = len(A)
        x = [1] * n
        y = [0] * n
        for _ in range(10):  # Power iteration method
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            norm_y = sum(y[i] ** 2 for i in range(n))
            if norm_y == 0:
                return 0
            x = [y[i] / math.sqrt(norm_y) for i in range(n)]
        return max(abs(sum(A[i][j] * x[j] for j in range(n))) for i in range(n))

    def sign_rounding_value(adj, eigenvector):
        n = len(eigenvector)
        cut_set = [i if eigenvector[i] > 0 else -1 for i in range(n)]
        return sum(len(adj[v]) - len(set(cut_set[i] for i in adj[v])) for v in set(i for i, x in enumerate(cut_set) if x != -1)) / 2

    def kashin_l1_defect(eigenvector):
        n = len(eigenvector)
        return 2 * (1 - sum(abs(x) for x in eigenvector) / math.sqrt(n))

    random.seed(seed)
    n_values = [10, 14, 18, 22]
    results = []
    instances_tested = 0
    max_violation_gap = 0

    for n in n_values:
        for _ in range(30):
            adj = generate_random_3regular_graph(n)
            L = laplacian_matrix(adj)
            lambda_max = spectral_norm(L)
            eigenvector = [x[1] for x in sorted(zip(eigenvector, range(n)), key=lambda x: -abs(x[0]))]
            eigenvector = [eigenvector[i] / math.sqrt(sum(x**2 for x in eigenvector)) for i in range(n)]
            kappa = kashin_l1_defect(eigenvector)
            if kappa == 0:
                continue
            MC = max_cut_exact(adj)
            rho = (n * lambda_max / 4) / MC - 1
            instances_tested += 1
            results.append({
                "metric_name": "rho_over_kappa",
                "metric_value": rho / kappa,
                "instances_tested": instances_tested,
                "conjecture_holds": rho <= 16 * kappa,
                "counterexample": f"n={n}, rho={rho}, kappa={kappa}" if rho > 16 * kappa else ""
            })
            max_violation_gap = max(max_violation_gap, abs(rho - 16 * kappa))

    mean_value = sum(result["metric_value"] for result in results) / instances_tested
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / instances_tested)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    return {
        "metric_name": "rho_over_kappa",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": max_violation_gap > 0 and f"max violation gap={max_violation_gap}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        max_violation_gap = max(abs(result["metric_value"] - 16) for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=max violation gap={max_violation_gap} first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown_failure_mode")