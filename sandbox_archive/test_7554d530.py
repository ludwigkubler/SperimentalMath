# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_connected_graph(n, d):
    while True:
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < d:
                    edges.add((i, j))
        if len(edges) == 0:
            continue
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adj[node])
        if len(visited) == n:
            return edges

def compute_cut_polynomial(G, n):
    cut_sizes = defaultdict(int)
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for u, v in G:
            if (u in S) != (v in S):
                cut_size += 1
        cut_sizes[cut_size] += 1
    return cut_sizes

def durand_kerner(coeffs, max_iter=80):
    degree = len(coeffs) - 1
    if degree == 0:
        return []
    roots = [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(degree)]
    for _ in range(max_iter):
        new_roots = []
        for i, z in enumerate(roots):
            numerator = 0 + 0j
            denominator = 1 + 0j
            for j, w in enumerate(roots):
                if i != j:
                    denominator *= (z - w)
            if denominator == 0:
                continue
            numerator = sum(coeffs[k] * z**(degree - k) for k in range(degree + 1))
            new_z = z - numerator / denominator
            new_roots.append(new_z)
        roots = new_roots
    return roots

def compute_ly(G, n):
    cut_sizes = compute_cut_polynomial(G, n)
    coeffs = [0.0] * (max(cut_sizes.keys()) + 1)
    for k, v in cut_sizes.items():
        coeffs[k] = float(v)
    roots = durand_kerner(coeffs)
    if not roots:
        return 0.0
    min_dist = min((abs(z + 1) / (1 + abs(z))) for z in roots)
    return min_dist

def power_iteration(M, max_iter=100, tol=1e-6):
    n = len(M)
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [0.0] * n
        for i in range(n):
            for j in range(n):
                b_k1[i] += M[i][j] * b_k[j]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        if norm == 0:
            break
        b_k1 = [x / norm for x in b_k1]
        if sum(abs(b_k1[i] - b_k[i]) for i in range(n)) < tol:
            break
        b_k = b_k1
    lambda_max = sum(M[i][i] * b_k[i] for i in range(n))
    return lambda_max

def compute_laplacian(G, n):
    L = [[0.0] * n for _ in range(n)]
    for u, v in G:
        L[u][u] += 1
        L[v][v] += 1
        L[u][v] = -1
        L[v][u] = -1
    return L

def compute_max_cut(G, n):
    max_cut = 0
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for u, v in G:
            if (u in S) != (v in S):
                cut_size += 1
        if cut_size > max_cut:
            max_cut = cut_size
    return max_cut

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    densities = [0.25, 0.4, 0.6]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    c_values = [0.01, 0.05, 0.1, 0.5, 1.0]

    for n in n_values:
        for d in densities:
            for _ in range(30):
                G = generate_connected_graph(n, d)
                if not G:
                    continue
                instances_tested += 1
                ly = compute_ly(G, n)
                L = compute_laplacian(G, n)
                lambda_max = power_iteration(L)
                dp = (n / 4) * lambda_max
                tau_star = compute_max_cut(G, n)
                delta = dp - tau_star
                edge_count = len(G)
                if edge_count == 0:
                    continue
                metric_value = delta / (edge_count * ly**2)
                metric_values.append(metric_value)
                if metric_value < 0.01:
                    conjecture_holds = False
                    counterexample = f"n={n}, d={d}, seed={seed}, delta={delta}, edge_count={edge_count}, ly={ly}, metric_value={metric_value}"
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "delta / (edge_count * ly^2)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "delta / (edge_count * ly^2)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((trial["seed"] for trial in trials if not trial["conjecture_holds"]), None)
        counterexample = next((trial["counterexample"] for trial in trials if not trial["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")