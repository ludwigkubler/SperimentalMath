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

def matrix_mul(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_det(A):
    if len(A) == 1:
        return A[0][0]
    det_A = 0
    for j in range(len(A)):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_A += (-1) ** j * A[0][j] * matrix_det(submatrix)
    return det_A

def char_poly(A):
    n = len(A)
    if n == 1:
        return [-A[0], 1]
    det_A = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_A += (-1) ** j * A[0][j] * char_poly(submatrix)[0]
    return [det_A, -sum(A[i][i] for i in range(n))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    D = [[random.random() for _ in range(n)] for _ in range(n)]
    C = char_poly(D)
    det_C = matrix_det(C)
    rho_D = len(C)
    
    if det_C != matrix_det(D):
        return {
            "metric_name": "Minimal Rank of Delone Set Complexity vs Permutation Circuit Depth",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "det(C) != det(D)"
        }
    
    return {
        "metric_name": "Minimal Rank of Delone Set Complexity vs Permutation Circuit Depth",
        "metric_value": rho_D,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"det(C) != det(D)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")