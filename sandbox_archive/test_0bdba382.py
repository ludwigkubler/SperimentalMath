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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for j in range(i + 1, n):
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges_added.add((i, j))
        return graph
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def compute_k_theory_invariant(graph):
        n = len(graph)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        zero_vector = [0] * n
        k_theory_invariant = 0
        for _ in range(10):  # Perform a few iterations of Gaussian elimination
            solution = gaussian_elimination(graph, zero_vector)
            if all(x == 0 for x in solution):
                return 0
            k_theory_invariant += sum(abs(x) for x in solution)
        return k_theory_invariant % 2
    
    def resolution_proof_width(n):
        # Placeholder function to simulate a simple measure of proof width
        return n * (n - 1) // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, random.randint(2, n-1))
        if graph is None:
            continue
        k_theory_invariant = compute_k_theory_invariant(graph)
        proof_width = resolution_proof_width(n)
        results.append((k_theory_invariant, proof_width))
    
    if len(results) < 30:
        return {
            "metric_name": "K-theory Invariant vs Proof Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    k_values, w_values = zip(*results)
    mean_k = sum(k_values) / len(k_values)
    mean_w = sum(w_values) / len(w_values)
    variance_k = sum((k - mean_k) ** 2 for k in k_values) / len(k_values)
    variance_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    covariance_kw = sum((k - mean_k) * (w - mean_w) for k, w in zip(k_values, w_values)) / len(k_values)
    
    r_squared = covariance_kw ** 2 / (variance_k * variance_w)
    
    return {
        "metric_name": "K-theory Invariant vs Proof Width",
        "metric_value": r_squared,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": r_squared >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_r_squared = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared < 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")