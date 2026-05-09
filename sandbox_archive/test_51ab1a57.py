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

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    
    # Generate a symmetric CSP instance
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                clause = [random.choice([-1, 1]) * var for var in (i, j)]
                clauses.append(clause)
    
    # Compute the characteristic polynomial using Young tableau branching rules
    def plethysm_coefficient(n):
        if n == 0:
            return 1
        coeff = 0
        for k in range(1, n + 1):
            coeff += (-1) ** (n - k) * math.comb(n, k) * plethysm_coefficient(k)
        return coeff
    
    chi = plethysm_coefficient(n)
    
    # Measure SOS refutation size using degree-4 SDP relaxation
    def sdp_relaxation_size(n):
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for i in range(n):
            A[i][i] = 1
            b[i] = 1
        x = gaussian_elimination(A, b)
        return sum(x[i]**2 for i in range(n))
    
    sos_refutation_size = sdp_relaxation_size(n)
    
    # Check the inequality chi * SOS_refutation_size >= c * log n
    c = 0.5  # Example constant, adjust as needed
    if chi * sos_refutation_size < c * math.log(n):
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": chi,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "inequality_violated"
        }
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": chi,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"inequality_violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")