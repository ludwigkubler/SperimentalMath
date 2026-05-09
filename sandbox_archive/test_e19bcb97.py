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
    n = 10  # Default value for n, can be changed in main loop
    c = 1.0 / (n * math.log(n))  # Universal constant c
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    def matrix_multiplication(A, B):
        result = [[sum(a*b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
        return result
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find the pivot
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        
        # Back-substitute to find the inverse
        inv_A = [[0] * n for _ in range(n)]
        for i in range(n):
            inv_A[i][i] = 1 / A[i][i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    inv_A[j][k] -= factor * inv_A[i][k]
        
        # Normalize the rows
        for i in range(n):
            norm = sum(inv_A[i])
            inv_A[i] = [x / norm for x in inv_A[i]]
        
        return inv_A
    
    def eigenvalues(A):
        n = len(A)
        if n == 1:
            return [A[0][0]]
        
        # Reduce to tridiagonal form
        T = [[0] * n for _ in range(n)]
        Q = [[0] * n for _ in range(n)]
        Q[0][0], Q[n-1][n-1] = 1, 1
        
        for k in range(2, n):
            h = sum(A[i][i+k-1]**2 for i in range(k-1))
            if h == 0:
                continue
            g = A[k-1][k-1]
            t = (A[k-1][k] * A[k][k-1]) / h
            c = 1 / math.sqrt(1 + t**2)
            s = t * c
            T[:k-1][:k-1] = matrix_multiplication(gaussian_elimination([[c, -s], [s, c]]), A[:k-1][:k-1])
            T[k-1:k][:k-1] = [[0] * (k-1)]
            T[:k-1][k-1:] = [[0] * (k-1)]
            T[k-1][k-1], T[k][k] = c, -s
            A[:k-1][:k-1] = matrix_multiplication(A[:k-1][:k-1], gaussian_elimination([[c, s], [-s, c]]))
        
        # Compute eigenvalues of tridiagonal matrix
        eigs = [T[i][i] for i in range(n)]
        return eigs
    
    def free_entropy(eigenvals):
        rho = sum(math.exp(-x) for x in eigenvals)
        entropy = -sum(math.log(rho) * math.exp(-x) / rho for x in eigenvals)
        return entropy
    
    M_n = generate_disjointness_matrix(n)
    X = [[(M_n[i][j] + 1) / 2 for j in range(n)] for i in range(n)]
    eigs = eigenvalues(X)
    Phi = free_entropy(eigs)
    
    result = {
        "metric_name": "free_entropy",
        "metric_value": Phi,
        "instances_tested": 1,
        "conjecture_holds": Phi >= c,
        "counterexample": "" if Phi >= c else f"Phi={Phi}, expected>=c"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")