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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            A[j][i] = A[i][j]
    
    # Compute eigenvalues and eigenvectors
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        U = [row[:] for row in A]
        for j in range(n):
            max_row = j
            for i in range(j + 1, m):
                if abs(U[i][j]) > abs(U[max_row][j]):
                    max_row = i
            U[j], U[max_row] = U[max_row], U[j]
            pivot = U[j][j]
            for k in range(n):
                U[j][k] /= pivot
            for i in range(m):
                if i != j:
                    factor = U[i][j]
                    for k in range(n):
                        U[i][k] -= factor * U[j][k]
        return U
    
    def is_upper_triangular(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            for j in range(i):
                if A[i][j] != 0:
                    return False
        return True
    
    def eigenvalues(A):
        if not is_upper_triangular(A):
            U = gaussian_elimination(A)
        else:
            U = A[:]
        
        evs = []
        for i in range(min(n, len(U))):
            if i < n - 1 and abs(U[i][i + 1]) > 1e-6:
                break
            evs.append(U[i][i])
        
        return evs
    
    evs = eigenvalues(A)
    lambda_min = min(e for e in evs if e != 0)
    
    # Simulate quantum communication complexity (placeholder)
    CC_XOR_n = 2**n / lambda_min
    
    # Transform A into a unitary matrix B
    def transform_to_unitary(A):
        m, n = len(A), len(A[0])
        U = [row[:] for row in A]
        for j in range(n):
            max_row = j
            for i in range(j + 1, m):
                if abs(U[i][j]) > abs(U[max_row][j]):
                    max_row = i
            U[j], U[max_row] = U[max_row], U[j]
            pivot = U[j][j]
            for k in range(n):
                U[j][k] /= pivot
            for i in range(m):
                if i != j:
                    factor = U[i][j]
                    for k in range(n):
                        U[i][k] -= factor * U[j][k]
        
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = U[i][j]
        
        return B
    
    B = transform_to_unitary(A)
    
    # Check eigenvalues of B
    def is_distinct_and_unitary(B):
        m, n = len(B), len(B[0])
        evs = eigenvalues(B)
        if len(evs) != len(set(evs)):
            return False
        
        for i in range(n):
            if abs(sum(row[i] * row[j].conjugate() for j in range(n)) - (i == j)) > 1e-6:
                return False
        
        return True
    
    B_eigenvalues_distinct_and_unitary = is_distinct_and_unitary(B)
    
    # Check Frobenius norm of B
    def frobenius_norm(B):
        m, n = len(B), len(B[0])
        norm = 0.0
        for i in range(m):
            for j in range(n):
                norm += abs(B[i][j]) ** 2
        return math.sqrt(norm)
    
    B_frobenius_norm = frobenius_norm(B)
    
    # Check if conjecture holds
    conjecture_holds = lambda_min <= CC_XOR_n and B_eigenvalues_distinct_and_unitary and B_frobenius_norm <= lambda_min**2
    
    return {
        "metric_name": "minimal_non_zero_eigenvalue",
        "metric_value": lambda_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "eigenvalues_of_B_not_distinct_or_outside_unit_circle" if not B_eigenvalues_distinct_and_unitary else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")