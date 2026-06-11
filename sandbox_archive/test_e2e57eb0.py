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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[] for _ in range(n)]
    edges_added = set()
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_added:
                graph[i].append(j)
                graph[j].append(i)
                edges_added.add((i, j))
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = list(range(1, 2 * n + 1))
    clauses = []
    for i in range(n):
        clause = [literals[2 * i], literals[2 * i + 1]]
        clauses.append(clause)
        for j in graph[i]:
            if j < i:
                continue
            clause = [-literals[2 * i], -literals[2 * j + 1]]
            clauses.append(clause)
            clause = [-literals[2 * i + 1], literals[2 * j]]
            clauses.append(clause)
    return clauses

def gaussian_elimination(matrix):
    n, m = len(matrix), len(matrix[0])
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        for j in range(m):
            matrix[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def minimal_index(graph):
    n = len(graph)
    clauses = tseitin_formula(graph)
    m = len(clauses)
    matrix = [[0] * (m + 1) for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            if j < i:
                continue
            matrix[i][clauses.index([-literals[2 * i], -literals[2 * j + 1]])] = 1
            matrix[i][clauses.index([-literals[2 * i + 1], literals[2 * j]])] = 1
    matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in matrix if any(row))
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        m_index = minimal_index(graph)
        w_phi = len(tseitin_formula(graph))
        results.append((m_index, w_phi))
    if not results:
        return {
            "metric_name": "m_index(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 33,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    m_index_values = [r[0] for r in results]
    w_phi_values = [r[1] for r in results]
    mean_m_index = sum(m_index_values) / len(m_index_values)
    std_m_index = math.sqrt(sum((x - mean_m_index) ** 2 for x in m_index_values) / len(m_index_values))
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    std_w_phi = math.sqrt(sum((x - mean_w_phi) ** 2 for x in w_phi_values) / len(w_phi_values))
    support_fraction = sum(1 for m, w in zip(m_index_values, w_phi_values) if abs(m - w) <= 3) / len(m_index_values)
    conjecture_holds = support_fraction >= 0.8 and max(m_index_values) <= 10
    counterexample = "" if conjecture_holds else "m_index(G) > 10 for some seed"
    return {
        "metric_name": "m_index(G)",
        "metric_value": mean_m_index,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample=\"m_index(G) > 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")