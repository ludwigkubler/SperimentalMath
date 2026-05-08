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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k1 = len(A), len(A[0])
    k2, n = len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k1):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(Augmented[i][j]) > abs(Augmented[max_row][j]):
                max_row = i
        Augmented[j], Augmented[max_row] = Augmented[max_row], Augmented[j]
        for i in range(m):
            if i != j:
                factor = Augmented[i][j] / Augmented[j][j]
                for k in range(n+1):
                    Augmented[i][k] -= factor * Augmented[j][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= Augmented[i][j] * x[j]
        x[i] /= Augmented[i][i]
    return x

def det(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = det(submatrix)
        det_val += sign * A[0][c] * sub_det
    return det_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, math.isqrt(n**2))
    
    # Generate permanent and determinant polynomials
    perm_n = [random.randint(-10, 10) for _ in range(math.comb(n, 2))]
    det_m = [random.randint(-10, 10) for _ in range(math.comb(m, 2))]
    
    # Compute Hilbert series (simplified version)
    def hilbert_series(poly, n):
        h = [1]
        for i in range(1, n+1):
            new_h = [0] * (len(h) + i)
            for j in range(len(h)):
                new_h[j+i-1] += h[j] * poly[i-1]
            h = new_h
        return h
    
    perm_series = hilbert_series(perm_n, n)
    det_series = hilbert_series(det_m, m)
    
    # Compare degrees and coefficients
    degree_perm = len(perm_series) - 1
    degree_det = len(det_series) - 1
    if degree_perm > degree_det:
        conjecture_holds = True
        counterexample = ""
    elif degree_perm < degree_det:
        conjecture_holds = False
        counterexample = "Degree of perm_n's Hilbert series is lower than det_m's"
    else:
        for i in range(len(perm_series)):
            if perm_series[i] > det_series[i]:
                conjecture_holds = True
                counterexample = ""
                break
            elif perm_series[i] < det_series[i]:
                conjecture_holds = False
                counterexample = "Coefficients of perm_n's Hilbert series are lower than det_m's"
                break
        else:
            conjecture_holds = True
            counterexample = ""
    
    return {
        "metric_name": "Hilbert Series Degree",
        "metric_value": degree_perm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Degree comparison failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")