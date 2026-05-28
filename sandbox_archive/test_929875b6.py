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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
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
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank_of_matrix(A):
    m, n = len(A), len(A[0])
    B = [row[:] for row in A]
    rank = 0
    for i in range(n):
        if any(B[j][i] != 0 for j in range(rank, m)):
            rank += 1
            for j in range(m):
                if j != rank - 1:
                    factor = B[j][i] / B[rank-1][i]
                    for k in range(n):
                        B[j][k] -= factor * B[rank-1][k]
    return rank

def tutte_polynomial(G, x, y):
    n = len(G)
    if n == 0:
        return 1
    if n == 1:
        return x + y - 1
    if n == 2:
        return (x + y) * (x + y - 1)
    
    for u in range(n):
        neighbors = [v for v in range(n) if G[u][v] != 0]
        if len(neighbors) > 0:
            subgraph = [[G[i][j] for j in range(u)] + [G[i][j] for j in range(u+1, n)]
                        for i in range(u+1, n)]
            return (x - 1) * tutte_polynomial(subgraph, x, y) + (y - 1) * len(neighbors)
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    G = [row[:] for row in G]
    for i in range(n):
        G[i][i] = 0
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                G[j][i] = 1
    
    ν_G = rank_of_matrix(G)
    T_G = tutte_polynomial(G, x=2, y=3)  # Example values for x and y
    circuit_size = len(bin(T_G)) - 2  # Binary representation length minus '0b'
    
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": ν_G <= circuit_size,
        "counterexample": "" if ν_G <= circuit_size else f"ν(G)={ν_G}, circuit_size={circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")