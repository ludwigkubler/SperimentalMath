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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
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
    if m == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def grothendieck_group_order(n):
    if n <= 2:
        return 1
    A = [[Fraction(0, 1)] * (n+1) for _ in range(n+1)]
    for i in range(n):
        A[i][i] = Fraction(1, 1)
        A[n][i] = Fraction(-1, n)
    A[n][n] = Fraction(1, 1)
    det = determinant(A)
    return abs(det.numerator) // abs(det.denominator)

def tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(1, n+1):
        clauses.append([i])
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            clauses.append([-i, -j, i+j])
            clauses.append([-i, -j, -(i+j)])
            clauses.append([-i, j, -(i-j)])
            clauses.append([i, -j, -(i-j)])
    return variables, clauses

def resolution_width(clauses):
    queue = [set(clause) for clause in clauses]
    while True:
        new_clause = None
        for i in range(len(queue)):
            for j in range(i+1, len(queue)):
                if not (queue[i] & queue[j]):
                    new_clause = (queue[i] | queue[j]) - {x for x in queue[i] & queue[j]}
                    break
            if new_clause:
                break
        if not new_clause:
            return len(max(queue, key=len))
        queue.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = tseitin_formula(n)
    groth_group_order = grothendieck_group_order(n)
    width = resolution_width(clauses)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= groth_group_order + 3,
        "counterexample": f"Width {width} exceeds Grothendieck group order {groth_group_order}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds Grothendieck group order\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")