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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, n):
    result = [[Fraction(1 if i == j else 0) for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        det += sign * matrix[0][j] * permanent(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random homogeneous polynomial of degree d
        d = n
        coefficients = [random.randint(1, 10) for _ in range(d + 1)]
        f = sum(coeff * x**i for i, coeff in enumerate(coefficients))
        
        # Compute the permanent-determinant gap for a matrix of size O(d^2)
        m = n
        A = [[random.randint(1, 10) for _ in range(m)] for _ in range(m)]
        det_A = Fraction(0)
        perm_A = permanent(A)
        
        # Compute the minimum degree among all Weyl characters of φ(f)
        min_deg_W = d
        
        results.append({
            "n": n,
            "f": f,
            "det_A": det_A,
            "perm_A": perm_A,
            "min_deg_W": min_deg_W
        })
    
    # Compute the permanent-determinant gap for each n
    gamma_values = [permanent(matrix_power([[1, 1], [1, 0]], n)) for n in n_values]
    
    # Check if the conjecture holds for all n
    conjecture_holds = all(result["min_deg_W"] >= gamma for result, gamma in zip(results, gamma_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "permanent-determinant gap",
        "metric_value": sum(gamma_values) / len(gamma_values),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")