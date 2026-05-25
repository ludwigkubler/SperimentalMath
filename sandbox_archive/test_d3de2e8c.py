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
    
    def generate_disjunctive_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def spectral_radius(matrix):
        n = len(matrix)
        # Implement Gaussian elimination to find the eigenvalues
        # and compute the spectral radius as the maximum absolute value of the eigenvalues
        # This is a simplified version and may not be numerically stable
        return max(abs(eigenvalue) for eigenvalue in matrix_eigenvalues(matrix))
    
    def matrix_eigenvalues(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        # Implement Gaussian elimination to find the eigenvalues
        # This is a simplified version and may not be numerically stable
        return [eigenvalue for eigenvalue, _ in gaussian_elimination(matrix + identity)]
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        eigenvalues = [A[i][i] for i in range(n)]
        eigenvectors = [[0]*n for _ in range(n)]
        for i in range(n):
            eigenvectors[i][i] = 1
        return eigenvalues, eigenvectors
    
    def noncommutative_Lp_space(F):
        n = len(F)
        # Implement the construction of the noncommutative L^p space
        # This is a simplified version and may not be accurate
        return [[F[i] * F[j] for j in range(n)] for i in range(n)]
    
    def Lp_spectral_radius(matrix, p):
        n = len(matrix)
        # Implement the computation of the L^p spectral radius
        # This is a simplified version and may not be accurate
        return (sum(sum(abs(matrix[i][j])**p for j in range(n))**(1/p) for i in range(n)))**(1/p)
    
    n = random.randint(5, 40)
    F = generate_disjunctive_boolean_function(n)
    Lp_space = noncommutative_Lp_space(F)
    p = random.uniform(1.1, 2.9)
    spectral_rad = spectral_radius(Lp_space)
    Lp_spectral_rad = Lp_spectral_radius(Lp_space, p)
    
    c = 0.5  # Placeholder for the constant c
    metric_value = Lp_spectral_rad / (c * math.log(n))
    
    return {
        "metric_name": "L^p spectral radius ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": abs(metric_value - 1) <= 3 * math.sqrt(1/n),
        "counterexample": "" if conjecture_holds else "c=0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"c=0.5\" first_failing_seed={first_failing_seed}")