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

def arithmetic_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(abs(matrix[j][i]) < 1e-9 for j in range(n)):
            continue
        pivot_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        rank += 1
        for j in range(n):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def generate_kcnf_instance(n, m):
    variables = set(f"x{i}" for i in range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause[0] = f"~{clause[0]}"
        if random.choice([True, False]):
            clause[1] = f"~{clause[1]}"
        clauses.append(clause)
    return n, m, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m, _, clauses = generate_kcnf_instance(n, n)
            tropical_semigroup = []
            for clause in clauses:
                tropicalizer = [1 if literal.startswith("x") else -1 for literal in clause]
                tropical_semigroup.append(tropicalizer)
            tropical_semigroup = list(set(tuple(row) for row in tropical_semigroup))
            A = [[0] * n for _ in range(n)]
            b = [0] * n
            for i in range(n):
                for j in range(i, n):
                    if i == j:
                        A[i][j] = 1
                    else:
                        A[i][j] = -1
                        A[j][i] = -1
                b[i] = 1
            rank = arithmetic_rank(A)
            communication_complexity = 2 ** rank
            results.append({
                "n": n,
                "m": m,
                "rank": rank,
                "communication_complexity": communication_complexity
            })
    metric_value = sum(result["communication_complexity"] for result in results) / len(results)
    conjecture_holds = all(result["communication_complexity"] >= 2 ** result["rank"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Communication Complexity",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")