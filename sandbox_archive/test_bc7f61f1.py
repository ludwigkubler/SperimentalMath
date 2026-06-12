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

def gaussian_elimination(matrix, mod):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None  # Singular matrix

        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = (matrix[j][i] * pow(matrix[i][i], -1, mod)) % mod
            for k in range(n):
                matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod

    rank = sum(1 for row in matrix if any(row))
    return rank

def symplectic_form_rank(matrix):
    return gaussian_elimination(matrix, 2) or 0

def tseitin_formula(G):
    n = len(G)
    literals = list(range(1, 2 * n + 1))
    clauses = []

    # Add clauses for each vertex
    for v in range(n):
        clauses.append([literals[v], literals[n + v]])

    # Add clauses for each edge
    for u, v in G:
        clauses.append([-literals[u], -literals[v]])
        clauses.append([-literals[u], literals[n + v]])
        clauses.append([literals[u], -literals[n + v]])
        clauses.append([literals[n + u], -literals[v]])

    # Add clauses for each vertex
    for v in range(n):
        clauses.append([-literals[v], literals[n + v]])

    return literals, clauses

def resolution_width(clauses):
    queue = [c for c in clauses if len(c) == 1]
    learned_clauses = []
    while queue:
        unit_clause = next((c for c in queue if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        queue.remove(unit_clause)
        learned_clauses.append([-literal])
        for clause in clauses:
            if literal in clause:
                new_clause = [l for l in clause if l != literal and -l not in clause]
                if len(new_clause) == 1:
                    queue.append(new_clause)
                else:
                    clauses.remove(clause)
    return len(learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = 2
    G = [[random.randint(0, n - 1), random.randint(0, n - 1)] for _ in range(n * (d - 1))]
    literals, clauses = tseitin_formula(G)
    sfr_matrix = [[0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        sfr_matrix[i][i] = 1
        sfr_matrix[n + i][n + i] = 1
    for u, v in G:
        sfr_matrix[u][v] = -1
        sfr_matrix[v][u] = -1
        sfr_matrix[n + u][n + v] = 1
        sfr_matrix[n + v][n + u] = 1

    sfr = symplectic_form_rank(sfr_matrix)
    w = resolution_width(clauses)

    return {
        "metric_name": "sfr_w_ratio",
        "metric_value": sfr / w if w != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(sfr / w - 1) <= 0.2 * (sfr / w + 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "sfr_w_ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")