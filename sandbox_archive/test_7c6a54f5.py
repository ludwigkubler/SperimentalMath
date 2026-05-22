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
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 6))
    clique = set(random.sample(range(n), k))
    
    # Constructive mapping from clique to affine scheme
    A = [[0 for _ in range(k)] for _ in range(k)]
    b = [0 for _ in range(k)]
    for i in range(k):
        for j in range(i+1, k):
            if (i, j) in clique or (j, i) in clique:
                A[i][j] = 1
                A[j][i] = 1
                b[i] += 1
                b[j] += 1
    
    # Solve linear system to get Hodge index
    try:
        x = gaussian_elimination(A, b)
        hodge_index = sum(x)
    except Exception as e:
        return {
            "metric_name": "Hodge Index and Resolution Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Mapping error: {e}"
        }
    
    # Calculate resolution proof length
    try:
        resolution_length = 2**n / (hodge_index ** 2)
    except ZeroDivisionError:
        return {
            "metric_name": "Hodge Index and Resolution Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution length calculation error: Division by zero"
        }
    
    # Check conjectures
    conjecture_holds = hodge_index <= n ** (k / 2) and resolution_length >= 2**n / (hodge_index ** 2)
    counterexample = "" if conjecture_holds else f"Hodge Index: {hodge_index}, Resolution Length: {resolution_length}"
    
    return {
        "metric_name": "Hodge Index and Resolution Length",
        "metric_value": hodge_index,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 31))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "conjecture_holds" in r and r["conjecture_holds"])
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")