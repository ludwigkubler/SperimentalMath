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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        if A[i][i] == 0:
            return 0
        det *= A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return det

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def fourier_coefficients(circuit, n):
    F = [Fraction(0) for _ in range(2**n)]
    for i in range(2**n):
        sum_val = Fraction(0)
        for k in range(n):
            sum_val += circuit[i] * math.exp(-2j * math.pi * k * i / (2**n))
        F[i] = sum_val
    return F

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = [random.choice([-1, 1]) for _ in range(2**n)]
    
    F = fourier_coefficients(circuit, n)
    norm_F = sum(x * x.conjugate() for x in F).real
    
    if norm_F == 0:
        return {
            "metric_name": "L^2-norm of Fourier coefficients",
            "metric_value": norm_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_all_zeros"
        }
    
    c = Fraction(1, n)
    if norm_F >= c * math.log(n):
        return {
            "metric_name": "L^2-norm of Fourier coefficients",
            "metric_value": norm_F,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "L^2-norm of Fourier coefficients",
            "metric_value": norm_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"norm_F < c * log(n) with n={n}, norm_F={norm_F}, c*log(n)={c*math.log(n)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
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
        print(f"RESULT: FALSIFIED counterexample=\"norm_F < c * log(n)\" first_failing_seed={first_failing_seed}")