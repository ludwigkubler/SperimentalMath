# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges = set()
    while len(edges) < n * d // 2:
        u, v = random.sample(range(n), 2)
        if u == v or (u, v) in edges or (v, u) in edges:
            continue
        graph[u].append(v)
        graph[v].append(u)
        edges.add((u, v))
    return graph

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def symplectic_form_degree(A):
    n = len(A)
    C = [[A[i][j] if i < j else 0 for j in range(n)] for i in range(n)]
    C_inv = gaussian_elimination(C)
    rank = sum(1 for row in C_inv if any(row))
    return rank

def circuit_monotone_width(graph):
    n = len(graph)
    edges = [(u, v) for u in range(n) for v in graph[u] if u < v]
    m = len(edges)
    dp = [[0] * (1 << m) for _ in range(2)]
    dp[0][0] = 1
    for i in range(m):
        dp[1][i] = dp[0][i]
        for j in range((1 << i) - 1, -1, -1):
            if dp[0][j]:
                dp[1][i] += dp[0][j ^ (1 << i)]
    return max(dp[1])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 5))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    A = [[random.choice([-1, 1]) if i == j else 0 for j in range(n)] for i in range(n)]
    symplectic_deg = symplectic_form_degree(A)
    w_G = circuit_monotone_width(graph)
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": w_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": symplectic_deg >= d ** 0.5 and abs(w_G - d ** 0.5 * math.log(n)) / (d ** 0.5 * math.log(n)) <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 100))
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")