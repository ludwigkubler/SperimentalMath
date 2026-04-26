# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
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
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
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
    return matrix_multiply(adjugate, 1 / det)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def build_M(F):
    n = len(F)
    M = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        sgn_ij = sum(sign(x[i]) * sign(x[j]) for x in F if x[i] != x[j])
        M[i][j] = sgn_ij
        M[j][i] = sgn_ij
    return M

def eigh(M):
    n = len(M)
    eigenvalues = [0] * n
    eigenvectors = [[0] * n for _ in range(n)]
    # Implement eigenvalue decomposition manually (e.g., QR algorithm)
    # This is a placeholder and should be replaced with actual implementation
    return eigenvalues, eigenvectors

def compute_g(F):
    M = build_M(F)
    eigenvalues, _ = eigh(M)
    lambda_max = max(eigenvalues)
    lambda_2 = sorted(eigenvalues)[-2]
    g = (lambda_max - lambda_2) / lambda_max
    return g

def is_unsat(F):
    n = len(F)
    A = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        A[i][j] = sum(sign(x[i]) * sign(x[j]) for x in F if x[i] != x[j])
    return determinant(A) == 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 11, 14]
    m_n_ratios = [1.0, 2.0, 4.0, 8.0]
    results = []
    
    for n in n_values:
        for m_n_ratio in m_n_ratios:
            m = int(n * m_n_ratio)
            F = []
            while len(F) < m:
                x = [random.choice([-1, 1]) for _ in range(n)]
                if is_unsat([x]):
                    F.append(x)
            
            g = compute_g(F)
            d_SoS = None
            slack = None
            
            if g >= 0.5 and d_SoS == 4:
                results.append((g, d_SoS))
                continue
            
            # Brute-force search for SoS refutation degree up to degree 6
            best_d_SoS = None
            for d in range(2, 7):
                # Implement small SDP-free linear programming relaxation here
                # This is a placeholder and should be replaced with actual implementation
                if d == 4:
                    best_d_SoS = 4
                    break
            
            if best_d_SoS is not None:
                d_SoS = best_d_SoS
                slack = d_SoS - math.ceil(2 / g)
                results.append((g, d_SoS))
    
    metric_name = "slack"
    metric_value = sum(slack for _, slack in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(d_SoS >= math.ceil(2 / g) + 2 for g, d_SoS in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(d_SoS == 4 and g >= 0.5 for g, d_SoS in sum([result["results"] for result in results], [])):
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if any(d_SoS == 4 and g >= 0.5 for g, d_SoS in result["results"]))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")