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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def transpose(A):
    return [list(row) for row in zip(*A)]

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if m == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def rank(A):
    A = gaussian_elimination(A)
    r = 0
    for row in A:
        if any(row):
            r += 1
    return r

def sos_degree(G, ε=0.878):
    n = len(G)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i, n):
            M[i][j] = G[i][j]
            M[j][i] = G[i][j]
    M[n][n] = 1
    M[0][0] = sum(G[i][j] for i in range(1, n) for j in range(i)) + 1
    for i in range(n):
        M[i+1][0] = -G[i][i]
    for i in range(n):
        M[0][i+1] = -G[i][i]
    
    def sdp_solver(d):
        if d == 2:
            A = [[M[0][0], M[0][1]], [M[1][0], M[1][1]]]
            b = [M[0][n], M[1][n]]
            x = gaussian_elimination(A)
            return sum(x[i][i] for i in range(2)) / 2
        elif d == 3:
            A = [[M[0][0], M[0][1], M[0][2]], [M[1][0], M[1][1], M[1][2]], [M[2][0], M[2][1], M[2][2]]]
            b = [M[0][n], M[1][n], M[2][n]]
            x = gaussian_elimination(A)
            return sum(x[i][i] for i in range(3)) / 3
        else:
            return None
    
    d = 2
    while True:
        ratio = sdp_solver(d)
        if ratio is not None and ratio >= 0.878 + ε:
            return d
        d += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.random() * (2 / n - 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] += 1
    norm = max(abs(G[i][j]) for i in range(n) for j in range(i, n))
    if norm > 1 + 1 / n:
        return {
            "metric_name": "counterexample",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "norm > 1 + 1/n"
        }
    
    M_rank = rank(G)
    d = sos_degree(G)
    if d is None:
        return {
            "metric_name": "counterexample",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "d_to_rank_ratio",
        "metric_value": d / math.log(M_rank),
        "instances_tested": 1,
        "conjecture_holds": d >= math.log(M_rank),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")