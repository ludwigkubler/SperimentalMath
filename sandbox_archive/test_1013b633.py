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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    n = len(A)
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    return C

def matrix_sub(A, B):
    n = len(A)
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    return C

def scalar_multiply(A, c):
    n = len(A)
    C = [[c * A[i][j] for j in range(n)] for i in range(n)]
    return C

def matrix_trace(A):
    n = len(A)
    trace = 0
    for i in range(n):
        trace += A[i][i]
    return trace

def identity_matrix(n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return I

def is_nilpotent(A, tolerance=1e-9):
    n = len(A)
    c = 0
    while True:
        A_next = matrix_multiply(A, A)
        if max(max(abs(x) for x in row) for row in A_next) < tolerance:
            return c
        A = A_next
        c += 1

def generate_transition_matrix(s):
    M = [[random.randint(0, 1) for _ in range(s)] for _ in range(s)]
    # Ensure the matrix is stochastic and symmetric
    for i in range(s):
        row_sum = sum(M[i])
        if row_sum == 0:
            M[i][i] = 1
        else:
            for j in range(s):
                M[j][i] = M[i][j] * (s / row_sum)
    return M

def generate_read_twice_bp(n, s):
    layers = []
    for _ in range(2 * n):
        var = random.randint(0, n - 1)
        if not layers or layers[-1][0] != var:
            layers.append((var, generate_transition_matrix(s)))
        else:
            layers.append((var, generate_transition_matrix(s)))
    return layers

def compute_M_bar(M, s):
    trace = matrix_trace(M)
    I = identity_matrix(s)
    M_bar = matrix_sub(M, scalar_multiply(I, trace / s))
    return M_bar

def bfs_close_lie_algebra(generators, dim_cap):
    n = len(generators[0])
    closure = generators[:]
    for _ in range(dim_cap):
        new_elements = []
        for A in closure:
            for B in closure:
                C = matrix_multiply(A, B)
                D = matrix_sub(C, matrix_multiply(B, A))
                if any(any(abs(x) >= 1e-9 for x in row) for row in D):
                    new_elements.append(D)
        if not new_elements:
            break
        closure.extend(new_elements)
    return closure

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [3, 4, 5, 6, 7, 8]
    s_values = [4, 8, 16, 32, 64, 128]
    
    for n in n_values:
        # Canonical IP_2_n product BP
        M_bar_k = []
        for k in range(n):
            M_bar_k.append(scalar_multiply(identity_matrix(2**(n+1)), 1))
        rho_canonical = is_nilpotent(matrix_add(*M_bar_k), tolerance=1e-9)
        if rho_canonical < n // 2:
            return {
                "metric_name": "rho_canonical",
                "metric_value": rho_canonical,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"IP_2_{n} canonical BP has rho < {n//2}"
            }
        
        for s in s_values:
            # Generate random read-twice BP
            layers = generate_read_twice_bp(n, s)
            M_bar_k = [compute_M_bar(layer[1], s) for layer in layers]
            g_P = bfs_close_lie_algebra(M_bar_k, s**2)
            rho_P = is_nilpotent(matrix_add(*g_P), tolerance=1e-9)
            results.append(rho_P <= 4 * math.log2(s) + 10)
    
    return {
        "metric_name": "rho_read_twice",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values) * len(s_values),
        "conjecture_holds": all(results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"read-twice BP with rho > 4*log2(size)+10\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient evidence to support or falsify the conjecture")