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
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def characteristic_polynomial(matrix):
    n = len(matrix)
    x = Fraction('x')
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    A = [row[:] for row in matrix]
    poly = [1]
    for k in range(n):
        A = matrix_multiply(A, matrix)
        coeff = determinant([[A[i][j] - identity[i][j] * (k+1) for j in range(n)] for i in range(n)])
        poly.append(coeff / Fraction(k + 1))
    return poly

def resolution_width(clauses):
    n = len(clauses)
    clauses_set = set(tuple(sorted(clause)) for clause in clauses)
    assignment = {}
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            polarity = literal > 0
            if literal in assignment and assignment[literal] != polarity:
                return False
            assignment[literal] = polarity
            new_clauses = []
            for c in clauses:
                if literal not in c:
                    new_clauses.append([l for l in c if l != -literal])
            return dpll(new_clauses, assignment)
        pure_literals = [l for l in range(1, n+1) if (l not in assignment and -l not in assignment)]
        if not pure_literals:
            return False
        literal = pure_literals[0]
        polarity = literal > 0
        assignment[literal] = polarity
        new_clauses = []
        for c in clauses:
            if literal not in c:
                new_clauses.append([l for l in c if l != -literal])
        return dpll(new_clauses, assignment)
    def find_pure_literal(clauses):
        pure_literals = [l for l in range(1, n+1) if (l not in assignment and -l not in assignment)]
        if not pure_literals:
            return None, None
        literal = pure_literals[0]
        polarity = literal > 0
        assignment[literal] = polarity
        new_clauses = []
        for c in clauses:
            if literal not in c:
                new_clauses.append([l for l in c if l != -literal])
        return literal, polarity
    return n - len(clauses_set) + dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    clauses = []
    for _ in range(10):
        clause = [random.randint(-n, n) for _ in range(n)]
        while not any(l != -m for l, m in zip(clause, reversed(clause))):
            clause = [random.randint(-n, n) for _ in range(n)]
        clauses.append(tuple(sorted(clause)))
    poly = characteristic_polynomial([[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)])
    phi_f = abs(poly[0]) % 2
    w_f = resolution_width(clauses)
    c = 1 / math.log(w_f + 1e-6, 2)
    metric_value = phi_f <= c * math.log(w_f, 2)
    return {
        "metric_name": "phi_f <= c log w(f)",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": metric_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")