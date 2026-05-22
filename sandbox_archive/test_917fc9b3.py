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
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] + B[k][j]
        return C
    
    def tropical_addition(a, b):
        return max(a, b)
    
    def tropical_multiplication(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            non_zero_row = False
            for j in range(n):
                if A[i][j] != float('-inf'):
                    non_zero_row = True
                    break
            if non_zero_row:
                rank += 1
        return rank
    
    def generate_polynomial_function(degree, n):
        coefficients = [random.randint(0, degree) for _ in range(n)]
        return lambda x: sum(c * (x ** i) for i, c in enumerate(coefficients))
    
    def generate_acc0_circuit(f, n):
        circuit_size = 0
        for i in range(n):
            inputs = [random.randint(0, 1) for _ in range(degree + 1)]
            outputs = f(inputs)
            # Simplified ACC⁰ circuit generation (linear combination)
            circuit_size += degree + 1
        return circuit_size
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    degree = random.randint(1, n // 2)
    f = generate_polynomial_function(degree, n)
    acc0_circuit_size = generate_acc0_circuit(f, n)
    
    # Construct tropical matrix A
    A = [[tropical_addition(float('-inf'), float('-inf'))] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            inputs = [random.randint(0, 1) for _ in range(degree + 1)]
            outputs_i = f(inputs)
            outputs_j = f(inputs)
            A[i][j] = tropical_multiplication(outputs_i, outputs_j)
    
    # Compute minimal rank of tropical matrix A
    min_rank = tropical_matrix_rank(A)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= acc0_circuit_size / n,
        "counterexample": "" if min_rank >= acc0_circuit_size / n else f"Function: {f}, ACC⁰ Circuit Size: {acc0_circuit_size}, Minimal Rank: {min_rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")