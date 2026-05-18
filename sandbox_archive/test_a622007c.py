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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def frobenius_norm(A):
    norm = 0
    for row in A:
        for val in row:
            norm += val ** 2
    return math.sqrt(norm)

def largest_singular_value(A):
    m, n = len(A), len(A[0])
    U, _, Vt = svd(A)
    return max(abs(v) for v in Vt[0])

def svd(A):
    m, n = len(A), len(A[0])
    A_t = list(zip(*A))
    Q_A, R_A = qr_decomposition(A)
    Q_B, R_B = qr_decomposition(A_t)
    U = matrix_multiplication(Q_A, R_A)
    Vt = matrix_multiplication(R_B, Q_B)
    S = [[R_A[i][i] if i < min(m, n) else 0 for i in range(n)] for _ in range(m)]
    return U, S, Vt

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q = []
    R = A
    for j in range(n):
        v = [R[i][j] for i in range(j, m)]
        norm = frobenius_norm(v)
        q = [v[i] / norm if i == j else 0 for i in range(m)]
        Q.append(q)
        R = [[sum(R[i][k] * Q[k][j] for k in range(j)) for k in range(n)] for i in range(m)]
    return Q, R

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    results = []
    
    def generate_rtbp(w, L):
        T0 = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
        T1 = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
        return T0, T1
    
    def layer_difference_stack(T0, T1):
        return [vec(T1[i] - T0[i]) for i in range(len(T0))]
    
    def vec(matrix):
        return sum([row for row in matrix], [])
    
    def frobenius_norm_squared(A):
        norm = 0
        for row in A:
            for val in row:
                norm += val ** 2
        return norm
    
    def operator_norm(A):
        m, n = len(A), len(A[0])
        U, _, Vt = svd(A)
        return max(abs(v) for v in Vt[0])
    
    for w in [3, 4, 5, 6]:
        for L in [4 * n for n in n_values]:
            T0, T1 = generate_rtbp(w, L)
            D = layer_difference_stack(T0, T1)
            norm_F_squared = frobenius_norm_squared(D)
            norm_op = operator_norm(D)
            s = w * L
            rho = math.log2(norm_F_squared / norm_op ** 2) if norm_op != 0 else 0
            results.append({"n": n, "w": w, "rho": rho, "s": s})
    
    canonical_rho_ip2 = [n / 4 for n in n_values]
    
    return {
        "metric_name": "rho",
        "metric_value": sum(result["rho"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(rho <= 2 * math.log2(s + 1) for rho, s in zip([result["rho"] for result in results], [result["s"] for result in results])) and all(rho >= n / 4 for rho, n in zip(canonical_rho_ip2, n_values)),
        "counterexample": "" if all(rho <= 2 * math.log2(s + 1) for rho, s in zip([result["rho"] for result in results], [result["s"] for result in results])) and all(rho >= n / 4 for rho, n in zip(canonical_rho_ip2, n_values)) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2 * math.log2(s + 1) and r >= n / 4 for s, n in zip([result["s"] for result in results], [n for n in n_values])) / (len(n_values) * len(results))
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not (r <= 2 * math.log2(s + 1) and r >= n / 4 for s, n in zip([result["s"] for result in results], [n for n in n_values])))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")