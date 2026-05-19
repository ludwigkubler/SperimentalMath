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
    
    def construct_sos_moment_matrix(vertices, edges, d):
        n = len(vertices)
        M_d = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Add constant term
        M_d[0][0] = 1
        
        # Add terms for each vertex
        for i, v in enumerate(vertices):
            M_d[i + 1][i + 1] = 1
        
        # Add terms for each edge
        for u, v in edges:
            M_d[u + 1][v + 1] += 1
            M_d[v + 1][u + 1] += 1
        
        return M_d
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
        
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            # Swap rows
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            # Eliminate below pivot
            for j in range(i + 1, n):
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        # Back-substitute
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = augmented_matrix[i][-1]
            for j in range(i + 1, n):
                x[i] -= augmented_matrix[i][j] * x[j]
            x[i] /= augmented_matrix[i][i]
        
        return x
    
    def compute_eigenvalues(matrix):
        n = len(matrix)
        identity = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        
        # Compute characteristic polynomial
        det = 0
        for sign in [1, -1]:
            for p in itertools.permutations(range(n)):
                term = sign * math.prod(matrix[i][p[i]] for i in range(n))
                det += term
        
        # Find eigenvalues using numerical methods (e.g., QR algorithm)
        A = [[Fraction(a) for a in row] for row in matrix]
        Q, R = [], []
        for _ in range(100):  # Maximum iterations
            Q, R = gaussian_elimination(A, [0] * n), gaussian_elimination(A, [0] * n)
            A = [[R[i][j] for j in range(n)] for i in range(n)]
        
        eigenvalues = [A[i][i] for i in range(n)]
        return eigenvalues
    
    def max_cut_instance(n):
        vertices = list(range(n))
        edges = []
        for _ in range(int(n * (n - 1) / 4)):
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def sos_approximation_ratio(M_d):
        n = len(M_d) - 1
        eigenvalues = compute_eigenvalues(M_d)
        max_eigenvalue = max(eigenvalues)
        sum_of_squares = sum(eigenvalue ** 2 for eigenvalue in eigenvalues)
        return max_eigenvalue / math.sqrt(sum_of_squares)
    
    def real_rank(matrix):
        n = len(matrix)
        identity = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        
        # Compute rank using Gaussian elimination
        A = [row + [1] for row in matrix]
        Q, R = [], []
        for _ in range(100):  # Maximum iterations
            Q, R = gaussian_elimination(A, [0] * (n + 1)), gaussian_elimination(A, [0] * (n + 1))
            A = [[R[i][j] for j in range(n + 1)] for i in range(n)]
        
        rank = sum(1 for row in R if any(row[j] != Fraction(0) for j in range(n)))
        return rank
    
    n = random.randint(5, 40)
    vertices, edges = max_cut_instance(n)
    d = random.randint(2, 4)
    
    M_d = construct_sos_moment_matrix(vertices, edges, d)
    rank_M_d = real_rank(M_d)
    sos_ratio = sos_approximation_ratio(M_d)
    
    metric_value = rank_M_d
    instances_tested = 1
    conjecture_holds = rank_M_d >= 0.8 * d ** 2
    counterexample = "" if conjecture_holds else f"rank(M_{d})={rank_M_d}, expected ≥{0.8 * d ** 2}"
    
    return {
        "metric_name": "real_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(seed) for seed in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")