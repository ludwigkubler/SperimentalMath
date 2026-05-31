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

def generate_random_graph(n):
    graph = {i: set() for i in range(n)}
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].add(v)
            graph[v].add(u)
            edges.add((u, v))
    return graph

def compute_curvature_form(graph):
    n = len(graph)
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j not in graph[i]:
                continue
            count = sum(1 for k in range(n) if k != i and k != j and (k in graph[i] or k in graph[j]))
            R[i][j] = Fraction(count - 2, n - 3)
    return R

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        rank += 1
        for row in range(n):
            if row == pivot_row:
                continue
            factor = -matrix[row][col] / matrix[pivot_row][col]
            for col2 in range(n):
                matrix[row][col2] += factor * matrix[pivot_row][col2]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mean_ranks = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        graph = generate_random_graph(n)
        curvature_form = compute_curvature_form(graph)
        rank = min_rank(curvature_form)
        mean_ranks.append(rank)
        instances_tested += 1
        if n > n_max:
            n_max = n

    if len(mean_ranks) == 0:
        return {
            "metric_name": "Minimal Rank of Curvature Form",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_rank = sum(mean_ranks) / len(mean_ranks)
    if instances_tested < 30:
        return {
            "metric_name": "Minimal Rank of Curvature Form",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    if n_max < 16:
        return {
            "metric_name": "Minimal Rank of Curvature Form",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }

    std_deviation_ranks = math.sqrt(sum((x - mean_rank) ** 2 for x in mean_ranks) / len(mean_ranks))
    if std_deviation_ranks == 0:
        return {
            "metric_name": "Minimal Rank of Curvature Form",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }

    return {
        "metric_name": "Minimal Rank of Curvature Form",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_deviation_ranks = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation_ranks} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")