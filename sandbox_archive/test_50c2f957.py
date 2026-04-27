# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return A

def submatrix(matrix, rows, cols):
    return [[matrix[r][c] for c in cols] for r in rows]

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(len(A)):
        submat = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submat)
        sign *= -1
    return det

def subdeterminant_dispersion(M):
    n = len(M)
    k_values = [2, 3]
    max_det_ratio = 0
    for k in k_values:
        for S in itertools.combinations(range(n), k):
            for T in itertools.combinations(range(n), k):
                submat = submatrix(M, S, T)
                det_val = abs(determinant(gaussian_elimination(submat)))
                max_det_ratio = max(max_det_ratio, det_val ** (1/k) / math.sqrt(k))
    return max_det_ratio

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 20]
    results = []
    
    for n in n_values:
        for _ in range(30):
            M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            delta = subdeterminant_dispersion(M)
            U, s, Vt = map(list, zip(*map(list, zip(*M))))
            tau = sum(s_i**2 >= (sum(x**2 for x in itertools.chain.from_iterable(M)) / n) for s_i in s)
            R = tau * delta**2 / n
            results.append(R)
    
    min_R = min(results)
    median_R = sorted(results)[len(results) // 2]
    
    conjecture_holds = min_R >= 0.25 and all(sorted(results)[i] <= sorted(results)[i+1] for i in range(len(results)-1))
    counterexample = "" if conjecture_holds else f"min R={min_R}, median R={median_R}"
    
    return {
        "metric_name": "R(M)",
        "metric_value": min_R,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    min_Rs = [run_trial(seed)["metric_value"] for seed in seeds]
    median_Rs = sorted(min_Rs)[len(min_Rs) // 2]
    support_fraction = sum(1 for r in min_Rs if r >= 0.25) / len(min_Rs)
    
    if all(r >= 0.25 for r in min_Rs):
        print(f"RESULT: SUPPORTED mean={sum(min_Rs)/len(min_Rs)} std={math.sqrt(sum((r - sum(min_Rs)/len(min_Rs))**2 for r in min_Rs) / len(min_Rs))} support_fraction={support_fraction}")
    elif any(r < 0.25 for r in min_Rs):
        first_failing_seed = next(i for i, r in enumerate(min_Rs) if r < 0.25)
        print(f"RESULT: FALSIFIED counterexample='min R={min_Rs[first_failing_seed]}, median R={median_Rs}' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")