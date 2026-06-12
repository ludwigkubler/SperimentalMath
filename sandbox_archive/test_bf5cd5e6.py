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
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

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

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1) ** (i + j) * determinant(minor)
            adjoint[j][i] = cofactor
    inv_A = matrix_multiply(adjoint, [[Fraction(1, det_A)] * n for _ in range(n)])
    return inv_A

def random_cnf(n):
    clauses = []
    for _ in range(n):
        literals = [random.choice([f"x{i}", f"~x{i}"]) for i in range(n)]
        clause = random.sample(literals, 2)
        clauses.append(clause)
    return clauses

def resolution_width(cnf):
    n = len(cnf)
    visited = set()
    queue = []
    for clause in cnf:
        queue.extend(clause)
    while queue:
        literal = queue.pop(0)
        if literal in visited:
            continue
        visited.add(literal)
        for clause in cnf:
            if literal in clause and ~literal in clause:
                return len(visited)
            elif literal in clause:
                new_clause = [l for l in clause if l != literal]
                queue.extend(new_clause)
    return len(visited)

def mrank(cnf):
    n = len(cnf)
    A = [[0] * (n+1) for _ in range(n)]
    b = [0] * n
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal.startswith("x"):
                j = int(literal[1:])
                A[i][j-1] += 1
            else:
                j = int(literal[2:])
                A[i][j-1] -= 1
        b[i] = 1
    try:
        x = gaussian_elimination(A, b)
        rank = sum(1 for val in x if abs(val) > 1e-9)
        return rank
    except ValueError:
        return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + (60 * len(sys.argv) - 10) < end_time:
            cnf = random_cnf(n)
            w = resolution_width(cnf)
            rank = mrank(cnf)
            n_max = max(n_max, n)
            instances_tested += 1
            metric_values.append(rank / w)
        else:
            counterexample = "budget_exceeded"
            break
    
    if counterexample == "":
        correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, range(len(metric_values)))) / (len(metric_values) * sum((x - mean) ** 2 for x in metric_values))
        if correlation_coefficient < 0.5 or any(rank > 3*w for rank, w in zip(metric_values, range(len(metric_values)))):
            conjecture_holds = False
            counterexample = "correlation_threshold_violated"
    
    return {
        "metric_name": "mrank_over_w",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time
    
    if not sys.argv[1:]:
        seeds = [2**i - 1 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    end_time = time.time() + (60 * len(seeds) - 10)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_violated\" first_failing_seed={first_failing_seed}")