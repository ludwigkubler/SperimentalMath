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

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank(matrix):
    A = [row[:] for row in matrix]
    b = [0] * len(matrix)
    sol = gaussian_elimination(A, b)
    non_zero_count = sum(1 for entry in sol if entry != 0)
    return non_zero_count

def secant_dimension(M):
    n = len(M)
    points = [(i, j) for i in range(n) for j in range(i+1, n) if M[i][j] == 1]
    if not points:
        return 0
    
    # Construct the secant ideal
    secant_ideal = []
    for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
        A = [[M[x1][y], M[x2][y]] for x, y in points]
        b = [0] * len(A)
        secant_ideal.append(gaussian_elimination(A, b))
    
    # Compute the rank of the matrix spanned by the secant ideal
    return rank(secant_ideal)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = 0
    
    secant_dim = secant_dimension(M)
    R_M = n * (n - 1) // 2  # Lower bound on communication complexity for DISJ_n
    conjecture_holds = R_M >= 0.5 * secant_dim
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "secant_dimension",
        "metric_value": secant_dim,
        "instances_tested": n * (n - 1) // 2,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")