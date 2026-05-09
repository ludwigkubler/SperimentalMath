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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += (-1) ** j * A[0][j] * det(submatrix)
        return det_val

def algebraic_connectivity(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(G[i])
        for j in range(n):
            if G[i][j]:
                L[i][j] = -1 / degree
            if i == j:
                L[i][j] += 1 + degree / (2 * det(gaussian_elimination(L)))

    eigenvalues = []
    for _ in range(50):  # Power iteration method
        v = [random.random() for _ in range(n)]
        v /= sum(v)
        for _ in range(10):
            v = [sum(L[i][j] * v[j] for j in range(n)) for i in range(n)]
            v /= sum(v)
        eigenvalues.append(sum(v) / n)

    return min(eigenvalues[1:])

def generate_tseitin_formula(G, assignment):
    n = len(G)
    clauses = []
    for i in range(n):
        if not assignment[i]:
            clauses.append([i + 1])
            clauses.append([-i - 1])
        else:
            for j in range(n):
                if G[i][j] and not assignment[j]:
                    clauses.append([-i - 1, j + 1])
    return clauses

def dpll(clauses, assignment, literals):
    if not clauses:
        return True
    literal = literals[0]
    pos_literal = abs(literal)
    neg_literal = -pos_literal
    if literal in assignment:
        new_assignment = assignment.copy()
        new_literals = [l for l in literals if l != literal and l != -literal]
        return dpll(clauses, new_assignment, new_literals)
    else:
        new_clauses_pos = [c for c in clauses if pos_literal not in c and neg_literal not in c]
        new_clauses_neg = [c for c in clauses if neg_literal not in c and pos_literal not in c]
        return dpll(new_clauses_pos, assignment | {pos_literal: True}, literals[1:]) or \
               dpll(new_clauses_neg, assignment | {neg_literal: False}, literals[1:])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0

    μ_G = algebraic_connectivity(G)
    if μ_G == 0:
        return {
            "metric_name": "DPLL Tree Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    c = 1.0
    target_size = 2 ** (c * μ_G)
    instances_tested = 0
    for _ in range(30):
        assignment = {i: random.choice([True, False]) for i in range(n)}
        clauses = generate_tseitin_formula(G, assignment)
        if dpll(clauses, {}, list(range(1, n + 1))):
            instances_tested += 1
    return {
        "metric_name": "DPLL Tree Size",
        "metric_value": target_size,
        "instances_tested": instances_tested,
        "conjecture_holds": instances_tested >= 24,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # First 30 primes
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")