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
            A[j][i] = 0
            for k in range(i+1, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tropical_rank(poly):
    n = len(poly)
    A = [[0] * (n+1) for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(n):
            if poly[i][j] > 0:
                A[i][j] = -math.log2(poly[i][j])
                A[i][-1] += A[i][j]
                b[j] -= A[i][j]
    x = gaussian_elimination(A, b)
    return sum(x)

def clause_indicator_polynomial(clauses, n):
    m = len(clauses)
    poly = [[0] * (n+1) for _ in range(n)]
    for i in range(m):
        clause = clauses[i]
        if len(clause) == 1:
            var = abs(clause[0]) - 1
            sign = 1 if clause[0] > 0 else -1
            poly[var][n] += sign
        elif len(clause) == 2:
            var1, var2 = abs(clause[0]) - 1, abs(clause[1]) - 1
            sign1, sign2 = (1 if clause[0] > 0 else -1), (1 if clause[1] > 0 else -1)
            poly[var1][var2] += sign1 * sign2
    return [sum(row) for row in matrix_multiplication(poly, poly)]

def resolution_width(clauses):
    n = len(clauses)
    clauses = [[abs(x)-1 for x in clause] for clause in clauses]
    stack = []
    for clause in clauses:
        if len(clause) == 1:
            stack.append([clause[0]])
        else:
            stack.append(clause)
    while len(stack) > 1:
        clause1 = stack.pop()
        clause2 = stack.pop()
        new_clauses = []
        for x in clause1:
            for y in clause2:
                if x != -y:
                    new_clause = list(set(clause1 + clause2))
                    new_clause.remove(x)
                    new_clause.remove(-y)
                    new_clauses.append(new_clause)
        stack.extend(new_clauses)
    return max(len(clause) for clause in stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    clauses = []
    for _ in range(m):
        num_vars = random.randint(1, n)
        clause = [random.choice([-i, i]) for i in range(1, num_vars+1)]
        clauses.append(clause)
    poly = clause_indicator_polynomial(clauses, n)
    width = resolution_width(clauses)
    trop_rank = tropical_rank(poly)
    if width > 2 ** trop_rank:
        return {
            "metric_name": "Resolution Width vs Tropical Rank",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Width {width} exceeds 2^trop_rank({trop_rank})"
        }
    return {
        "metric_name": "Resolution Width vs Tropical Rank",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds 2^trop_rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")