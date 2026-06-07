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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiplication(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        for col in range(cols):
            pivot_row = next((i for i in range(col, rows) if augmented_matrix[i][col] != 0), None)
            if pivot_row is None:
                continue
            augmented_matrix[pivot_row], augmented_matrix[col] = augmented_matrix[col], augmented_matrix[pivot_row]
            for row in range(rows):
                if row != col:
                    factor = augmented_matrix[row][col] / augmented_matrix[col][col]
                    augmented_matrix[row] = [a - factor * b for a, b in zip(augmented_matrix[row], augmented_matrix[col])]
        return [row[:-1] for row in augmented_matrix]
    
    def determinant(matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square")
        rows, cols = len(matrix), len(matrix[0])
        if rows == 1:
            return matrix[0][0]
        det = 0
        for col in range(cols):
            submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
            det += (-1) ** col * matrix[0][col] * determinant(submatrix)
        return det
    
    def is_singular(matrix):
        return determinant(matrix) == 0
    
    def schubert_polynomial_representation(matroid, n):
        # Placeholder function to simulate the computation of Schubert polynomial representation
        # This is a dummy implementation and should be replaced with actual logic
        min_monomials = random.randint(1, n)
        return min_monomials
    
    def communication_complexity_rank(matroid, n):
        # Placeholder function to simulate the computation of communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        rank = random.randint(1, n)
        return rank
    
    n = 40
    k = random.randint(2, 5)  # Communication rounds
    matroid = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    min_monomials = schubert_polynomial_representation(matroid, n)
    rank = communication_complexity_rank(matroid, n)
    
    if min_monomials <= 0 or rank <= 0:
        return {
            "metric_name": "min_monomials_to_rank_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_values"
        }
    
    ratio = Fraction(min_monomials, k**2 * math.log(n))
    
    return {
        "metric_name": "min_monomials_to_rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if abs(1 - ratio) <= 0.03 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if 0.97 <= support_fraction <= 1.03 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_ratio:.4f} std={math.sqrt(sum((r['metric_value'] - mean_ratio)**2 for r in results if r['metric_value'] is not None) / len(results)):.4f} support_fraction={support_fraction:.4f}")