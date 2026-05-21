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
    
    def is_3_regular(G):
        degrees = [sum(1 for _ in neighbors) for _, neighbors in G.items()]
        return all(d == 3 for d in degrees)

    def generate_random_3_regular(n):
        while True:
            vertices = list(range(n))
            edges = []
            for v in vertices:
                neighbors = random.sample(vertices, 2)
                if (v, neighbors[0]) not in edges and (neighbors[0], v) not in edges:
                    edges.append((v, neighbors[0]))
                    edges.append((v, neighbors[1]))
            G = {v: set() for v in vertices}
            for u, v in edges:
                G[u].add(v)
                G[v].add(u)
            if is_3_regular(G):
                return G

    def adjacency_matrix(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i, neighbors in enumerate(G.values()):
            for j in neighbors:
                A[i][j] = 1
                A[j][i] = 1
        return A

    def hankel_matrix(A):
        n = len(A)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                H[i][j] = sum(A[k][l] for k, l in zip(range(i, n), range(j, n))) / n
        return H

    def eigenvalues(A):
        n = len(A)
        A_flat = [sum(row) for row in A]
        A_diag = [A[i][i] for i in range(n)]
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            Q[i][i] = 1
        for k in range(1, n):
            v = [A_flat[j] - A_diag[j] for j in range(k)] + [sum(A_flat[k:]) - sum(A_diag[k:])]
            u = [v[0]]
            for i in range(1, len(v)):
                u.append(v[i] - sum(u[j] * Q[i][j] for j in range(i)))
            norm_u = math.sqrt(sum(x**2 for x in u))
            for i in range(n):
                Q[i][k] = u[i] / norm_u
        eigenvals = [sum(A[i][j] * Q[i][k] * Q[j][k] for j in range(n)) for k in range(n)]
        return sorted(eigenvals, reverse=True)

    def max_cut(G):
        n = len(G)
        max_cut_size = 0
        for mask in range(1 << (n - 1)):
            cut_size = sum(1 for v in range(1, n) if (mask >> v) & 1 == 1 and any((v, u) in G[v] or (u, v) in G[u] for u in range(v)))
            max_cut_size = max(max_cut_size, cut_size)
        return max_cut_size

    def ub_dp(G):
        n = len(G)
        E = sum(len(neighbors) for _, neighbors in G.items()) // 2
        lambda_min = min(eigenvalues(adjacency_matrix(G)))
        return (E / 2) - (n / 4) * lambda_min

    def gw_slack(G):
        return ub_dp(G) - max_cut(G)

    n_values = [8, 10, 12, 14, 16, 18]
    results = []
    
    for n in n_values:
        for _ in range(30):
            G = generate_random_3_regular(n)
            A = adjacency_matrix(G)
            H = hankel_matrix(A)
            eigenvals = eigenvalues(A)
            ν_G = len(set(eigenvals))
            S_G = gw_slack(G)
            r_G = S_G / ν_G if ν_G > 0 else float('inf')
            results.append(r_G)

    min_r_G = min(results)
    mean_r_G = sum(results) / len(results)
    
    conjecture_holds = min_r_G >= 0.02 and mean_r_G <= 0.45
    counterexample = "" if conjecture_holds else f"min_r_G={min_r_G}, mean_r_G={mean_r_G}"
    
    return {
        "metric_name": "GW Slack / ν(G)",
        "metric_value": mean_r_G,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    min_r_G = min(r["metric_value"] for r in results if r["conjecture_holds"])
    mean_r_G = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_G:.4f} std={0:.4f} support_fraction={support_fraction:.2f}")
    elif any(r["metric_value"] < 0.02 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_r_G={min_r_G:.4f}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")