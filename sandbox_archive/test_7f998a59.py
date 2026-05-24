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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def free_entropy(graph):
        n = len(graph)
        laplacian = [[0]*n for _ in range(n)]
        for i in range(n):
            degree = sum(graph[i])
            laplacian[i][i] = degree
            for j in range(i+1, n):
                if graph[i][j]:
                    laplacian[i][j] = -1
                    laplacian[j][i] = -1
        
        eigenvalues = []
        for _ in range(10):  # Power iteration method to find the largest eigenvalue
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x**2 for x in v))
            for _ in range(10):
                v = matrix_multiply(laplacian, v)
                v /= math.sqrt(sum(x**2 for x in v))
            eigenvalues.append(v[0])
        
        return -sum(math.log(eigenvalue) for eigenvalue in eigenvalues if eigenvalue > 0)
    
    def tensor_width(bp):
        # Placeholder function to calculate the tensor width
        # This is a dummy implementation and should be replaced with actual logic
        return len(bp)
    
    n = random.randint(5, 40)
    bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = construct_graph(bp)
    
    F_G = free_entropy(G)
    DTW_BP = tensor_width(bp)
    
    if DTW_BP == 0:
        return {
            "metric_name": "F(G)/DTW(BP)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tensor_width_is_zero"
        }
    
    ratio = F_G / DTW_BP
    
    return {
        "metric_name": "F(G)/DTW(BP)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= f(n),
        "counterexample": ""
    }

def construct_graph(bp):
    n = len(bp)
    G = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if bp[i][j]:
                G[i][j] = 1
                G[j][i] = 1
    return G

def f(n):
    # Placeholder function to define the lower bound f(n)
    # This is a dummy implementation and should be replaced with actual logic
    return n / 2

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(result["metric_value"] for result in results if "metric_value" in result)
    mean_ratio = total_ratio / len(results) if results else 0
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results if "metric_value" in result)) / len(results) if results else 0
    
    support_fraction = sum(1 for result in results if "conjecture_holds" and result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n) is too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")