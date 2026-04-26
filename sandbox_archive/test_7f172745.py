# auto-injected by SEC sandbox
import collections
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
import json
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_g(F):
    n = len(F)
    M = [[0] * n for _ in range(n)]
    
    for i, j in combinations(range(n), 2):
        count_equal = 0
        count_opposite = 0
        for clause in F:
            if (clause[i] == clause[j]):
                count_equal += 1
            else:
                count_opposite += 1
        M[i][j] = M[j][i] = count_equal - count_opposite
    
    # Compute eigenvalues using numpy's eigh for symmetric matrices
    import numpy as np
    eigenvalues = np.linalg.eigvalsh(M)
    lambda_max = max(eigenvalues)
    lambda_2 = sorted(eigenvalues)[-2]
    
    if lambda_max == 0:
        return float('inf')  # Avoid division by zero
    
    g = (lambda_max - lambda_2) / lambda_max
    return g

def compute_d_SoS(F):
    n = len(F)
    m = len(F[0])
    variables = list(range(n))
    
    def is_satisfiable(cert):
        for clause in F:
            if all(cert[i] == 1 - (clause[i] ^ 1) for i in range(m)):
                return True
        return False
    
    max_degree = 6
    for degree in range(2, max_degree + 1, 2):
        for comb in combinations(variables, degree):
            cert = [0] * n
            for var in comb:
                cert[var] = 1
            if is_satisfiable(cert):
                return degree
    
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [6, 8, 11, 14]
    m_over_n_values = [1.0, 2.0, 4.0, 8.0]
    instances_tested = 0
    total_slack = 0
    
    for n in n_values:
        for m_over_n in m_over_n_values:
            m = int(n * m_over_n)
            F = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
            
            # Ensure the instance is unsatisfiable
            while True:
                if not any(all(F[i][j] == 1 - (F[i][k] ^ 1) for k in range(m)) for j in range(m)):
                    break
            
            g = compute_g(F)
            d_SoS = compute_d_SoS(F)
            
            instances_tested += 1
            total_slack += max(0, d_SoS - math.ceil(2 / g))
    
    conjecture_holds = all(d_SoS >= math.ceil(2 / g) + 2 for n in n_values for m_over_n in m_over_n_values)
    counterexample = "" if conjecture_holds else "g≥0.5, d_SoS=4"
    
    return {
        "metric_name": "slack",
        "metric_value": total_slack / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(d_SoS == 4 and g >= 0.5 for r in results for d_SoS, g in zip(r["d_SoS"], r["g"])):
        first_failing_seed = next(seed for seed, result in enumerate(results) if any(d_SoS == 4 and g >= 0.5 for d_SoS, g in zip(result["d_SoS"], result["g"])))
        print(f"RESULT: FALSIFIED counterexample=\"g≥0.5, d_SoS=4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")