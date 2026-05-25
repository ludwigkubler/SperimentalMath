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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank_of_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for i in range(rows):
        if any(row_echelon_form[i]):
            rank += 1
    return rank

def generate_k_clique(n, k):
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    for _ in range(n - k):
        u = random.choice(vertices)
        v = random.choice(vertices)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return {u: [v for v in vertices if (u, v) in edges] for u in vertices}

def quandle_representation(graph):
    n = len(graph)
    q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            if j in graph[i]:
                q[i][j] = 1
    return q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            graph = generate_k_clique(n, k=3)
            q = quandle_representation(graph)
            rank = rank_of_matrix(q)
            if rank < 3:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}"
                break
            total_metric_value += rank
            instances_tested += 1

    return {
        "metric_name": "Minimal Rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")