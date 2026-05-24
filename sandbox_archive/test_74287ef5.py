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
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
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

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjoint[j][i] = (-1) ** (i + j) * cofactor
    return matrix_multiplication(adjoint, [[1 / det_A] * n for _ in range(n)])

def p_adic_analytic_continuation(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if G[u][v]:
                A[u][v] = A[v][u] = random.choice([1, -1])
    x = gaussian_elimination(A, [0] * n)
    return sum(abs(xi) for xi in x)

def tseitin_formula(edges, n):
    literals = {i: f"x{i}" for i in range(n)}
    clauses = []
    for u, v in edges:
        l_u = literals[u]
        l_v = literals[v]
        clauses.append([l_u, -l_v])
        clauses.append([-l_u, l_v])
        clauses.append([l_u, l_v])
    return clauses

def resolution_width(clauses):
    queue = set()
    for clause in clauses:
        if len(clause) == 1:
            queue.add(clause[0])
    while queue:
        literal = random.choice(list(queue))
        queue.remove(literal)
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                return len(queue)
            new_clause = [l for l in clause if l != -literal]
            if not new_clause:
                return len(queue)
            new_clauses.append(new_clause)
        clauses.extend(new_clauses)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if G[u][v]]
    ν_G = p_adic_analytic_continuation(G)
    clauses = tseitin_formula(edges, n)
    width = resolution_width(clauses)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (math.log(ν_G, 2) * math.log(n, 2)),
        "counterexample": "" if width >= 2 ** (math.log(ν_G, 2) * math.log(n, 2)) else f"Width {width} < 2^(Ω({ν_G}) * log({n}, 2))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")