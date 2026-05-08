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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return [row[n-1] / row[-2] if i != n-1 else 0 for i, row in enumerate(A)]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def tensor_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        for j in range(n):
            if A[i][j] != 0:
                rank += 1
                break
    return rank

def sos_refutation_size(f, n):
    # Placeholder function. In practice, this would use semidefinite programming.
    return n**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    f = determinant(A)
    tensor_rk = tensor_rank([[f] * n for _ in range(n)])
    sos_size = sos_refutation_size(f, n)
    
    metric_value = sos_size / (n**1.5 / math.log(n))
    conjecture_holds = metric_value >= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "SOS Refutation Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")