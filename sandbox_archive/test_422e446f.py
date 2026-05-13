# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += (-1) ** i * A[0][i] * determinant(submatrix)
    return det

def inverse(A):
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    n = len(A)
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1) ** (i + j) * determinant(submatrix)
            adjoint[j][i] = cofactor
    return matrix_multiplication(adjoint, [[Fraction(1, det_A)] * n for _ in range(n)])

def lex_maximal_hypergraph(n):
    V = list(range(n))
    E = []
    for k in range(2, n + 1):
        for comb in itertools.combinations(V, k):
            E.append(comb)
    return E

def algebraically_shifted_hypergraph(E):
    m = len(E)
    A = [[0] * (m + 1) for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            if all(x in E[i] and x not in E[j] for x in E[i]):
                A[i][j] = 1
            if all(x in E[j] and x not in E[i] for x in E[j]):
                A[j][i] = 1
    A[m] = [1] * m + [0]
    A = gaussian_elimination(A)
    shifted_E = []
    for i in range(m):
        if A[i][-1] == 1:
            shifted_E.append(E[i])
    return shifted_E

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, n**2)
    E = lex_maximal_hypergraph(n)
    DNF = [random.sample(E, random.randint(1, len(E))) for _ in range(m)]
    
    shifted_E = algebraically_shifted_hypergraph(E)
    E_shifted = sum(len(shifted_E), 0)
    
    if E_shifted > log(n) + 2 * sqrt(m):
        conjecture_holds = False
        counterexample = "E_shifted > log(n) + 2*sqrt(m)"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "E_shifted",
        "metric_value": E_shifted,
        "instances_tested": m,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_E_shifted = sum(r["metric_value"] for r in results) / len(results)
    std_E_shifted = (sum((r["metric_value"] - mean_E_shifted)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_E_shifted} std={std_E_shifted} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"E_shifted > log(n) + 2*sqrt(m)\" first_failing_seed={first_failing_seed}"
    
    print(result)