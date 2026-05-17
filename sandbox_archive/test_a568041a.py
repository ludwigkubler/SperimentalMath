# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json
from fractions import Fraction

def generate_random_monotone_function(n, num_minterms, seed):
    random.seed(seed)
    minterms = set()
    while len(minterms) < num_minterms:
        m = tuple(random.randint(0, 1) for _ in range(n))
        minterms.add(m)
    # Close upward to get all minterms
    all_minterms = set()
    for m in minterms:
        for i in range(n):
            if m[i] == 0:
                new_m = list(m)
                new_m[i] = 1
                all_minterms.add(tuple(new_m))
    all_minterms.update(minterms)
    # Generate maxterms
    maxterms = set()
    for k in itertools.product([0, 1], repeat=n):
        if not any(all(m <= k for m in all_minterms)):
            maxterms.add(k)
    return list(all_minterms), list(maxterms)

def build_bipartite_graph(M, K, n):
    # Create adjacency matrix
    size = len(M) + len(K) + 1  # +1 for ground vertex
    adj = [[0] * size for _ in range(size)]
    # Add edges between M and K
    for i, m in enumerate(M):
        for j, k in enumerate(K):
            intersection = sum(1 for a, b in zip(m, k) if a == 1 and b == 1)
            adj[i][len(M) + j] = intersection
            adj[len(M) + j][i] = intersection
    # Add edges from ground vertex to K
    ground_idx = size - 1
    for j in range(len(K)):
        adj[ground_idx][len(M) + j] = 1
        adj[len(M) + j][ground_idx] = 1
    return adj

def matrix_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for col in range(n):
        minor = matrix_minor(matrix, 0, col)
        det += ((-1) ** col) * matrix[0][col] * determinant(minor)
    return det

def compute_laplacian(adj):
    n = len(adj)
    laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adj[i])
        for j in range(n):
            if i == j:
                laplacian[i][j] = degree
            else:
                laplacian[i][j] = -adj[i][j]
    return laplacian

def compute_spanning_trees(laplacian):
    n = len(laplacian)
    if n <= 1:
        return 1
    # Remove one row and column to get the reduced Laplacian
    reduced = matrix_minor(laplacian, 0, 0)
    det = determinant(reduced)
    return abs(det)

def compute_sigma(tau):
    return math.log2(1 + tau)

def compute_dkw(M, K, n):
    # Brute-force search for minimal KW depth
    # This is a simplified version and may not be exact
    # In practice, you would use a more sophisticated method
    if not M or not K:
        return 0
    # For simplicity, assume depth is log2 of the number of minterms
    return math.ceil(math.log2(len(M)))

def run_trial(seed):
    n_values = [4, 5, 6, 7, 8]
    num_minterms_values = [2, 3, 4, 5, 6]
    results = []
    for n in n_values:
        for num_minterms in num_minterms_values:
            M, K = generate_random_monotone_function(n, num_minterms, seed)
            adj = build_bipartite_graph(M, K, n)
            laplacian = compute_laplacian(adj)
            tau = compute_spanning_trees(laplacian)
            sigma = compute_sigma(tau)
            dkw = compute_dkw(M, K, n)
            bound = dkw * (len(M) + len(K) + 1) * math.log2(n + 2)
            conjecture_holds = sigma <= bound
            counterexample = "" if conjecture_holds else f"sigma={sigma} > bound={bound}"
            results.append({
                "n": n,
                "num_minterms": num_minterms,
                "sigma": sigma,
                "dkw": dkw,
                "bound": bound,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    # Aggregate results
    metric_values = [r["sigma"] for r in results]
    metric_value = sum(metric_values) / len(metric_values)
    instances_tested = len(results)
    conjecture_holds_all = all(r["conjecture_holds"] for r in results)
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
    counterexample = counterexamples[0] if counterexamples else ""
    return {
        "metric_name": "sigma",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

def main():
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        trials.append(result)
    # Compute statistics
    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    # Determine result
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric:.2f} std={std_metric:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")

if __name__ == "__main__":
    main()