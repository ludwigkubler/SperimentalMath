# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        denom = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= denom
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def min_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(cols)))
    return rank

def communication_complexity_rank(graph):
    n = len(graph)
    edges = [edge for node in graph for edge in graph[node]]
    unique_edges = set(frozenset(edge) for edge in edges)
    return len(unique_edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3
    n_max = 40
    instances_tested = 0
    total_diff = 0.0
    squared_diff_sum = 0.0

    for n in range(5, n_max + 1, 5):
        graph = {i: [] for i in range(n)}
        for _ in range(d * n // 2):
            u, v = random.sample(range(n), 2)
            if (u, v) not in graph[u] and (v, u) not in graph[v]:
                graph[u].append((v, 1))
                graph[v].append((u, 1))

        cluster_algebra = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            cluster_algebra[i][i] = 1
            for j in range(i + 1, n):
                if (j, i) in graph[i]:
                    cluster_algebra[i][j] = 1
                    cluster_algebra[j][i] = 1

        min_rank_cG = min_rank(cluster_algebra)
        r_G = communication_complexity_rank(graph)

        instances_tested += 1
        diff = abs(min_rank_cG - r_G)
        total_diff += diff
        squared_diff_sum += diff ** 2

    mean_diff = total_diff / instances_tested
    std_dev = math.sqrt(squared_diff_sum / instances_tested)

    conjecture_holds = all(abs(diff - mean_diff) <= 1.5 * std_dev for diff in [total_diff / instances_tested] * instances_tested)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "min_rank_cG_r_G_diff",
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")