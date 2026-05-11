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

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** i
        det += sign * A[0][i] * determinant(submatrix)
    return det

def transition_matrix(bp, n):
    P = [[0] * n for _ in range(n)]
    for state in bp:
        if len(state) == 2 and state[0] != state[1]:
            i, j = state
            P[i][j] += 1
    return P

def free_cumulant(P):
    n = len(P)
    det_P = determinant(P)
    if det_P == 0:
        return float('inf')
    P_inv = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in P[:i] + P[i+1:]]
            P_inv[i][j] = (-1) ** (i+j) * determinant(minor) / det_P
    return sum(P_inv[i][i] for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    trivial_bp = [(i, i+1) for i in range(n-1)]
    other_bps = []
    for _ in range(29):
        bp = []
        while len(bp) < n:
            state = (random.randint(0, n-1), random.randint(0, n-1))
            if state not in bp and state[0] != state[1]:
                bp.append(state)
        other_bps.append(bp)
    
    trivial_cumulant = free_cumulant(transition_matrix(trivial_bp, n))
    other_cumuulants = [free_cumulant(transition_matrix(bp, n)) for bp in other_bps]
    
    metric_name = "Free Cumulant Gap"
    metric_value = max(other_cumuulants) - trivial_cumulant
    instances_tested = 30
    conjecture_holds = all(cumulant < n/2 for cumulant in other_cumuulants)
    counterexample = "" if conjecture_holds else "trivial BP should have larger cumulant"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
        print(f"RESULT: FALSIFIED counterexample=\"trivial BP should have larger cumulant\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")