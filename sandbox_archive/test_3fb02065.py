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
    graph = {i: set() for i in range(n)}
    edges_added = 0
    while edges_added < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            edges_added += 1
    return graph

def tseitin_formula(graph):
    n = len(graph)
    variables = {f'x{i}': i for i in range(n)}
    clauses = []
    for u in range(n):
        if not graph[u]:
            continue
        literals = [variables[f'x{v}'] for v in graph[u]]
        clause = [-variables[f'x{u}']] + literals
        clauses.append(clause)
        for i in range(len(literals)):
            for j in range(i + 1, len(literals)):
                clauses.append([-literals[i], -literals[j]])
    return variables, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        pivot_row = None
        for row in range(col, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        for row in range(rows):
            if row == col:
                continue
            factor = -matrix[row][col] / matrix[col][col]
            for j in range(cols):
                matrix[row][j] += factor * matrix[col][j]
    rank = 0
    for row in range(rows):
        if any(matrix[row]):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_sum = 0
    m_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        d = random.randint(2, n - 1)
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        variables, clauses = tseitin_formula(graph)
        matrix = [[0] * (n + len(clauses)) for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 1
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    row = variables[f'x{literal - 1}']
                else:
                    row = variables[f'x{-literal - 1}'] + n
                col = abs(literal) - 1
                matrix[row][col] += 1

        min_rank = gaussian_elimination(matrix)
        m = len(clauses)

        min_rank_sum += min_rank
        m_sum += m
        instances_tested += 1
        n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "min_rank_over_m",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    min_rank_over_m = min_rank_sum / m_sum
    if min_rank_over_m < 0.1 or min_rank_over_m > 10:
        return {
            "metric_name": "min_rank_over_m",
            "metric_value": min_rank_over_m,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"min_rank_over_m out of bounds: {min_rank_over_m}"
        }

    return {
        "metric_name": "min_rank_over_m",
        "metric_value": min_rank_over_m,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_over_m out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_instances")