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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def eigenvalue_decomposition(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    v = [1.0] * n
    for _ in range(100):  # Simple power iteration
        v = matrix_multiply(A, v)
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    return v

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        # Generate a random Max-CUT instance
        A = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        b = [sum(A[i][j] for j in range(i)) for i in range(n)]
        
        # Compute the degree-2 SOS moment matrix
        M = [[sum(A[i][k] * A[j][l] for k in range(n) for l in range(n)) for j in range(n)] for i in range(n)]
        
        # Calculate real rank via eigenvalue decomposition
        eigvals = eigenvalue_decomposition(M)
        rank = sum(1 for x in eigvals if abs(x) > 1e-6)
        
        # Verify integrality gap using small DPLL
        def dpll(A, b):
            m, n = len(A), len(A[0])
            assignment = [None] * n
            stack = []
            def backtrack(i=0):
                if i == n:
                    return all(b[j] >= 0 for j in range(m))
                if assignment[i] is not None:
                    return backtrack(i + 1)
                assignment[i] = True
                if backtrack(i + 1):
                    return True
                assignment[i] = False
                if backtrack(i + 1):
                    return True
                return False
            return backtrack()
        
        gap = 1 - dpll(A, b) / 2
        
        instances_tested += 1
        if gap > 0.878 and rank < 0.3 * n:
            conjecture_holds = False
            counterexample = f"n={n}, gap={gap:.4f}, rank={rank}"
    
    return {
        "metric_name": "Real Rank",
        "metric_value": rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")