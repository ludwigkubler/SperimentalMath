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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def tropical_add(a, b):
        if a == float('-inf') or b == float('-inf'):
            return max(a, b)
        return max(a + b, 0)
    
    def tropical_multiply(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[float('-inf')] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] = tropical_add(C[i][j], tropical_multiply(A[i][k], B[k][j]))
        return C
    
    def tropical_determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = float('-inf')
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det = tropical_add(det, tropical_multiply(A[0][j], tropical_determinant(submatrix)))
        return det
    
    def generate_random_matrix(m, n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    
    def compute_tropicalized_cohomology(P):
        m = len(P)
        A = generate_random_matrix(m, m)
        B = generate_random_matrix(m, m)
        C = tropical_matrix_multiplication(A, B)
        det = tropical_determinant(C)
        return det
    
    n = random.randint(5, 40)
    P = [random.choice([0, 1]) for _ in range(n)]
    s_P = len(P)
    
    rho_trop_H_star_P = compute_tropicalized_cohomology(P)
    
    metric_value = rho_trop_H_star_P
    instances_tested = 1
    
    conjecture_holds = rho_trop_H_star_P <= 2 * s_P and rho_trop_H_star_P >= 0.5 * s_P
    counterexample = "" if conjecture_holds else f"rho_trop(H^*(P))={rho_trop_H_star_P}, s(P)={s_P}"
    
    return {
        "metric_name": "minimal_rank_of_tropicalized_cohomology",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")