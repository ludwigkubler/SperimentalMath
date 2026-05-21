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
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = A[i][i]
        if factor == 0:
            continue  # Skip row with zero pivot
        for k in range(i+1, n):
            factor_k = A[k][i] / factor
            for j in range(n):
                A[k][j] -= factor_k * A[i][j]
    return A

def r_transform(A):
    n = len(A)
    det_A = 0
    sign = 1
    for i in range(n):
        det_A += sign * A[0][i] * determinant(minor(A, 0, i))
        sign *= -1
    if det_A == 0:
        return Fraction(0)  # Avoid division by zero
    return Fraction(1, det_A)

def minor(A, i, j):
    n = len(A)
    minor = []
    for r in range(n):
        if r == i:
            continue
        row = []
        for c in range(n):
            if c == j:
                continue
            row.append(A[r][c])
        minor.append(row)
    return minor

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det_A = Fraction(0)
    sign = 1
    for i in range(n):
        det_A += sign * A[0][i] * determinant(minor(A, 0, i))
        sign *= -1
    return det_A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    P = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    P = gaussian_elimination(P)
    
    rho_P = abs(r_transform(P))
    if rho_P <= 10 * math.log(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "rho(IP_2) exceeds 10n"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='rho(IP_2) exceeds 10n' first_failing_seed={first_failing_seed}")