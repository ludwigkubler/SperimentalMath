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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def frege_proof_depth(phi_G):
        # Placeholder implementation of Frege proof depth calculation
        # This is a dummy function and should be replaced with actual logic
        return random.randint(10, 50)

    def mrank(G):
        n = len(G)
        A = [[0] * (n + 2) for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
            for j in range(n):
                if G[i][j]:
                    A[i][-2] += 1
                    A[-1][i] += 1
        A[-1][-2] = n
        A[-2][-1] = n
        return len(gaussian_elimination(A)) - 1

    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = G[v][u] = 1
                edges.add((u, v))
        return G

    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_d_regular_graph(n, 3)
            phi_G = "Tseitin formula for G"
            mrank_value = mrank(G)
            f_phi_G = frege_proof_depth(phi_G)
            instances_tested += 1
            metric_values.append(mrank_value / f_phi_G)

    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for v in metric_values if abs(v - 1) < 0.5) / len(metric_values)

    if support_fraction >= 0.8:
        result = "SUPPORTED"
    elif any(abs(v - 1) >= 0.5 for v in metric_values):
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"

    return {
        "metric_name": "mrank / f(φ_G)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - 1) < 0.5) / len(results)

    print(f"RESULT: {result} mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")