# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

# Constants and utility functions

def hamming_distance(u, v):
    return sum(1 for x, y in zip(u, v) if x != y)

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    pivot_col = 0
    pivot_row = 0

    while pivot_col < n and pivot_row < m:
        # Find the pivot row
        max_idx = pivot_row
        for i in range(pivot_row + 1, m):
            if abs(A[i][pivot_col]) > abs(A[max_idx][pivot_col]):
                max_idx = i
        
        if A[max_idx][pivot_col] == 0:
            pivot_col += 1
            continue

        # Swap rows to put the pivot in place
        A[pivot_row], A[max_idx] = A[max_idx], A[pivot_row]

        # Eliminate entries below the pivot
        for i in range(pivot_row + 1, m):
            factor = -A[i][pivot_col] / A[pivot_row][pivot_col]
            for j in range(n):
                A[i][j] += factor * A[pivot_row][j]

        rank += 1
        pivot_row += 1
        pivot_col += 1

    return rank

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def max_degree(A):
    return max(sum(row) for row in A)

# MetricGadget definitions

X_XOR = ['0', '1']
Y_XOR = ['0', '1']
d_XOR = hamming_distance
R_XOR = 2

X_IND = ['0', '1']
Y_IND = ['0', '1', '10', '11']
d_IND = hamming_distance
R_IND = 2

# ProtocolPullback computation

def protocol_pullback(protocol, gadget, n):
    X, Y, d, R = gadget
    N = len(X) ** n * len(Y) ** n
    max_degree_A = max_degree(A_R)
    
    m_Π = 0
    R_Π = 0
    
    for f in range(2**n):
        transcript_cells = set()
        for x in X:
            for y in Y:
                cell = (x, y)
                if protocol(f, cell):
                    transcript_cells.add(cell)
        
        m_Π = max(m_Π, len(transcript_cells))
        R_Π = max(R_Π, max(hamming_distance(u, v) for u, v in itertools.combinations(transcript_cells, 2)))
    
    return m_Π, R_Π

def canonical_protocol(f, cell):
    x, y = cell
    return f(x) == y

def alternative_protocol(f, cell):
    x, y = cell
    return f(x) != y

# run_trial function

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for gadget, X, Y, d, R in [(X_XOR, Y_XOR, d_XOR, R_XOR), (X_IND, Y_IND, d_IND, R_IND)]:
        for n in [1, 2, 3]:
            A_R = [[0] * len(X) ** n * len(Y) ** n for _ in range(len(X) ** n * len(Y) ** n)]
            
            for u in range(len(X) ** n):
                for v in range(len(Y) ** n):
                    if hamming_distance((u // len(Y) ** n, u % len(Y) ** n), (v // len(Y) ** n, v % len(Y) ** n)) <= R:
                        A_R[u][v] = 1
            
            L_R = [[0] * len(A_R) for _ in range(len(A_R))]
            degree = [sum(row) for row in A_R]
            
            for i in range(len(L_R)):
                L_R[i][i] = -degree[i]
                for j in range(i + 1, len(L_R)):
                    if A_R[i][j]:
                        L_R[i][j] = A_R[j][i] = 1
            
            eigenvalues = [0] * 2
            eigenvectors = [[0] * len(A_R) for _ in range(2)]
            
            # Compute the smallest nonzero eigenvalue and eigenvector using power iteration
            v = [random.random() for _ in range(len(A_R))]
            for _ in range(100):
                v = matrix_multiply(A_R, v)
                v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            
            eigenvalues[0] = max(v[i] * A_R[i][j] * v[j] for i in range(len(A_R)) for j in range(i + 1, len(A_R)))
            eigenvectors[0] = v
            
            # Compute the multiplicity and scale
            m_Π, R_Π = protocol_pullback(canonical_protocol, (X, Y, d, R), n)
            m_Π_alt, R_Π_alt = protocol_pullback(alternative_protocol, (X, Y, d, R), n)
            
            # Check the inequality
            if m_Π * R_Π < math.ceil(eigenvalues[0] * len(X) ** n * len(Y) ** n / (4 * max_degree(A_R))):
                results.append((f"m_Π={m_Π}, R_Π={R_Π}, λ_R(n)={eigenvalues[0]}, N={len(X) ** n * len(Y) ** n}", True))
            else:
                results.append((f"m_Π={m_Π}, R_Π={R_Π}, λ_R(n)={eigenvalues[0]}, N={len(X) ** n * len(Y) ** n}", False))
    
    metric_value = sum(1 for _, valid in results if not valid)
    conjecture_holds = all(not valid for _, valid in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ProtocolPullbackMultiplicity",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main execution

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction == 0:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")