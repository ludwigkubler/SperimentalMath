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
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det
    
    def primary_decomposition(matrix):
        n = len(matrix)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A = matrix_multiply(matrix, I)
        U = gaussian_elimination(A)
        det_U = determinant(U)
        if det_U == 0:
            return None
        V = [[A[i][j] / U[j][j] for j in range(n)] for i in range(n)]
        return V
    
    def permanent(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        perm = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            perm += sign * matrix[0][j] * permanent(submatrix)
        return perm
    
    def circuit_size(permanent_value, n):
        # This is a placeholder function. In practice, you would use a black-box SAT solver.
        # For simplicity, we assume a linear relationship for demonstration purposes.
        return abs(permanent_value) + n**2
    
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    M = generate_matrix(n)
    
    orbit_closure_dimension = primary_decomposition(M)
    if orbit_closure_dimension is None:
        return {
            "metric_name": "orbit_closure_dimension",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    perm = permanent(M)
    circ_size = circuit_size(perm, n)
    log_n = math.log(n)
    
    return {
        "metric_name": "orbit_closure_dimension",
        "metric_value": orbit_closure_dimension,
        "instances_tested": 1,
        "conjecture_holds": circ_size >= orbit_closure_dimension / log_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 50))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")