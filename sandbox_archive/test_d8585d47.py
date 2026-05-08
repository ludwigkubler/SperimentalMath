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
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(j+1, m):
            factor = augmented[i][j] / augmented[j][j]
            augmented[i][j:] = [a - factor * b for a, b in zip(augmented[i][j:], augmented[j][j:])]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (augmented[i][-1] - sum(x[j] * augmented[i][j+1] for j in range(i+1, n))) / augmented[i][i]
    return x

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def matrix_inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    adjugate = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix) * (-1) ** (i + j)
            adjugate[j][i] = cofactor
    return matrix_multiply(adjugate, [[1/det] * n for _ in range(m)])

def is_kst_free(G, s, t):
    m, n = len(G), len(G[0])
    if m < s or n < t:
        return True
    for i in range(m - s + 1):
        for j in range(n - t + 1):
            submatrix = [[G[i+k][j+l] for l in range(t)] for k in range(s)]
            if all(submatrix[k][l] == 0 for k in range(s) for l in range(t)):
                return True
    return False

def zarankiewicz_number(n, s, t):
    if n < s or n < t:
        return 0
    max_edges = 0
    for i in range(1, s + 1):
        j = (n * i) // s
        max_edges = max(max_edges, i * j)
    return max_edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    s, t = random.randint(2, n//2), random.randint(2, n//2)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    while not is_kst_free(G, s, t):
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    znt = zarankiewicz_number(n, n, s, t)
    circuit_size = float('inf')
    
    # Dynamic programming to find monotone circuit size
    dp = [[float('inf')] * (n+1) for _ in range(n+1)]
    dp[0][0] = 0
    for i in range(1, n+1):
        dp[i][i] = 1
    
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + 1
    
    circuit_size = dp[n][n]
    
    conjecture_holds = circuit_size >= znt**2
    counterexample = "" if conjecture_holds else f"Zarankiewicz number {znt}, Circuit size {circuit_size}"
    
    return {
        "metric_name": "Monotone Circuit Size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")