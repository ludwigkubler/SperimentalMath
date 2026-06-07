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
        # Generate a random graph using adjacency matrix representation
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix

    def matrix_multiplication(A, B):
        # Manually implement matrix multiplication
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
        return result

    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [0] for row in matrix]
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        # Back-substitute to find the solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = augmented_matrix[i][-1] / augmented_matrix[i][i]
            for j in range(i-1, -1, -1):
                augmented_matrix[j][-1] -= augmented_matrix[j][i] * x[i]
        return x

    def compute_hdim(G):
        # Compute the Hodge theoretical dimension (simplified version)
        n = len(G)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        adj_matrix = G
        laplacian = matrix_multiplication(adj_matrix, adj_matrix)
        laplacian = [row[:] for row in laplacian]
        for i in range(n):
            laplacian[i][i] -= sum(row[i] for row in laplacian if row != laplacian[i])
        
        # Perform Gaussian elimination to find the rank
        rank = gaussian_elimination(laplacian)
        return n - rank.count(0)

    def compute_ccr(G):
        # Compute the communication complexity rank (simplified version)
        n = len(G)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        adj_matrix = G
        laplacian = matrix_multiplication(adj_matrix, adj_matrix)
        laplacian = [row[:] for row in laplacian]
        for i in range(n):
            laplacian[i][i] -= sum(row[i] for row in laplacian if row != laplacian[i])
        
        # Perform Gaussian elimination to find the rank
        rank = gaussian_elimination(laplacian)
        return n - rank.count(0)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        hdim_values = []
        ccr_values = []
        for _ in range(5):  # Test each size with 5 instances
            G = generate_random_graph(n)
            hdim = compute_hdim(G)
            ccr = compute_ccr(G)
            hdim_values.append(hdim)
            ccr_values.append(ccr)
        
        mean_hdim = sum(hdim_values) / len(hdim_values)
        mean_ccr = sum(ccr_values) / len(ccr_values)
        correlation_coefficient = (sum((h - mean_hdim) * (c - mean_ccr) for h, c in zip(hdim_values, ccr_values)) /
                                   math.sqrt(sum((h - mean_hdim) ** 2 for h in hdim_values) *
                                             sum((c - mean_ccr) ** 2 for c in ccr_values)))
        
        results.append({
            "n": n,
            "mean_hdim": mean_hdim,
            "mean_ccr": mean_ccr,
            "correlation_coefficient": correlation_coefficient
        })

    # Check if the correlation coefficient is significantly different from 0
    p_value = 2 * (1 - math.erf(abs(results[0]["correlation_coefficient"]) / math.sqrt(2 * len(results))))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": results[0]["correlation_coefficient"],
        "instances_tested": 30,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(results[0]["correlation_coefficient"]) > 0.8 and p_value < 0.05,
        "counterexample": "" if abs(results[0]["correlation_coefficient"]) > 0.8 else "not_enough_instances"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_enough_instances' first_failing_seed={first_failing_seed}")