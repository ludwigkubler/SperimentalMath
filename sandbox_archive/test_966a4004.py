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

def generate_connected_graph(n, d, seed):
    random.seed(seed)
    adj = [[0]*n for _ in range(n)]
    edges = set()

    # Generate a random spanning tree
    for i in range(1, n):
        j = random.randint(0, i-1)
        adj[i][j] = adj[j][i] = 1
        edges.add((min(i, j), max(i, j)))

    # Add additional edges until density d is reached
    max_edges = n*(n-1)//2
    target_edges = int(d * max_edges)
    while len(edges) < target_edges:
        i, j = random.sample(range(n), 2)
        if i != j and adj[i][j] == 0:
            adj[i][j] = adj[j][i] = 1
            edges.add((min(i, j), max(i, j)))

    return adj

def compute_cut_polynomial(adj):
    n = len(adj)
    coeffs = defaultdict(int)

    for S in itertools.product([0, 1], repeat=n):
        if sum(S) == 0 or sum(S) == n:
            continue
        cut_size = 0
        for i in range(n):
            for j in range(i+1, n):
                if adj[i][j] and S[i] != S[j]:
                    cut_size += 1
        coeffs[cut_size] += 1

    return sorted(coeffs.items())

def evaluate_polynomial(poly, z):
    result = 0.0
    for k, c in poly:
        result += c * (z ** k)
    return result

def durand_kerner(poly, max_iter=80):
    n = len(poly) - 1
    if n == 0:
        return []

    # Initial guesses
    roots = [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]

    for _ in range(max_iter):
        new_roots = []
        for i in range(n):
            numerator = evaluate_polynomial(poly, roots[i])
            denominator = 1.0
            for j in range(n):
                if i != j:
                    denominator *= (roots[i] - roots[j])
            new_root = roots[i] - numerator / denominator
            new_roots.append(new_root)
        roots = new_roots

    return roots

def compute_ly(roots):
    if not roots:
        return 0.0

    min_dist = float('inf')
    for z in roots:
        if z == -1:
            continue
        dist = abs(z + 1) / (1 + abs(z))
        if dist < min_dist:
            min_dist = dist

    return min_dist

def power_iteration(M, max_iter=100, tol=1e-6):
    n = len(M)
    b = [random.uniform(-1, 1) for _ in range(n)]

    for _ in range(max_iter):
        new_b = [0.0] * n
        for i in range(n):
            for j in range(n):
                new_b[i] += M[i][j] * b[j]

        norm = math.sqrt(sum(x**2 for x in new_b))
        if norm == 0:
            break
        new_b = [x / norm for x in new_b]

        if sum(abs(new_b[i] - b[i]) for i in range(n)) < tol:
            break

        b = new_b

    eigenvalue = sum(b[i] * sum(M[i][j] * b[j] for j in range(n)) for i in range(n))
    return eigenvalue

def compute_laplacian(adj):
    n = len(adj)
    L = [[0.0]*n for _ in range(n)]
    degrees = [sum(row) for row in adj]

    for i in range(n):
        for j in range(n):
            if i == j:
                L[i][j] = degrees[i]
            elif adj[i][j] == 1:
                L[i][j] = -1

    return L

def compute_max_cut(adj):
    n = len(adj)
    max_cut = 0

    for S in itertools.product([0, 1], repeat=n):
        if sum(S) == 0 or sum(S) == n:
            continue
        cut_size = 0
        for i in range(n):
            for j in range(i+1, n):
                if adj[i][j] and S[i] != S[j]:
                    cut_size += 1
        if cut_size > max_cut:
            max_cut = cut_size

    return max_cut

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    densities = [0.25, 0.4, 0.6]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for d in densities:
            adj = generate_connected_graph(n, d, seed)
            poly = compute_cut_polynomial(adj)
            roots = durand_kerner(poly)
            ly = compute_ly(roots)
            L = compute_laplacian(adj)
            lambda_max = power_iteration(L)
            tau_star = compute_max_cut(adj)
            edge_count = sum(sum(row) for row in adj) // 2
            dp = (n / 4) * lambda_max
            delta = dp - tau_star

            if edge_count == 0 or ly == 0:
                continue

            metric_value = delta / (edge_count * ly**2)
            metric_values.append(metric_value)
            instances_tested += 1

            if metric_value < 0.01:
                conjecture_holds = False
                counterexample = f"n={n}, d={d}, seed={seed}, delta={delta}, edge_count={edge_count}, ly={ly}, metric_value={metric_value}"

    if not metric_values:
        return {
            "metric_name": "delta / (edge_count * ly^2)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    avg_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "delta / (edge_count * ly^2)",
        "metric_value": avg_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [821, 877, 929, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109]

    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((trial["seed"] for trial in trials if not trial["conjecture_holds"]), None)
        if first_failing_seed is not None:
            print(f"RESULT: FALSIFIED counterexample=\"{trials[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=no_failing_seed_found")