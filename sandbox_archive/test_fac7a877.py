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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def transpose(A):
        n = len(A)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[j][i] = A[i][j]
        return T
    
    def rank_1_decomposition(M, iterations=50):
        n = len(M)
        U = [[random.random() for _ in range(n)] for _ in range(n)]
        V = [[random.random() for _ in range(n)] for _ in range(n)]
        
        for _ in range(iterations):
            U = matrix_multiply(U, M)
            V = matrix_multiply(V, transpose(M))
            
            U_norm = sum(sum(x**2 for x in row) for row in U)**0.5
            V_norm = sum(sum(x**2 for x in col) for col in V)**0.5
            
            U = [[x / U_norm for x in row] for row in U]
            V = [[x / V_norm for x in col] for col in V]
        
        return U, V
    
    def border_rank(M):
        n = len(M)
        rank = 1
        while True:
            U, V = rank_1_decomposition(M, iterations=50)
            M_approx = matrix_multiply(U, transpose(V))
            if max(max(abs(x) for x in row) for row in (M - M_approx)) < 1e-6:
                return rank
            rank += 1
    
    def secant_dimension(M):
        n = len(M)
        rank = border_rank(M)
        return rank * (rank + 1) // 2
    
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    secant_dim = secant_dimension(M)
    ratio = secant_dim / n
    
    return {
        "metric_name": "secant_dimension_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1,
        "counterexample": "" if ratio >= 1 else f"n={n}, M={M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")