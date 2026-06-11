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
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d < 1 or d > n - 1:
            return None
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while any((i, j) in edges or (j, i) in edges for j in neighbors):
                neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j:
                    edges.add((i, j))
        return list(edges)

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(2 * n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[2 * i], literals[2 * i + 1]])
        for u, v in graph:
            clauses.append([-literals[2 * u], -literals[2 * v + 1]])
            clauses.append([-literals[2 * u + 1], literals[2 * v]])
            clauses.append([literals[2 * u], literals[2 * v]])
        return literals, clauses

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i == j:
                    continue
                factor = -matrix[j][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix

    def minimal_index(graph):
        n = len(graph)
        literals, clauses = tseitin_formula(graph)
        m = len(clauses)
        matrix = [[0] * (m + 1) for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                if any(l in clauses[i] and -l in clauses[j] for l in literals):
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        matrix = gaussian_elimination(matrix)
        if matrix is None:
            return None
        rank = sum(1 for row in matrix if any(row))
        return rank

    def resolution_width(clauses):
        n = len(clauses)
        width = [len(c) for c in clauses]
        return max(width)

    n_max = 40
    instances_tested = 30
    m_indices = []
    widths = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        d = (n * (n - 1)) // 2 // n
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        m_index = minimal_index(graph)
        if m_index is None or m_index > 10:
            continue
        phi, clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        m_indices.append(m_index)
        widths.append(width)

    if not m_indices or not widths:
        return {
            "metric_name": "m_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_m = sum(m_indices) / len(m_indices)
    mean_w = sum(widths) / len(widths)
    std_dev = math.sqrt(sum((x - mean_m) ** 2 for x in m_indices) / len(m_indices))
    support_fraction = sum(1 for m, w in zip(m_indices, widths) if abs(m - w) <= 3) / len(m_indices)

    return {
        "metric_name": "m_index",
        "metric_value": mean_m,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_m = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_m) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_m} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")