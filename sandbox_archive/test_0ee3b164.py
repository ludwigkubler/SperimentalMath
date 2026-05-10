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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return [row[:i+1] for row in A]

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_positive_definite(M):
    n = len(M)
    for i in range(n):
        if M[i][i] <= 0:
            return False
        factor = 1 / M[i][i]
        for j in range(i, n):
            M[i][j] *= factor
        for k in range(i+1, n):
            factor = M[k][i]
            for j in range(i, n):
                M[k][j] -= factor * M[i][j]
    return True

def max_cut_instance(n):
    # Generate a random Max-CUT instance
    edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(int(n*(n-1)/2))]
    weights = [random.random() for _ in range(len(edges))]
    return edges, weights

def moment_matrix(instance, degree):
    # Construct the moment matrix of a given degree
    edges, weights = instance
    n = len(set(u for u, v in edges))
    M = [[0] * (n**2) for _ in range(n**2)]
    for u, v in edges:
        idx_u = u * n + v
        idx_v = v * n + u
        M[idx_u][idx_u] += weights[edges.index((u, v))]
        M[idx_u][idx_v] -= weights[edges.index((u, v))]
        M[idx_v][idx_u] -= weights[edges.index((u, v))]
        M[idx_v][idx_v] += weights[edges.index((u, v))]
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instance = max_cut_instance(n)
    
    min_sos_degree = float('inf')
    negative_eigenvalues_count = 0
    
    for d in range(2, 11):
        M = moment_matrix(instance, d)
        eigenvalues = [abs(e) for e in gaussian_elimination(M)[-1]]
        negative_eigenvalues_count += sum(1 for e in eigenvalues if e < 1e-6)
        
        # Check if the matrix is positive definite
        if not is_positive_definite(M):
            min_sos_degree = d
            break
    
    conjecture_holds = min_sos_degree >= negative_eigenvalues_count + 1
    counterexample = "" if conjecture_holds else f"min_sos_degree={min_sos_degree}, negative_eigenvalues_count={negative_eigenvalues_count}"
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": min_sos_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")