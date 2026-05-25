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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = Fraction(0)
    sign = Fraction(1, 1)
    for j in range(len(A)):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * matrix_determinant(submatrix)
        sign *= -Fraction(1, 1)
    return det

def char_poly(D):
    n = len(D)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            A[i][j] = D[i][j]
    A[n][n-1] = -sum(A[i][i] for i in range(n))
    A[n][n] = 1
    det_A = matrix_determinant(A)
    return [det_A]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    D = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    det_D = matrix_determinant(D)
    char_poly_D = char_poly(D)
    min_rank = len(D)
    min_depth = float('inf')
    
    for i in range(100):
        C = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        det_C = matrix_determinant(C)
        if det_C == det_D:
            depth = 0
            while True:
                depth += 1
                C_new = []
                for j in range(n):
                    row = [C[i][j] for i in range(n) if i != j]
                    C_new.append(row)
                det_C = matrix_determinant(C_new)
                if det_C == det_D:
                    break
            min_depth = min(min_depth, depth)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 100,
        "conjecture_holds": min_rank <= min_depth,
        "counterexample": "" if min_rank <= min_depth else f"Det(D)={det_D}, Det(C)={det_C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Det(D) != Det(C)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")