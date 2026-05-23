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
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_B)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def matrix_invert(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity)]
        
        for i in range(n):
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                return None
            for j in range(i, n * 2):
                augmented_matrix[i][j] /= pivot
        
            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n * 2):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        
        inverted_matrix = [row[n:] for row in augmented_matrix]
        return inverted_matrix
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
    
    def rank(matrix):
        n, m = len(matrix), len(matrix[0])
        augmented_matrix = [row[:] for row in matrix]
        
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            factor = 1 / augmented_matrix[i][i]
            for j in range(i, m):
                augmented_matrix[i][j] *= factor
            
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, m):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    def monotone_circuit_depth(n):
        # Placeholder function; actual implementation needed
        return n ** (1/4)
    
    n = random.randint(5, 40)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    B = matrix_invert(A)
    if B is None:
        return {
            "metric_name": "monotone_circuit_depth",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "matrix_not_invertible"
        }
    
    rank_A = rank(A)
    depth_A = monotone_circuit_depth(n)
    depth_B = monotone_circuit_depth(n)
    
    c = depth_A / rank_A
    if depth_B > c * rank_B:
        return {
            "metric_name": "monotone_circuit_depth",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"depth_B ({depth_B}) exceeds c * rank_B ({c * rank_B})"
        }
    
    return {
        "metric_name": "monotone_circuit_depth",
        "metric_value": depth_A,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != -1]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth_B exceeds c * rank_B\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")