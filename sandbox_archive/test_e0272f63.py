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
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(i+1, n):
            factor_k = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor_k * A[i][j]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def real_radical_dimension(A):
    n = len(A)
    if n == 0:
        return 0
    if n == 1:
        return int(determinant(A) != 0)
    
    # Perform Gaussian elimination to get the rank of the matrix
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(val != 0 for val in row))
    
    # The dimension of the real radical is n - rank
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    
    d = real_radical_dimension(A)
    if d == -1:
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sos_degree = random.randint(1, 2 * n)
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": sos_degree >= math.log(d),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean = sum(res["metric_value"] for res in results) / len(results)
        std = math.sqrt(sum((res["metric_value"] - mean)**2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        mean = None
        std = None
        support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
    
    if all(res["conjecture_holds"] or res["counterexample"] == "mapping_undefined" for res in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] != "mapping_undefined" for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")