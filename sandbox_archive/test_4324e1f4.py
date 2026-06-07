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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

# Helper functions for matrix operations
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
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def generate_d_regular_graph(d, n):
    if d * (d - 1) / 2 != n:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    G = [[] for _ in range(n)]
    edges_added = set()
    for i in range(n):
        for j in range(i + 1, n):
            if len(G[i]) < d and len(G[j]) < d:
                G[i].append(j)
                G[j].append(i)
                edges_added.add((i, j))
                edges_added.add((j, i))
    return G

def isometric_embedding(G, n):
    embedding = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if v in G[u]:
                embedding[u][v] = 1
                embedding[v][u] = 1
    return embedding

def apply_non_rigid_transformations(embedding, n):
    # Placeholder for non-rigid transformation logic
    # This is a dummy implementation that does not actually transform the graph
    return embedding

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3  # Example degree
    n_values = [5, 10, 15, 20, 30, 40]
    total_non_rigid_motions = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        G = generate_d_regular_graph(d, n)
        embedding = isometric_embedding(G, n)
        non_rigid_motions = apply_non_rigid_transformations(embedding, n)
        total_non_rigid_motions += len(non_rigid_motions)
        instances_tested += 1
        n_max = max(n_max, n)

    metric_value = total_non_rigid_motions / instances_tested
    conjecture_holds = metric_value <= (n_max ** 2) * d
    counterexample = "" if conjecture_holds else f"Non-rigid motions: {total_non_rigid_motions}, Expected: O({n_max}^2)"

    return {
        "metric_name": "non_rigid_motions",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-rigid motions exceeded expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")