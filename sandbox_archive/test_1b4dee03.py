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

def generate_communication_complexity(n):
    # Placeholder for generating communication complexity instances
    return [random.randint(1, n) for _ in range(n)]

def rank_variance(lst):
    mean = sum(lst) / len(lst)
    return sum((x - mean) ** 2 for x in lst) / len(lst)

def minimal_symplectic_quotient_rank(cc_instance):
    # Placeholder for computing minimal symplectic quotient rank
    return sum(cc_instance) % 10

def matrix_mul(A, B, mod=10**9 + 7):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_inv(A, mod=10**9 + 7):
    n = len(A)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for j in range(n):
            A[k][j] *= pow(pivot, mod - 2, mod)
            I[k][j] *= pow(pivot, mod - 2, mod)
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    A[i][j] %= mod
                    I[i][j] -= factor * I[k][j]
                    I[i][j] %= mod
    return I

def polyfit(x, y, degree):
    n = len(x)
    X = [[x[i]**j for j in range(degree + 1)] for i in range(n)]
    Y = [y[i] for i in range(n)]
    A = matrix_mul(X, transpose(X))
    B = matrix_mul(X, Y)
    coefficients = matrix_mul(matrix_inv(A), B)
    return [coeff[0] for coeff in coefficients]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    rv_values = []
    msqr_values = []
    
    for n in n_values:
        cc_instance = generate_communication_complexity(n)
        rv = rank_variance(cc_instance)
        msqr = minimal_symplectic_quotient_rank(cc_instance)
        
        if rv == 0 or msqr == 0:
            continue
        
        rv_values.append(rv)
        msqr_values.append(msqr)
    
    if not rv_values or not msqr_values:
        return {
            "metric_name": "msqr_vs_rv",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    coefficients = polyfit(rv_values, msqr_values, 1)
    slope, intercept = coefficients
    r_squared = sum((msqr - (slope * rv + intercept)) ** 2 for rv, msqr in zip(rv_values, msqr_values))
    r_squared /= sum((msqr - (sum(msqr_values) / len(msqr_values))) ** 2 for msqr in msqr_values)
    
    return {
        "metric_name": "msqr_vs_rv",
        "metric_value": slope,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": r_squared >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")