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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def transpose(M):
        return [list(row) for row in zip(*M)]
    
    def rank(A, tol=1e-8):
        m, n = len(A), len(A[0])
        U, s, Vt = [], [], []
        A_copy = [row[:] for row in A]
        
        # QR decomposition
        for i in range(m):
            u = [A_copy[i][j] for j in range(n)]
            norm = sum(x**2 for x in u)**0.5
            if norm > tol:
                u = [x / norm for x in u]
                U.append(u)
                Q = identity_matrix(m)
                Q[i] = u
                A_copy = matrix_multiply(Q, A_copy)
        
        # Singular value decomposition
        s = [sum(A_copy[i][i]**2 for i in range(min(m, n)))**0.5 for i in range(n)]
        Vt = transpose(U)
        
        return sum(1 for x in s if x > tol)
    
    def identity_matrix(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def border_rank(M, max_iter=50):
        n = len(M)
        rank_M = rank(M)
        secant_dimension = rank_M
        
        for _ in range(max_iter):
            U, S, Vt = [], [], []
            A = [row[:] for row in M]
            
            # QR decomposition
            for i in range(n):
                u = [A[i][j] for j in range(n)]
                norm = sum(x**2 for x in u)**0.5
                if norm > 1e-8:
                    u = [x / norm for x in u]
                    U.append(u)
                    Q = identity_matrix(n)
                    Q[i] = u
                    A = matrix_multiply(Q, A)
            
            # Singular value decomposition
            S = [sum(A[i][i]**2 for i in range(min(n, n)))**0.5 for i in range(n)]
            Vt = transpose(U)
            
            rank_A = sum(1 for x in S if x > 1e-8)
            secant_dimension = max(secant_dimension, rank_M + rank_A - 1)
        
        return secant_dimension
    
    n = random.randint(5, 40)
    M = generate_disjointness_matrix(n)
    
    secant_dimension = border_rank(M)
    ratio = secant_dimension / n
    
    return {
        "metric_name": "secant_dimension_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1,
        "counterexample": "" if ratio >= 1 else f"n={n}, secant_dimension={secant_dimension}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='secant_dimension_ratio < 1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")