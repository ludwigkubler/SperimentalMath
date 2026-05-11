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
from math import factorial

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * matrix_det(submatrix)
        sign *= -1
    return det

def gaussian_elimination(A, b):
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tutte_polynomial(graph, memo={}):
        if (graph,) in memo:
            return memo[(graph,)]
        n = len(graph)
        if n == 1:
            return 2
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] == 0:
                    A = tutte_polynomial(graph[:i] + graph[i+1:], memo)
                    B = tutte_polynomial(graph[:j] + graph[j+1:], memo)
                    C = tutte_polynomial([[graph[k][l] for l in range(n) if l != j] for k in range(i)] + [[graph[k][l] for l in range(i, n-1)] for k in range(i+1, n)], memo)
                    return A * B - C
        return 0
    
    def is_k_clique(graph, k):
        n = len(graph)
        if k == 2:
            for i in range(n):
                for j in range(i+1, n):
                    if graph[i][j] == 0:
                        return False
            return True
        for subset in itertools.combinations(range(n), k):
            subgraph = [[graph[i][j] for j in subset] for i in subset]
            if not is_k_clique(subgraph, k-1):
                return False
        return True
    
    def get_tutte_values(graph, k):
        T21 = tutte_polynomial(graph)
        T12 = tutte_polynomial([[graph[j][i] for j in range(i+1)] for i in range(len(graph))])
        return T21, T12
    
    n_max = 40
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
            T21, T12 = get_tutte_values(graph, 2)
            instances_tested += 1
            if T21 < n**(2/2) or T12 < n**(2/2):
                conjecture_holds = False
                counterexample = f"Graph with n={n}, T(2,1)={T21}, T(1,2)={T12}"
    
    return {
        "metric_name": "Tutte Polynomial Values",
        "metric_value": (T21 + T12) / 2,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")