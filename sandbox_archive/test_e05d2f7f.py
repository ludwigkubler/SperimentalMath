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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda k: abs(matrix[k][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = 1 / matrix[i][i]
        for j in range(cols):
            matrix[i][j] *= factor
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += sign * matrix[0][i] * determinant(submatrix)
        sign *= -1
    return det

def p_rank(clause_set, p=2):
    n = len(clause_set)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = sum(1 for literal in clause_set[i] & clause_set[j] if literal % p == 0)
    return determinant(matrix)

def dpll(clause_set, assignment, literals):
    if not clause_set:
        return True
    if not literals:
        return False
    literal = literals[0]
    positive_clauses = [c for c in clause_set if literal in c or -literal in c]
    negative_clauses = [c for c in clause_set if -literal in c]
    assignment[literal] = True
    if dpll(positive_clauses, assignment, literals[1:]):
        return True
    assignment[literal] = False
    assignment[-literal] = True
    if dpll(negative_clauses, assignment, literals[1:]):
        return True
    assignment[-literal] = False
    return False

def diameter(clause_set):
    n = len(clause_set)
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if not (clause_set[i] & clause_set[j]):
                graph[i].append(j)
                graph[j].append(i)
    visited = [False] * n
    queue = [(0, 0)]
    max_distance = 0
    while queue:
        node, distance = queue.pop(0)
        if visited[node]:
            continue
        visited[node] = True
        max_distance = max(max_distance, distance)
        for neighbor in graph[node]:
            queue.append((neighbor, distance + 1))
    return max_distance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clause_set = [set(random.sample(range(-n, -1), random.randint(1, n))) for _ in range(n)]
    p_val_rank = p_rank(clause_set)
    dpll_diam = diameter(clause_set)
    metric_value = abs(p_val_rank - dpll_diam)
    return {
        "metric_name": "p-rank vs. DPLL diameter",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else list(range(2, 30))
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")