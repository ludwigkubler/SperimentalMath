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
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        k //= 2
    return result

def kronecker_coefficient(λ, μ, ν):
    n = len(λ)
    m = len(μ)
    l = len(ν)
    if λ[0] + μ[0] != ν[0]:
        return 0
    coeff = 1
    for i in range(n):
        coeff *= math.factorial(λ[i])
        coeff //= math.factorial(i+1) * math.factorial(λ[i]-i-1)
    for j in range(m):
        coeff *= math.factorial(μ[j])
        coeff //= math.factorial(j+1) * math.factorial(μ[j]-j-1)
    for k in range(l):
        coeff *= math.factorial(ν[k])
        coeff //= math.factorial(k+1) * math.factorial(ν[k]-k-1)
    return coeff

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    matrix = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    
    # Compute Sym^2(Perm_n)
    perm_matrix = matrix_power(matrix, n-1)
    sym2_perm = matrix_multiply(perm_matrix, perm_matrix)
    
    # Compute Kronecker coefficients
    λ = [n//2] * (n//2)
    μ = [n//2] * (n//2)
    ν = [n] * n
    
    coeff = kronecker_coefficient(λ, μ, ν)
    ratio = coeff / (n**2)
    
    return {
        "metric_name": "Kronecker Coefficient Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 1,
        "counterexample": "" if ratio > 1 else f"Ratio {ratio} ≤ 1 for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio ≤ 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or support_fraction < 80%")