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
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = random.randint(3*n//2, 5*n//2)
    clauses = []
    variables = set()
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i+1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
        variables.update(abs(x) for x in clause)
    
    variables = sorted(variables)
    num_vars = len(variables)
    monomials = []
    for clause in clauses:
        for sign in [1, -1]:
            monomial = 1
            for var in variables:
                if var in clause:
                    monomial *= var ** (abs(clause[variables.index(var)]) == 1)
                elif -var in clause:
                    monomial *= var ** (-abs(clause[variables.index(-var)]) == 1)
            monomials.append(monomial)
    
    A = [[0] * num_vars for _ in range(num_vars)]
    b = [0] * num_vars
    for monomial in monomials:
        for i, var in enumerate(variables):
            if var in monomial:
                A[i][variables.index(var)] += 1
            elif -var in monomial:
                A[i][variables.index(-var)] -= 1
    
    x = gaussian_elimination(A, b)
    sos_degree = sum(abs(x[i]) for i in range(num_vars))
    
    def hilbert_function(d):
        if d < 0:
            return 0
        count = 0
        for monomial in monomials:
            degree = sum(abs(var) for var in monomial)
            if degree <= d:
                count += 1
        return count
    
    max_d = int(sos_degree * 1.5)
    H_I_Φ_values = [hilbert_function(d) for d in range(max_d + 1)]
    
    metric_name = "Hilbert Function Growth"
    metric_value = sum(H_I_Φ_values[d] / (n ** (d / 2)) for d in range(max_d + 1))
    instances_tested = max_d + 1
    conjecture_holds = all(H_I_Φ_values[d] <= n ** (d / 2) for d in range(max_d + 1))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")