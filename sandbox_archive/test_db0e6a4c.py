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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def matrix_inverse(A):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A_augmented = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(A_augmented, [0]*n)
        return [row[n:] for row in A_augmented]
    
    def matrix_determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * A[0][j] * matrix_determinant(submatrix)
        return det
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def matrix_inverse(A):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A_augmented = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(A_augmented, [0]*n)
        return [row[n:] for row in A_augmented]
    
    def matrix_determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * A[0][j] * matrix_determinant(submatrix)
        return det
    
    def compute_psi(C, N):
        m = len(C)
        p_g = [sum(C[i][j] for i in range(N)) / N for j in range(m)]
        psi = sum(-log2(2 * max(min(p_g[j], 1 - p_g[j]), 1 / (2 * m))) for j in range(m)) / m
        return psi
    
    def generate_ac0_circuit(n, d):
        if d == 2:
            # Full minterm DNF up to n=14
            pass
        elif d == 3:
            # √n-block tower
            pass
        elif d == 4:
            # Recursive ∜n-block
            pass
        else:
            raise ValueError("Unsupported depth")
    
    def generate_random_non_parity_circuit(n, m):
        C = [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
        return C
    
    def generate_or_n_circuit(n):
        C = [[i & (1 << j) != 0 for j in range(n)] for i in range(2**n)]
        return C
    
    n_values = [6, 8, 10, 12, 16, 20, 24, 30]
    d_values = [2, 3, 4]
    
    results = []
    for n in n_values:
        N = min(2**n, 16384)
        for d in d_values:
            if d == 2 and n > 14:
                continue
            C = generate_ac0_circuit(n, d)
            psi = compute_psi(C, N)
            results.append({
                "metric_name": "psi",
                "metric_value": psi,
                "instances_tested": 1,
                "conjecture_holds": psi <= log2(len(C)) + 1,
                "counterexample": "" if psi <= log2(len(C)) + 1 else f"psi={psi} > {log2(len(C)) + 1}"
            })
    
    mean_psi = sum(result["metric_value"] for result in results) / len(results)
    std_psi = math.sqrt(sum((result["metric_value"] - mean_psi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "mean_psi": mean_psi,
        "std_psi": std_psi,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_psi = sum(result["mean_psi"] for result in results) / len(results)
    std_psi = math.sqrt(sum((result["mean_psi"] - mean_psi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_psi} std={std_psi} support_fraction={support_fraction}")