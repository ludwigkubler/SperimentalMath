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
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, p):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_multiply(result, M)
        M = matrix_multiply(M, M)
        p //= 2
    return result

def determinant(matrix):
    n = len(matrix)
    det = 0
    if n == 1:
        return matrix[0][0]
    for j in range(n):
        submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
    return det

def orbit_closure_dimension(n):
    if n == 2:
        return 3
    elif n == 3:
        return 9
    else:
        return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    det_dim = orbit_closure_dimension(n)
    perm_dim = 2 ** (n * (n - 1)) // 2
    if det_dim is None or perm_dim is None:
        return {
            "metric_name": "orbit_closure_dimension",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    return {
        "metric_name": "orbit_closure_dimension",
        "metric_value": det_dim < perm_dim,
        "instances_tested": 1,
        "conjecture_holds": det_dim < perm_dim,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(results):
        support_fraction = len([r for r in results if r]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results)} std={math.sqrt(sum((x - sum(results) / len(results)) ** 2 for x in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if not r))]
        print(f"RESULT: FALSIFIED counterexample=\"orbit_closure_dimension\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")