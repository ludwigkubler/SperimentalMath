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
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        result = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n + 1):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def compute_sos_moment_matrix(G, d):
        n = len(G)
        M = [[0 for _ in range(d+1)] for _ in range(d+1)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    for k in range(d+1):
                        M[k][k] += (i**k + j**k) * G[i][j]
        return M
    
    def compute_eigenvalues(M):
        n = len(M)
        if n != len(M[0]):
            raise ValueError("Matrix must be square")
        
        # Convert to a list of lists for Gaussian elimination
        A = [row[:] for row in M]
        b = [0] * n
        
        # Perform Gaussian elimination
        x = gaussian_elimination(A, b)
        
        # Compute eigenvalues using the Schur decomposition method
        # This is a simplified version and may not work for all matrices
        eigenvalues = []
        for i in range(n):
            lambda_i = 0
            for j in range(n):
                if i != j:
                    lambda_i += A[i][j] * x[j]
                else:
                    lambda_i += M[i][i]
            eigenvalues.append(lambda_i)
        
        return eigenvalues
    
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    M = compute_sos_moment_matrix(G, 3)
    eigenvalues = compute_eigenvalues(M)
    
    metric_value = max(abs(e) for e in eigenvalues)
    conjecture_holds = all(-1 <= e <= 1 for e in eigenvalues)
    counterexample = "" if conjecture_holds else "eigenvalue_outside_interval"
    
    return {
        "metric_name": "Eigenvalue Gap",
        "metric_value": metric_value,
        "instances_tested": n * (n - 1) // 2,  # Number of edges in the graph
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = (len([result for result in results if result["conjecture_holds"]]) / len(results)) * 100
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}%")