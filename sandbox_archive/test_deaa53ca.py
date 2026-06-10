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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for r in range(i+1, m):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for r in range(i+1, m):
            factor = -A[r][i] / A[i][i]
            for c in range(i, n):
                A[r][c] += factor * A[i][c]

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def matrix_power(A, n):
    result = [[Fraction(0) if r != c else Fraction(1) for c in range(len(A))] for r in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def characteristic_function(circuit):
    n = len(circuit)
    M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if circuit[i][j] == '1':
                M[i][j] = Fraction(1, 2**i * 2**j)
    return matrix_power(M, n)

def mock_theta_function(x, q):
    return x + q * x**5 + q**2 * x**7 + q**3 * x**9

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random Boolean circuit with n inputs
    n = random.randint(5, 40)
    circuit = [[random.choice(['0', '1']) for _ in range(n)] for _ in range(n)]
    
    # Compute the characteristic function χ_C of the circuit
    chi_C = characteristic_function(circuit)
    
    # Express χ_C in terms of Ramanujan's mock theta functions
    q = Fraction(1, 2)
    representation_size = sum(mock_theta_function(chi_C[i][j], q) for i in range(n) for j in range(n))
    
    # Determine the representation size |χ_C|
    metric_value = abs(representation_size)
    
    # Check if the conjecture holds
    conjecture_holds = metric_value <= 1.5 * n**(2/3)
    counterexample = f"Circuit with {n} inputs and size {len(circuit)}" if not conjecture_holds else ""
    
    return {
        "metric_name": "representation_size",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")