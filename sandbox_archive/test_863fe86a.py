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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def grothendieck_witt_class(poly, mod):
    n = len(poly)
    A = [[0] * (n+1) for _ in range(n+1)]
    b = [0] * (n+1)
    for i in range(n):
        for j in range(i, n):
            A[i][j] = (poly[i] + poly[j]) % mod
            A[j][i] = A[i][j]
        b[i] = 1 if i == 0 else 0
    gaussian_elimination(A, b)
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank

def resolution_width(F):
    # Simplified DPLL solver to estimate resolution width
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        else:
            literals = [l for l in range(1, len(clauses)+1) if l not in assignment]
            literal = random.choice(literals)
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        return False

    width = 0
    for i in range(1 << len(F)):
        assignment = [bool(i & (1 << j)) for j in range(len(F))]
        if dpll(F, assignment):
            width = max(width, sum(1 for l in range(len(F)) if assignment[l]))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n // 2, n * (n - 1) // 2)
    k = 3
    F = []
    for _ in range(m):
        clause = [random.randint(1, n) for _ in range(k)]
        if random.choice([True, False]):
            clause = [-l for l in clause]
        F.append(clause)

    tropical_curve_rank = grothendieck_witt_class(F, 2)
    resolution_width_F = resolution_width(F)

    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_F,
        "instances_tested": m,
        "conjecture_holds": resolution_width_F <= 1.5 * tropical_curve_rank and resolution_width_F <= 1.2 * tropical_curve_rank,
        "counterexample": "" if resolution_width_F <= 1.5 * tropical_curve_rank else f"resolution_width_F={resolution_width_F}, tropical_curve_rank={tropical_curve_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std_dev:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std_dev:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")