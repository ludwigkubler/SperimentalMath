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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def operator_norm(matrix):
        n = len(matrix)
        max_norm = 0
        for i in range(n):
            row_norm = sum(abs(matrix[i][j]) for j in range(n))
            if row_norm > max_norm:
                max_norm = row_norm
        return max_norm
    
    def r_transform(matrix):
        n = len(matrix)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix
        B = I
        for _ in range(20):  # Approximate R-transform with 20 iterations
            A, B = B, matrix_multiply(B, A)
        return B
    
    def free_cumulant_transform(matrix):
        n = len(matrix)
        R = r_transform(matrix)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    C[i][j] = 1
                else:
                    C[i][j] = -R[i][j]
        return C
    
    def ip2_bp(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = 1 / math.sqrt(2)
                A[j][i] = 1 / math.sqrt(2)
        return A
    
    def random_bp(n):
        A = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        gaussian_elimination(A)
        return A
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    if seed % 2 == 0:
        P = ip2_bp(n)
        target_norm = 0.9 * n
    else:
        P = random_bp(n)
        target_norm = 1.2 * math.log(n)
    
    C = free_cumulant_transform(P)
    norm = operator_norm(C)
    
    return {
        "metric_name": "operator_norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": (norm >= target_norm) if seed % 2 == 0 else (norm <= target_norm),
        "counterexample": "" if seed % 2 == 0 else f"Random BP with n={n} failed"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Random BP failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")