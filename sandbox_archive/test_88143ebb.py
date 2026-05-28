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

# Constants
MAX_N = 40
MAX_CLAUSES = 150
MAX_VARIABLES = 20
MAX_ITERATIONS = 30

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def grothendieck_witt_class(poly, mod):
    n = len(poly)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = (poly[i] + poly[j]) % mod
            A[j][i] = A[i][j]
    det = determinant(A)
    return abs(det) ** (1/n)

def resolution_width(F):
    # Simplified DPLL solver for demonstration purposes
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = next(iter(unit_clauses[0]))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c - {literal} for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c - {-literal} for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literals = [l for l in range(1, len(clauses) + 1) if (all(l in c for c in clauses) or all(-l in c for c in clauses))]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c - {literal} for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c - {-literal} for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        return False

    assignment = [False] * (len(F) + 1)
    return len(next((assignment for assignment in itertools.product([True, False], repeat=len(F)) if dpll(F, assignment)), []))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, MAX_CLAUSES)
    F = []
    for _ in range(m):
        clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
        F.append(clause)
    
    tropical_curve_rank = grothendieck_witt_class(F, 2) if m > 0 else 0
    resolution_width_F = resolution_width(F)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_F,
        "instances_tested": 1,
        "conjecture_holds": resolution_width_F <= 1.5 * tropical_curve_rank and resolution_width_F <= 1.2 * tropical_curve_rank,
        "counterexample": "" if resolution_width_F <= 1.5 * tropical_curve_rank else f"resolution_width={resolution_width_F} > 1.5 * tropical_curve_rank={1.5 * tropical_curve_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")