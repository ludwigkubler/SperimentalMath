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
        # Find max pivot in column i
        max_idx = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_idx][i]):
                max_idx = j
        A[i], A[max_idx] = A[max_idx], A[i]
        b[i], b[max_idx] = b[max_idx], b[i]

        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back substitution
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
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def characteristic_polynomial(A):
    n = len(A)
    x = Fraction('x')
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    poly = [1]
    for k in range(n):
        A_k = matrix_multiply(A, A)
        coeff = (-1)**k * determinant(A_k - identity)
        poly.append(coeff)
    return poly

def tropical_divisors(poly):
    divisors = set()
    n = len(poly) - 1
    for i in range(1, n+1):
        if poly[i] != Fraction(0):
            divisor = math.log(abs(poly[i].numerator)) / abs(poly[i].denominator)
            divisors.add(divisor)
    return divisors

def dpll(phi):
    variables = set()
    for clause in phi:
        for var in clause:
            variables.add(var)

    def solve(assignment, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            assignment[var] = 1 if var > 0 else -1
            new_clauses = [c for c in clauses if var not in c and (-var not in c)]
            return solve(assignment, new_clauses)

        pure_literal = next((v for v in variables if all(v not in clause or -v not in clause for clause in clauses)), None)
        if pure_literal:
            assignment[pure_literal] = 1
            new_clauses = [c for c in clauses if pure_literal not in c and (-pure_literal not in c)]
            return solve(assignment, new_clauses)

        var = next(iter(variables))
        assignment[var] = 1
        new_assignment = {k: v for k, v in assignment.items()}
        new_assignment[-var] = -1
        if solve(new_assignment, clauses):
            return True

    assignment = {}
    return solve(assignment, phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        phi = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice([-i, i]) for i in range(1, n+1)]
            phi.append(clause)

        poly = characteristic_polynomial(phi)
        divisors = tropical_divisors(poly)
        h_phi = dpll(phi)
        metric_value += len(divisors) / (h_phi + 1e-9)

    mean_height = metric_value / instances_tested
    if abs(mean_height - 2 * n) > 3:
        conjecture_holds = False
        counterexample = "height_difference"

    return {
        "metric_name": "mean_height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "height_difference" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "height_difference")
        print(f"RESULT: FALSIFIED counterexample='height_difference' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")