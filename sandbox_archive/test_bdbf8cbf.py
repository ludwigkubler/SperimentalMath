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

def generate_random_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = set()
    nodes = list(range(n))
    while len(edges) < n * 3 // 2:
        u, v = random.sample(nodes, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            for w in nodes:
                if (w, u) in edges or (u, w) in edges:
                    continue
                if (w, v) in edges or (v, w) in edges:
                    continue
                edges.add((u, w))
                edges.add((v, w))
    return edges

def max_cut_value(graph):
    n = len(graph)
    best_cut = 0
    for partition in combinations(range(n), n // 2):
        cut_size = sum(1 for u, v in graph if (u in partition and v not in partition) or (v in partition and u not in partition))
        best_cut = max(best_cut, cut_size)
    return best_cut

def degree_d_moment_matrix(graph, d):
    n = len(graph)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        M[i][i] = 2
    for u, v in graph:
        M[u][v] += 1
        M[v][u] += 1
    return M

def rank(matrix):
    n = len(matrix)
    augmented_matrix = [row + [0] * (n - len(row)) + [i] for i, row in enumerate(matrix)]
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                    break
            else:
                return i
        pivot = augmented_matrix[i][i]
        for j in range(n + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i and augmented_matrix[j][i] != 0:
                factor = augmented_matrix[j][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return n - sum(1 for row in augmented_matrix if all(val == 0 for val in row[:n]))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 2
    epsilon = 0.001
    alpha_G = max_cut_value(generate_random_3_regular_graph(n))
    M_d = degree_d_moment_matrix(generate_random_3_regular_graph(n), d)
    rank_M_d = rank(M_d)
    metric_name = "Rank of Moment Matrix"
    metric_value = rank_M_d
    instances_tested = 1
    conjecture_holds = rank_M_d >= math.sqrt(n) * (1 - epsilon)
    counterexample = "" if conjecture_holds else f"Rank {rank_M_d} < Ω(√{n})"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank < Ω(√n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")