# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [identity]
        for _ in range(2, n+1):
            A.append(matrix_multiply(matrix, A[-1]))
        det = Fraction(0)
        for i in range(n):
            sign = (-1) ** (i % 2)
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            submatrix = [col[:i] + col[i+1:] for col in zip(*submatrix)]
            det += sign * matrix[0][i] * determinant(submatrix)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return Fraction(matrix[0][0])
        det = Fraction(0)
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            submatrix = [col[:i] + col[i+1:] for col in zip(*submatrix)]
            det += (-1) ** i * matrix[0][i] * determinant(submatrix)
        return det
    
    def p_adic_roots(det, p):
        roots = set()
        x = 0
        while True:
            if (det - x**2) % p == 0:
                roots.add(x)
                roots.add(-x)
            if x >= p:
                break
            x += 1
        return roots
    
    def rank(matrix):
        matrix = gaussian_elimination(matrix)
        return sum(1 for row in matrix if any(row[i] != 0 for i in range(len(row))))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = Fraction(0)
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            matrix = generate_random_matrix(n)
            det = characteristic_polynomial(matrix)
            p_adic_roots_set = p_adic_roots(det, 2)  # Assuming p=2 for simplicity
            rank_value = rank(matrix)
            instances_tested += 1
            n_max = max(n_max, n)
            total_ratio += len(p_adic_roots_set) / rank_value
    
    mean_ratio = total_ratio / (len(n_values) * 5)
    conjecture_holds = mean_ratio <= Fraction(3)
    
    return {
        "metric_name": "p-adic root count to rank variance ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")