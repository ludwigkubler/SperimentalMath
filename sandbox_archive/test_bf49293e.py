# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_power(A, power):
    result = [[0.0 if i != j else 1.0 for j in range(len(A))] for i in range(len(A))]
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if any(A[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def matrix_inverse(A):
    n = len(A)
    I = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        I[i][i] = 1.0
    AI = [row[:] for row in A]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(AI[r][col]))
        AI[col], AI[pivot] = AI[pivot], AI[col]
        I[col], I[pivot] = I[pivot], I[col]
        if AI[col][col] == 0:
            raise ValueError("Matrix is singular")
        for row in range(col + 1, n):
            factor = AI[row][col] / AI[col][col]
            for c in range(col, n):
                AI[row][c] -= factor * AI[col][c]
            for c in range(n):
                I[row][c] -= factor * I[col][c]
    for col in reversed(range(n)):
        for row in reversed(range(col)):
            factor = AI[row][col] / AI[col][col]
            for c in range(col, n):
                AI[row][c] -= factor * AI[col][c]
            for c in range(n):
                I[row][c] -= factor * I[col][c]
    for row in range(n):
        factor = 1.0 / AI[row][row]
        for col in range(n):
            AI[row][col] *= factor
            I[row][col] *= factor
    return I

def matrix_eigenvalues(A):
    n = len(A)
    eigenvalues = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            Ax = matrix_multiply(A, [x])[0]
            x = [a / matrix_norm(Ax) for a in Ax]
        eigenvalue = matrix_multiply([x], matrix_multiply(A, [x]))[0][0]
        eigenvalues.append(eigenvalue)
    return sorted(eigenvalues)

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even")
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([s for s in stubs if s != u])
        stubs.remove(v)
        edges.append((u, v))
    return edges

def compute_laplacian(edges, n):
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1.0
        A[v][u] = 1.0
        D[u][u] += 1.0
        D[v][v] += 1.0
    L = matrix_subtract(D, A)
    return L

def compute_hcf(L, n):
    eigenvalues = matrix_eigenvalues(L)
    lambda_1 = eigenvalues[-1]
    lambda_k = eigenvalues[1:]
    sum_lambda_k_4 = sum(l**4 for l in lambda_k)
    sum_lambda_k_2 = sum(l**2 for l in lambda_k)
    hcf = (n - 1) * sum_lambda_k_4 / sum_lambda_k_2**2
    return hcf

def compute_sb(L, n):
    eigenvalues = matrix_eigenvalues(L)
    lambda_1 = eigenvalues[-1]
    sb = (n / 4) * lambda_1
    return sb

def compute_mc(edges, n):
    max_cut = 0
    for partition in itertools.product([-1, 1], repeat=n):
        cut = sum(1 for u, v in edges if partition[u] != partition[v])
        if cut > max_cut:
            max_cut = cut
    return max_cut

def run_trial(seed):
    random.seed(seed)
    n = random.choice([12, 14, 16, 18, 20])
    edges = generate_3_regular_graph(n)
    L = compute_laplacian(edges, n)
    hcf = compute_hcf(L, n)
    sb = compute_sb(L, n)
    mc = compute_mc(edges, n)
    rho = mc / sb
    u = 1 - (1 / 10) * math.sqrt((hcf - 1) / (n - 1))
    conjecture_holds = rho <= u
    counterexample = "" if conjecture_holds else f"rho={rho} > u={u}"
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")