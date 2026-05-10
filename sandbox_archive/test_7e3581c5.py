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
    m, n = len(A), len(b)
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i - 1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def coxeter_polynomial(C):
    m, n = len(C), len(C[0])
    identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(m)]
    C_inv = gaussian_elimination(identity, [C[i][j] for j in range(n) for i in range(m)])
    det = determinant(C_inv)
    return det

def clause_to_reflection(clause):
    n = len(clause)
    reflection = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for var in clause:
        if var > 0:
            reflection[var-1][var-1] = Fraction(-2)
            reflection[0][var-1] = Fraction(1)
            reflection[var-1][0] = Fraction(1)
        else:
            reflection[-var-1][-var-1] = Fraction(-2)
            reflection[0][-var-1] = Fraction(1)
            reflection[-var-1][0] = Fraction(1)
    return reflection

def dpll_with_clause_learning(clauses):
    n = max(abs(var) for clause in clauses for var in clause)
    assignment = [None] * (n + 1)
    learned_clauses = []

    def is_satisfiable():
        stack = []
        while stack or any(c for c in clauses if all(assignment[abs(v)] == v > 0 for v in c)):
            while not stack and any(c for c in clauses if all(assignment[abs(v)] == v > 0 for v in c)):
                clause = next(c for c in clauses if all(assignment[abs(v)] == v > 0 for v in c))
                learned_clauses.append(clause)
                var = next(v for v in clause if assignment[v] is None)
                stack.append((var, True))
            if not stack:
                return False
            var, polarity = stack.pop()
            assignment[var] = -var if polarity else var
            for c in learned_clauses:
                if all(assignment[abs(v)] == v > 0 for v in c):
                    learned_clauses.remove(c)
        return True

    if is_satisfiable():
        return len(learned_clauses)
    else:
        return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n), random.randint(1, n)]
        random.shuffle(clause)
        clauses.append(clause)

    C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for clause in clauses:
        C += clause_to_reflection(clause)

    resolution_length = dpll_with_clause_learning(clauses)
    if resolution_length is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }

    coxeter_poly = coxeter_polynomial(C)
    roots = [root for root in range(-10, 11) if abs(coxeter_poly.subs(x=root)) < 1e-6]
    num_roots = len(roots)

    conjecture_holds = num_roots >= math.log2(resolution_length) + 1
    counterexample = "" if conjecture_holds else f"resolution_length={resolution_length}, roots={num_roots}"

    return {
        "metric_name": "number_of_roots",
        "metric_value": num_roots,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])["instances_tested"]]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")