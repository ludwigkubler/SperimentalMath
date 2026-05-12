# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
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
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def transition_matrix(P, n):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if P[i][j]:
                M[i][j] = 1
    return M

def moment_cumulant_formula(M):
    n = len(M)
    det_M = determinant(M)
    log_det_M = math.log(abs(det_M)) if det_M != 0 else -math.inf
    return log_det_M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    T = transition_matrix(P, n)
    kappa_sum = moment_cumulant_formula(T)
    
    if kappa_sum == -math.inf:
        return {
            "metric_name": "kappa_sum",
            "metric_value": kappa_sum,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    size_P = n**n
    log_size_P = math.log(size_P)
    
    return {
        "metric_name": "kappa_sum",
        "metric_value": kappa_sum,
        "instances_tested": 1,
        "conjecture_holds": kappa_sum <= log_size_P + 1 and kappa_sum == O(1),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    kappa_sums = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(kappa_sums) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(kappa_sums)/len(kappa_sums):.2f} std={math.sqrt(sum((x - sum(kappa_sums)/len(kappa_sums))**2 for x in kappa_sums) / len(kappa_sums)):.2f} support_fraction={support_fraction:.2f}"
    else:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}"
    
    print(RESULT)