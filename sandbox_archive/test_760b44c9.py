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
    
    def matrix_add(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C
    
    def matrix_scalar_multiply(A, c):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] * c
        return C
    
    def matrix_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += abs(A[i][j])
        return norm
    
    def generate_read_twice_bp(n: int) -> list:
        bp = [[0] * (n + 1) for _ in range(2 ** n)]
        for i in range(2 ** n):
            for j in range(n):
                if i & (1 << j):
                    bp[i][j] = 1
                else:
                    bp[i][j] = -1
        return bp
    
    def noncommutative_fourier_transform(bp: list, n: int) -> float:
        identity_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            identity_matrix[i][i] = 1
        
        fourier_transform = matrix_multiply(bp[0], identity_matrix)
        for i in range(1, 2 ** n):
            fourier_transform = matrix_add(fourier_transform, bp[i])
        
        return matrix_norm(fourier_transform)
    
    n = 40
    bp = generate_read_twice_bp(n)
    operator_norm = noncommutative_fourier_transform(bp, n)
    
    return {
        "metric_name": "operator_norm",
        "metric_value": operator_norm,
        "instances_tested": 1,
        "conjecture_holds": operator_norm >= n,
        "counterexample": "" if operator_norm >= n else "Noncommutative Fourier norm < n"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Noncommutative Fourier norm < n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")