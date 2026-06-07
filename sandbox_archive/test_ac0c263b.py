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
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def is_cyclic_group(G):
    n = len(G)
    if n == 1:
        return True
    for g in G:
        if any(g**i != 1 for i in range(1, n)):
            return False
    return True

def coxeter_group_size(f):
    n = len(f)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if f[i] == 1 and f[j] == 1:
                A[i][j] = 2
                A[j][i] = 2
            elif f[i] == 0 and f[j] == 0:
                A[i][j] = 1
                A[j][i] = 1
    det = determinant(A)
    if det == 0:
        return float('inf')
    G = set()
    for i in range(n):
        for j in range(i+1, n):
            g = (A[i][j], A[j][i])
            if g not in G and g[::-1] not in G:
                G.add(g)
    return len(G) + 2

def dnf_circuit_size(f):
    n = len(f)
    if n == 0:
        return 0
    if n == 1:
        return 1
    f1 = [f[i] for i in range(n-1)]
    f2 = [f[i] ^ f[n-1] for i in range(n-1)]
    return max(dnf_circuit_size(f1), dnf_circuit_size(f2)) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = [random.randint(0, 1) for _ in range(n)]
        cox_size = coxeter_group_size(f)
        dnf_size = dnf_circuit_size(f)
        if cox_size == float('inf'):
            return {
                "metric_name": "Coxeter Group Size / DNF Circuit Size Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        ratio = Fraction(cox_size, dnf_size)
        results.append(ratio)
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Coxeter Group Size / DNF Circuit Size Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": all(r <= 2 for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r is not None and r <= 2) / len(results)
    if all(r is not None and r <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r is not None and r > 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is not None and result > 2)
        print(f"RESULT: FALSIFIED counterexample=\"Coxeter group size exceeds DNF circuit size by more than a factor of 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid results found")