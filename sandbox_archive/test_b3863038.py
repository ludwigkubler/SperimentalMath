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
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
        return G
    
    def degree(G, v):
        return sum(G[v][u] for u in range(len(G)))
    
    def communication_complexity_rank(G):
        return min(degree(G, v) for v in range(len(G)))
    
    def adjacency_matrix_to_laplacian(A):
        n = len(A)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            row_sum = sum(A[i][j] for j in range(n))
            D[i][i] = row_sum
        L = [[D[i][j] - A[i][j] if i == j else -A[i][j] for j in range(n)] for i in range(n)]
        return L
    
    def normalize_matrix(M):
        n = len(M)
        sum_elements = sum(sum(row) for row in M)
        return [[M[i][j] / sum_elements for j in range(n)] for i in range(n)]
    
    def smallest_non_zero_eigenvalue(L_norm):
        n = len(L_norm)
        if n == 0:
            return 0
        eigenvalues = []
        A = L_norm[:]
        while A:
            v = [A[i][i] for i in range(n)]
            norm_v = sum(v[i] * v[i] for i in range(n)) ** 0.5
            if norm_v == 0:
                break
            q = [v[i] / norm_v for i in range(n)]
            A = [[A[i][j] - q[i] * q[j] for j in range(n)] for i in range(n)]
            eigenvalues.append(norm_v)
        return min(eigenvalues) if eigenvalues else 0
    
    def qr_decomposition(A):
        n = len(A)
        Q = [[Fraction(0, 1)] * n for _ in range(n)]
        R = [[Fraction(0, 1)] * n for _ in range(n)]
        for k in range(n):
            v = [A[k][i] for i in range(k, n)]
            norm_v = sum(v[i] * v[i] for i in range(len(v))) ** 0.5
            Q[k][k] = Fraction(norm_v).limit_denominator()
            R[0][k] = A[k][k]
            for j in range(k + 1, n):
                q = [Q[j][i] / Q[k][k] for i in range(k, n)]
                R[j][k] = sum(q[i] * v[i] for i in range(len(v)))
                for i in range(k, n):
                    A[j][i] -= q[i] * v[i]
        return Q, R
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
        return C
    
    def transpose_matrix(M):
        n = len(M)
        M_t = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M_t[j][i] = M[i][j]
        return M_t
    
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = Fraction(0, 1)
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def inverse_matrix(M):
        n = len(M)
        det_M = determinant(M)
        if det_M == 0:
            raise ValueError("Matrix is singular and does not have an inverse.")
        cofactors = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
                cofactors[i][j] = (-1) ** (i + j) * determinant(submatrix)
        adjugate = transpose_matrix(cofactors)
        inv_M = [[adjugate[i][j] / det_M for j in range(n)] for i in range(n)]
        return inv_M
    
    def solve_linear_system(A, b):
        n = len(A)
        A_augmented = [A[i] + [b[i]] for i in range(n)]
        Q, R = qr_decomposition(A_augmented)
        x = [Fraction(0, 1)] * n
        for j in range(n - 1, -1, -1):
            x[j] = (Q[n-1][j] - sum(Q[i][j] * x[i] for i in range(j + 1, n))) / R[j][j]
        return x
    
    def generate_random_communication_complexity_function(n):
        G = generate_random_graph(n)
        r_f = communication_complexity_rank(G)
        f = [random.randint(0, 1) for _ in range(r_f)]
        return G, f
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G, f = generate_random_communication_complexity_function(n)
        L_norm = normalize_matrix(adjacency_matrix_to_laplacian(G))
        lambda_min = smallest_non_zero_eigenvalue(L_norm)
        r_f = communication_complexity_rank(G)
        
        if lambda_min == 0 or n == 1:
            continue
        
        ratio = lambda_min / n
        results.append({
            "n": n,
            "lambda_min": lambda_min,
            "r_f": r_f,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["ratio"] >= 0.5 * math.log(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else "lambda_min/n < 0.5 * log(n)"
    
    return {
        "metric_name": "Ratio of smallest non-zero eigenvalue to n",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lambda_min/n < 0.5 * log(n)\" first_failing_seed={first_failing_seed}")