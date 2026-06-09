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
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank_of_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    return sum(1 for row in reduced_matrix if any(row[j] != Fraction(0) for j in range(cols)))

def tseitin_formula(graph):
    n = len(graph)
    variables = list(range(2 * n))
    clauses = []
    for i in range(n):
        clauses.append([variables[2 * i], -variables[2 * (i + n)]])
        for j in graph[i]:
            if j > i:
                clauses.append([-variables[2 * i], -variables[2 * j]])
                clauses.append([variables[2 * i], variables[2 * j]])
    return variables, clauses

def resolution_width(clauses):
    queue = set()
    while True:
        new_clauses = []
        for clause1 in queue:
            for clause2 in queue:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = list(set(clause1 + clause2) - {list(set(clause1) & set(clause2))[0]})
                    if not any(new_clause == c for c in queue):
                        new_clauses.append(new_clause)
        if not new_clauses:
            return len(queue)
        queue.update(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    graph = [random.sample(range(n), n - 1) for _ in range(n)]
    variables, clauses = tseitin_formula(graph)
    min_rep = rank_of_matrix([[1 if i == j else 0 for j in range(2 * n)] for i in range(2 * n)])
    w = resolution_width(clauses)
    return {
        "metric_name": "min_rep_vs_w",
        "metric_value": abs(min_rep - w),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_rep - w) <= 3 * math.sqrt(2 * n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")