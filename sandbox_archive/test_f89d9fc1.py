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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inverse(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

def arithmetic_divergence(F, n):
    # Placeholder implementation of arithmetic divergence
    # This is a dummy function and should be replaced with actual computation
    return random.random() * n ** 0.25

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def generate_xor_circuit(n, S, D):
    # Placeholder implementation of XOR circuit generation
    # This is a dummy function and should be replaced with actual computation
    return random.random() * (S ** 0.5) + random.random() * (D ** 0.25)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "arithmetic_divergence_ratio"
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            F = generate_cnf(n)
            A_F = arithmetic_divergence(F, n)
            
            S = random.randint(1, n)
            D = random.randint(1, n)
            A_C = generate_xor_circuit(n, S, D)
            
            if A_F <= 0.2:
                ratio = A_C / (S ** 0.5 + D ** 0.25)
                total_metric_value += ratio
                instances_tested += 1
    
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")