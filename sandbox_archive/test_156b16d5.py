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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_invertible(A):
        m, n = len(A), len(A[0])
        if m != n:
            return False
        det = 1
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
        return det != 0
    
    def generate_random_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def count_monoids(A):
        m, n = len(A), len(A[0])
        monoids = set()
        for i in range(m):
            for j in range(n):
                if A[i][j] == 1:
                    submatrix = [row[j:] for row in A[i:]]
                    if is_invertible(submatrix):
                        monoids.add(tuple(map(tuple, submatrix)))
        return len(monoids)
    
    def calculate_representation_error(A, B):
        m, n = len(A), len(A[0])
        error = 0
        for i in range(m):
            for j in range(n):
                error += abs(A[i][j] - B[i][j])
        return error
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        A = generate_random_matrix(n)
        B = gaussian_elimination(A.copy())
        C = matrix_multiply(A, B)
        
        num_monoids = count_monoids(A)
        error = calculate_representation_error(A, C)
        
        results.append({
            "n": n,
            "num_monoids": num_monoids,
            "error": error
        })
    
    max_n = max(result["n"] for result in results)
    avg_num_monoids = sum(result["num_monoids"] for result in results) / len(results)
    avg_error = sum(result["error"] for result in results) / len(results)
    
    conjecture_holds = all(num_monoids <= math.log2(n)**2 and error <= 0.1 * n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "num_monoids",
        "metric_value": avg_num_monoids,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")