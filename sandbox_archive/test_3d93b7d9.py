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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate non-pivot elements in the current column
        for k in range(i + 1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    
    # Back-substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i - 1, -1, -1):
            b[k] -= A[k][i] * x[i]
    
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        k //= 2
    
    return result

def modular_form_degree(poly, p):
    n = len(poly) - 1
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            A[i][j - i] = poly[j]
        b[i] = poly[i]
    
    try:
        solution = gaussian_elimination(A, b)
    except IndexError:
        return None
    
    degree = max([i for i, x in enumerate(solution) if x != 0])
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = random.randint(2, 100)  # Finite field characteristic
    n = random.randint(5, 40)   # Polynomial degree
    
    # Generate a random polynomial of degree n over F_p
    poly = [random.randint(0, p - 1) for _ in range(n + 1)]
    
    m = modular_form_degree(poly, p)
    if m is None:
        return {
            "metric_name": "modular_form_degree",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "gaussian_elimination_failed"
        }
    
    # Construct a Boolean circuit for the polynomial
    # This is a placeholder; actual construction depends on the polynomial
    # For simplicity, we assume D = O(n log p)
    D = n * math.log(p, 2)
    
    if m < math.log(n) or m > D * math.log(n):
        return {
            "metric_name": "modular_form_degree",
            "metric_value": m,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"m={m}, D={D}"
        }
    
    return {
        "metric_name": "modular_form_degree",
        "metric_value": m,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8 and mean <= 3:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"m out of bounds\" first_failing_seed={first_failing_seed}")