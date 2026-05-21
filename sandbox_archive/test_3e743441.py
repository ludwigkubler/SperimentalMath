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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i - 1, -1, -1):
            b[j] -= A[j][i] * x[i]

    return x

def dpll(clauses, assignment=[]):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment[:]
        if literal > 0:
            new_assignment.append(literal)
        else:
            new_assignment.append(-literal)
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)

    literals = set(abs(c) for c in sum(clauses, []))
    literal = next(lit for lit in literals if lit not in [abs(c) for c in assignment] and -lit not in [abs(c) for c in assignment])
    new_assignment = assignment[:]
    if literal > 0:
        new_assignment.append(literal)
    else:
        new_assignment.append(-literal)

    return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment) or \
           dpll(clauses, [l for l in new_assignment if l != literal])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([3, 4, 5])
    clauses = []
    for i in range(2**n):
        clause = []
        for j in range(n):
            if random.randint(0, 1) == 0:
                clause.append(j + 1)
            else:
                clause.append(-(j + 1))
        clauses.append(clause)

    refutation = dpll(clauses)
    if not refutation:
        return {
            "metric_name": "beta_1",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "DPLL did not find a refutation"
        }

    vertices = set(clause for clause in clauses)
    edges = []
    triangles = []

    # Build the graph
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses[i+1:], start=i+1):
            common_literals = set(lit for lit in clause1 if -lit in clause2)
            if len(common_literals) > 0:
                edges.append((i, j))
                triangles.extend([(i, j, k) for k in range(len(clauses)) if len(set(clause1).intersection(clause2, clauses[k])) == 2])

    # Compute beta_1
    V = len(vertices)
    E = len(edges)
    F = len(triangles)

    boundary_matrix = [[0] * (E + F) for _ in range(E)]
    cycle_rank = E - V

    for i, (u, v) in enumerate(edges):
        boundary_matrix[i][i] = 1
        boundary_matrix[i][i + E] = 1

    for j, (u, v, w) in enumerate(triangles):
        boundary_matrix[j + E][j] = 1
        boundary_matrix[j + E][j + F] = 1
        boundary_matrix[j + E][j + 2 * F] = 1

    b = [0] * (E + F)
    for i, (u, v) in enumerate(edges):
        if u < v:
            b[i] = 1
        else:
            b[i] = -1

    beta_1 = sum(1 for x in gaussian_elimination(boundary_matrix, b) if x != 0)

    # Check the conjecture
    lower_bound = math.floor(n * math.log2(n + 1))
    ratio = beta_1 / len(refutation)

    return {
        "metric_name": "beta_1",
        "metric_value": beta_1,
        "instances_tested": 1,
        "conjecture_holds": beta_1 >= lower_bound and ratio > 0.01,
        "counterexample": "" if beta_1 >= lower_bound else f"beta_1={beta_1} < {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_beta_1 = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    var_beta_1 = sum((r["metric_value"] - mean_beta_1)**2 for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results if r["metric_value"] is not None) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_beta_1} std={var_beta_1} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='beta_1 < {math.floor(n * math.log2(n + 1))}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")