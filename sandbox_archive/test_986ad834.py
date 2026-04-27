# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mod(A, mod):
    m, n = len(A), len(A[0])
    for i in range(m):
        for j in range(n):
            A[i][j] %= mod
    return A

def matrix_multiply(A, B, mod):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
            C[i][j] %= mod
    return C

def matrix_determinant(A, mod):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        sign = (-1) ** (j % 2)
        subdet = matrix_determinant(submatrix, mod)
        det += sign * A[0][j] * subdet
    return det % mod

def gaussian_elimination(A, b, mod):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = (A[j][i] * pow(A[i][i], mod - 2, mod)) % mod
            A[j][i:] = [(A[j][k] - factor * A[i][k]) % mod for k in range(i, n)]
            b[j] = (b[j] - factor * b[i]) % mod
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) * pow(A[i][i], mod - 2, mod) % mod
    return x

def build_lifted_matrix(f, b):
    n = len(f)
    m = 2 ** (b * n)
    M = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            x = [i >> (k * b) & ((1 << b) - 1) for k in range(n)]
            y = [j >> (k * b) & ((1 << b) - 1) for k in range(n)]
            M[i][j] = f(tuple(x + y))
    return M

def build_bipartite_graph(M):
    n = len(M)
    m = n
    L = [[0] * (n + m) for _ in range(n + m)]
    for i in range(n):
        for j in range(m):
            if M[i][j]:
                L[i][j + n] = 1
                L[j + n][i] = 1
    return L

def compute_spanning_tree_count(L, mod=604853):
    n = len(L)
    det = matrix_determinant(L, mod)
    if det == 0:
        return 0
    prime1 = 293
    prime2 = 2017
    det1 = matrix_determinant(matrix_mod(L, prime1), prime1)
    det2 = matrix_determinant(matrix_mod(L, prime2), prime2)
    det = (det1 * pow(prime1, mod - 2, mod) + det2 * pow(prime2, mod - 2, mod)) % mod
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    b_values = [2, 3]
    results = []
    
    for n in n_values:
        f_values = [random.randint(0, 1) for _ in range(2 ** (2 * n))] if n == 3 else [f for f in range(2 ** (2 * n))]
        
        for b in b_values:
            for f in f_values:
                D_f = 0
                x = 0
                while True:
                    query = tuple(random.randint(0, 1) for _ in range(n))
                    if f(query):
                        D_f += 1
                        x ^= reduce(lambda a, b: a ^ b, query)
                    if len(x.bit_set()) == n:
                        break
                
                M = build_lifted_matrix(f, b)
                L = build_bipartite_graph(M)
                tau = compute_spanning_tree_count(L)
                
                metric_value = math.log2(tau) if tau else float('-inf')
                conjecture_holds = (metric_value >= D_f * 2 ** (b * n - 2)) and (f == [1] * n or abs(metric_value - D_f * 2 ** (b * n - 2)) <= b)
                counterexample = "parity" if f != [1] * n else ""
                
                results.append({
                    "metric_name": "log2_tau",
                    "metric_value": metric_value,
                    "instances_tested": 1,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                })
    
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        all_results.extend(result["trials"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        result_type = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in all_results):
        result_type = "FALSIFIED"
    else:
        result_type = "INCONCLUSIVE"
    
    print(json.dumps({
        f"RESULT": result_type,
        "mean": mean_value,
        "std": std_value,
        "support_fraction": support_fraction
    }))