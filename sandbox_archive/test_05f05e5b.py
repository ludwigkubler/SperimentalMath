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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Singular matrix")
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_3regular_graph(v):
    while True:
        edges = set()
        vertices = list(range(v))
        random.shuffle(vertices)
        for i in range(v):
            for j in range(i+1, v):
                if len(edges) == 2 * v - 3:
                    break
                if (vertices[i], vertices[j]) not in edges and (vertices[j], vertices[i]) not in edges:
                    edges.add((vertices[i], vertices[j]))
        if len(edges) == 2 * v - 3:
            return [sorted(e) for e in edges]

def tseitin_formula(v):
    clauses = []
    variables = list(range(1, v+1))
    for i in range(v):
        clauses.append([variables[i]])
        clauses.append([-variables[i]])
        for j in range(i+1, v):
            clauses.append([variables[i], variables[j]])
            clauses.append([variables[i], -variables[j]])
            clauses.append([-variables[i], variables[j]])
            clauses.append([-variables[i], -variables[j]])
    return clauses

def persistent_homology(clauses, scale):
    n = len(clauses)
    points = [[-1 if i % 2 == 0 else 1 for _ in range(n)] for _ in range(2)]
    H1_lifespans = []
    for t in range(1, int(scale * math.sqrt(2)) + 1):
        distance_matrix = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dist = sum((points[0][i] - points[0][j])**2 for k in range(n))
                if dist <= t**2:
                    distance_matrix[i][j] = distance_matrix[j][i] = dist
        # Compute the boundary matrix and perform Gaussian elimination
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if distance_matrix[i][j] <= t**2:
                    B[j][i] = 1
        try:
            gaussian_elimination(B)
        except ValueError:
            continue
        # Count the number of non-zero rows to get H1 dimension
        H1_dimension = sum(1 for row in B if any(row))
        H1_lifespans.append(H1_dimension)
    return sum(H1_lifespans)

def resolution_width(clauses, max_width):
    def dpll(clause_set, assignment, model):
        if not clause_set:
            return True
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(clause_set - {c for c in clause_set if literal in c}, new_assignment, model):
                return True
            new_assignment[literal] = False
            if dpll(clause_set - {c for c in clause_set if -literal in c}, new_assignment, model):
                return True
            return False
        literals = [l for l in range(1, max_width+1) if l not in assignment]
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(clause_set - {c for c in clause_set if literal in c}, new_assignment, model):
            return True
        new_assignment[literal] = False
        if dpll(clause_set - {c for c in clause_set if -literal in c}, new_assignment, model):
            return True
        return False

    max_width_found = 0
    for width in range(1, max_width+1):
        if dpll(set(tuple(c) for c in clauses), {}, {}):
            max_width_found = width
        else:
            break
    return max_width_found

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for v in [6, 8, 10, 12, 14, 16]:
        if v * 3 // 2 > 30:
            break
        n_max = max(n_max, v * 3 // 2)
        clauses = tseitin_formula(v)
        L1 = persistent_homology(clauses, 2 * math.sqrt(3))
        w = resolution_width(clauses, 6)
        metric_values.append(w / (L1 + math.log(v * 3 // 2)))
        instances_tested += 1

    if len(metric_values) < 30:
        return {
            "metric_name": "w(L1+log n)",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    C_star = max(metric_values)

    if C_star > 10:
        conjecture_holds = False
        counterexample = f"C*={C_star} > 10"

    return {
        "metric_name": "w(L1+log n)",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["metric_value"] for r in results) > 10:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"C* exceeds 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")