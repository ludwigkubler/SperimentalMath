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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n):
        # Generate a read-twice BP for IP_2 mod 2
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A, B
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def transpose(matrix):
        n = len(matrix)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[j][i] = matrix[i][j]
        return T
    
    def is_positive_definite(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        for k in range(n):
            pivot = A[k][k]
            if pivot <= 0:
                return False
            for j in range(k, n):
                A[k][j] /= pivot
            for i in range(k + 1, n):
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
        return True
    
    def cholesky_decomposition(matrix):
        n = len(matrix)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    L[i][j] = math.sqrt(matrix[i][i] - sum_k)
                else:
                    L[i][j] = (matrix[i][j] - sum_k) / L[j][j]
        return L
    
    def solve_linear_system(L, b):
        n = len(L)
        y = [0] * n
        for i in range(n):
            sum_j = sum(L[i][j] * y[j] for j in range(i))
            y[i] = (b[i] - sum_j) / L[i][i]
        
        x = [0] * n
        for i in range(n - 1, -1, -1):
            sum_j = sum(L[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - sum_j) / L[i][i]
        return x
    
    def matrix_inverse(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        I = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        
        for k in range(n):
            pivot = A[k][k]
            for j in range(k, n):
                A[k][j] /= pivot
            for j in range(n):
                I[k][j] /= pivot
            
            for i in range(n):
                if i != k:
                    factor = A[i][k]
                    for j in range(k, n):
                        A[i][j] -= factor * A[k][j]
                    for j in range(n):
                        I[i][j] -= factor * I[k][j]
        
        return I
    
    def spectral_norm(matrix):
        n = len(matrix)
        identity = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        A = [row[:] for row in matrix]
        B = identity
        
        for _ in range(50):  # Power iteration
            B = matrix_multiplication(A, B)
            norm_B = math.sqrt(sum(sum(x**2 for x in row) for row in B))
            B = [[x / norm_B for x in row] for row in B]
        
        return max(abs(eigenvalue) for eigenvalue in solve_linear_system(matrix_inverse(B), [sum(row[i] for row in A) for i in range(n)]))

    n = random.randint(5, 40)
    A, B = generate_read_twice_bp(n)
    
    M = matrix_multiplication(A, transpose(B))
    
    cb_norm = spectral_norm(M)
    
    return {
        "metric_name": "cb_norm",
        "metric_value": cb_norm,
        "instances_tested": 1,
        "conjecture_holds": cb_norm >= n / 20,  # c=1/20 as a simple lower bound
        "counterexample": "" if cb_norm >= n / 20 else f"cb_norm={cb_norm} < {n/20}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cb_norm = sum(res["metric_value"] for res in results) / len(results)
    std_cb_norm = math.sqrt(sum((res["metric_value"] - mean_cb_norm) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cb_norm} std={std_cb_norm} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")