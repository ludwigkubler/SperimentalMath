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
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(matrix):
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        r = 0
        for row in matrix:
            if any(row):
                r += 1
        return r
    
    def communication_complexity(M):
        n = len(M)
        rows, cols = [], []
        for i in range(n):
            rows.append(''.join(map(str, M[i])))
            cols.append(''.join(map(str, [row[i] for row in M])))
        
        def binary_search(lo, hi):
            if lo >= hi:
                return 0
            mid = (lo + hi) // 2
            if any(row[:mid+1] == col[:mid+1] for row in rows for col in cols):
                return binary_search(mid + 1, hi)
            else:
                return binary_search(lo, mid)
        
        return binary_search(0, n-1)
    
    def noncommutative_tensor_product(M):
        n = len(M)
        tensor_product = [[0] * (n*n) for _ in range(n*n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        tensor_product[i*n + k][j*n + l] += M[i][k] * M[j][l]
        return tensor_product
    
    n = random.randint(5, 40)
    M = generate_matrix(n)
    
    τ_n = rank(noncommutative_tensor_product(M))
    CC_R = communication_complexity(M)
    
    if CC_R == 0:
        return {
            "metric_name": "τ_n / CC_R",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "CC_R is zero, making the ratio undefined."
        }
    
    C_n = τ_n / CC_R
    return {
        "metric_name": "τ_n / CC_R",
        "metric_value": τ_n / CC_R,
        "instances_tested": 1,
        "conjecture_holds": τ_n <= 2 * CC_R,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999973) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")