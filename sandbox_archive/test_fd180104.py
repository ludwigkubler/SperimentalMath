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
        adj = defaultdict(set)
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adj[node] - visited)
        if len(visited) == n:
            return edges

def evaluate_polynomial(poly, z):
    result = 0
    for k, c in enumerate(poly):
        if abs(z) > 1e100:
            z = z / abs(z) * 1e100
        result += c * (z ** k)
    return result

def durand_kerner(poly, max_iter=80):
    n = len(poly) - 1
    roots = [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    for _ in range(max_iter):
        new_roots = []
        for i in range(n):
            numerator = evaluate_polynomial(poly, roots[i])
            denominator = 1.0
            for j in range(n):
                if i != j:
                    denominator *= (roots[i] - roots[j])
            new_roots.append(roots[i] - numerator / denominator)
        roots = new_roots
    return roots

def compute_cut_polynomial(G, n):
    poly = [0] * (n + 1)
    for S in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in range(n + 1)):
        cut_size = 0
        for u, v in G:
            if (u in S) != (v in S):
                cut_size += 1
        poly[cut_size] += 1
    return poly

def compute_ly(G, n):
    poly = compute_cut_polynomial(G, n)
    roots = durand_kerner(poly)
    min_dist = float('inf')
    for z in roots:
        dist = abs(z + 1) / (1 + abs(z))
        if dist < min_dist:
            min_dist = dist
    return min_dist

def power_iteration(M, max_iter=100, tol=1e-6):
    n = len(M)
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [sum(M[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k1 = [x / norm for x in b_k1]
        if sum((b_k1[i] - b_k[i])**2 for i in range(n)) < tol:
            break
        b_k = b_k1
    return sum(b_k[i] * b_k[i] for i in range(n))

def compute_laplacian(G, n):
    L = [[0] * n for _ in range(n)]
    for u, v in G:
        L[u][u] += 1
        L[v][v] += 1
        L[u][v] -= 1
        L[v][u] -= 1
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
            metric_value = delta / (len(G) * ly**2)
            metric_values.append(metric_value)

            for c in c_values:
                if delta < c * len(G) * ly**2:
                    conjecture_holds = False
                    counterexample = f"n={n}, d={d}, delta={delta}, c={c}, ly={ly}"
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "max_cut_sos2_gap",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no valid graphs generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "max_cut_sos2_gap",
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

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")