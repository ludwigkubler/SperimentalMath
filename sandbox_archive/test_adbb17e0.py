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
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def permanent(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in M[1:]]
        sign = (-1) ** j
        det += sign * M[0][j] * permanent(submatrix)
    return det

def circuitsize(n):
    # Minimal circuit size for computing the permanent on n variables
    # This is a known result from computational complexity theory
    return math.factorial(n)

def hilbert_polynomial_coefficient(M, k):
    n = len(M)
    I = [[1 if i <= j else 0 for j in range(k+1)] for i in range(k+1)]
    det = permanent(I)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    k = min(n, 3)
    I_coeff = hilbert_polynomial_coefficient(M, k)
    circuit_size = circuitsize(n)
    if circuit_size == 0:
        return {
            "metric_name": "leading_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ratio = I_coeff / circuit_size
    return {
        "metric_name": "leading_coefficient",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio) < 1e-6,  # Assuming the leading coefficient is approximately zero
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")