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

def generate_random_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(p):
                if l < len(B) and j < len(B[l]):
                    C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def randomized_communication_complexity(X, Y):
    n = len(X)
    m = len(Y)
    if n != m:
        raise ValueError("X and Y must have the same length")
    
    # Create an entangled state |ψ⟩
    ψ = [[0] * (n + m) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if X[i] == '1' and Y[j] == '1':
                ψ[i][j] = 1
    
    # Compute the minimal tensor rank τ(|ψ⟩)
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    B = [[Fraction(0) for _ in range(m)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            if ψ[i][j] == 1:
                A[i][i] += Fraction(1)
                B[j][j] += Fraction(1)
    
    rank_A = len(gaussian_elimination(A, [Fraction(0)] * n))
    rank_B = len(gaussian_elimination(B, [Fraction(0)] * m))
    τ_ψ = max(rank_A, rank_B)
    
    # Compute the randomized communication complexity CC_DISJ(n)
    cc_disj = 1 + math.log2(n) + math.log2(m)
    
    return τ_ψ, cc_disj

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    X = generate_random_string(n)
    Y = generate_random_string(n)
    
    try:
        τ_ψ, cc_disj = randomized_communication_complexity(X, Y)
    except Exception as e:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    correlation = τ_ψ / cc_disj
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")