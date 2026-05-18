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

def generate_connected_graph(n, edge_prob):
    while True:
        adj = defaultdict(set)
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < edge_prob:
                    adj[i].add(j)
                    adj[j].add(i)
                    edges.add((i, j))
        if len(edges) == 0:
            continue
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adj[node] - visited)
        if len(visited) == n:
            return adj, edges

def compute_cut_polynomial(G, n):
    max_cut_size = 0
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i in S) != (j in S) and j in G[i]:
                    cut_size += 1
        if cut_size > max_cut_size:
            max_cut_size = cut_size
    poly = [0] * (max_cut_size + 1)
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i in S) != (j in S) and j in G[i]:
                    cut_size += 1
        poly[cut_size] += 1
    return poly

def compute_ly(poly):
    if not poly:
        return 0.0
    roots = durand_kerner(poly)
    min_dist = float('inf')
    for root in roots:
        dist = abs(root + 1) / (1 + abs(root))
        if dist < min_dist:
            min_dist = dist
    return min_dist

def durand_kerner(poly, max_iter=80):
    n = len(poly) - 1
    if n == 0:
        return []
    roots = [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    for _ in range(max_iter):
        new_roots = []
        for i, root in enumerate(roots):
            numerator = denominator = 1.0
            for j, other_root in enumerate(roots):
                if i != j:
                    numerator *= (root - other_root)
                    denominator *= (root - other_root)
            if denominator == 0:
                continue
            new_root = root - numerator / denominator
            new_roots.append(new_root)
        roots = new_roots
    return roots

def compute_max_cut(G, n):
    max_cut = 0
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i in S) != (j in S) and j in G[i]:
                    cut_size += 1
        if cut_size > max_cut:
            max_cut = cut_size
    return max_cut

def compute_laplacian_eigenvalue(G, n):
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = len(G[i])
        for j in G[i]:
            L[i][j] -= 1
    eigenvalue = power_iteration(L, n)
    return eigenvalue

def power_iteration(matrix, n, max_iter=100, tol=1e-6):
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [0.0] * n
        for i in range(n):
            for j in range(n):
                b_k1[i] += matrix[i][j] * b_k[j]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        if norm == 0:
            break
        b_k1 = [x / norm for x in b_k1]
        if sum(abs(b_k1[i] - b_k[i]) for i in range(n)) < tol:
            break
        b_k = b_k1
    eigenvalue = 0.0
    for i in range(n):
        for j in range(n):
            eigenvalue += b_k[i] * matrix[i][j] * b_k[j]
    return eigenvalue

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    edge_densities = [0.25, 0.4, 0.6]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    c_values = [0.01, 0.05, 0.1, 0.5, 1.0]
    for n in n_values:
        for d in edge_densities:
            for _ in range(30):
                G, edges = generate_connected_graph(n, d)
                poly = compute_cut_polynomial(G, n)
                ly = compute_ly(poly)
                max_cut = compute_max_cut(G, n)
                laplacian_eigenvalue = compute_laplacian_eigenvalue(G, n)
                dp = (n / 4) * laplacian_eigenvalue
                delta = dp - max_cut
                term = len(edges) * ly**2
                if term == 0:
                    continue
                ratio = delta / term
                metric_values.append(ratio)
                instances_tested += 1
                if any(ratio < c for c in c_values):
                    conjecture_holds = False
                    counterexample = f"n={n}, d={d}, seed={seed}, ratio={ratio}"
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break
    if not metric_values:
        return {
            "metric_name": "DP(G) - τ*(G) / (|E|·LY(G)²)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "DP(G) - τ*(G) / (|E|·LY(G)²)",
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
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")