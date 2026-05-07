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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def hashimoto_operator(G):
    V, E = G
    n, m = len(V), len(E)
    B = [[0] * (2*m) for _ in range(2*m)]
    for i, (u, v) in enumerate(E):
        B[2*i][2*i+1] = 1
        B[2*i+1][2*i] = 1
        B[2*i][2*m + 2*v] = 1
        B[2*m + 2*u][2*i+1] = 1
    return B

def spectral_radius(M):
    n = len(M)
    eigenvalues = gaussian_elimination(M)
    max_real_part = -float('inf')
    for row in eigenvalues:
        real_part = sum(row[i] * row[j] / (i + j) for i, j in zip(range(n), range(n)))
        if real_part > max_real_part:
            max_real_part = real_part
    return max_real_part

def dpll_node_count(G, sigma):
    V, E = G
    n = len(V)
    stack = [(0, set(), 0)]
    while stack:
        node, covered, depth = stack.pop()
        if node == n:
            return depth
        for neighbor in range(n):
            if (node, neighbor) not in E and (neighbor, node) not in E:
                continue
            if sigma[node] != sigma[neighbor]:
                new_covered = covered.union({(node, neighbor)})
                stack.append((neighbor + 1, new_covered, depth + 1))
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    graph_families = [
        lambda n: ([i for i in range(n)], [(i, (i+1)%n) for i in range(n)]),
        lambda n: ([0] + [i for i in range(2, n//2+1)] + [n-1], [(0, 1), (0, n-1)] + [(i, i+1) for i in range(1, n//2)] + [(n-2, n-1)]),
        lambda n: ([i for i in range(n)], [(i, j) for i in range(n) for j in range(i+1, n) if (i+j)%3 == 0]),
        lambda n: ([i for i in range(n)], [(i, j) for i in range(n) for j in range(i+1, n) if (i+j)%4 == 0]),
        lambda n: ([i for i in range(n//2)] + [i+n//2 for i in range(n//2)], [(i, i+n//2) for i in range(n//2)]),
    ]
    graph_sizes = [8, 12, 16, 20, 28, 36]
    results = []
    for G_func in graph_families:
        for n in graph_sizes:
            for _ in range(30):
                V, E = G_func(n)
                sigma = {v: random.randint(0, 1) for v in V}
                B_G = hashimoto_operator((V, E))
                lambda_values = spectral_radius(B_G)
                nu_G = math.log(abs(lambda_values)) - math.log(max([abs(lam) for lam in lambda_values if lam != lambda_values[0] and abs(lam) != 1], default=1))
                if nu_G < 0:
                    nu_G = 0
                nodes = dpll_node_count((V, E), sigma)
                log_nodes = math.log2(nodes)
                results.append({
                    "metric_name": "log2(DPLL_nodes)",
                    "metric_value": log_nodes,
                    "instances_tested": 1,
                    "conjecture_holds": nu_G > 0.1 * math.log(n),
                    "counterexample": "" if nu_G < 0.1 * math.log(n) else f"nu(G)={nu_G}, n={n}"
                })
    return {
        "metric_name": "log2(DPLL_nodes)",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        all_results.append(result)
    mean_metric = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in all_results):
        first_failing_seed = next((r["seed"] for r in all_results if r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")