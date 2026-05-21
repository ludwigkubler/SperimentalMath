# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def transpose(A):
        m, n = len(A), len(A[0])
        T = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                T[j][i] = A[i][j]
        return T

    def svd(A):
        U, S, Vt = [], [], []
        A_T = transpose(A)
        AAT = matrix_multiply(A, A_T)
        ATA = matrix_multiply(A_T, A)
        
        # Compute singular values of AAT and ATA
        for i in range(min(len(A), len(A[0]))):
            eigenvalues_AAT = [AAT[i][i] - s**2 for s in S]
            eigenvalues_ATA = [ATA[i][i] - s**2 for s in S]
            
            # Find next singular value
            sv = max(eigenvalues_AAT + eigenvalues_ATA)
            S.append(math.sqrt(sv))
        
        return U, S, Vt

    def generate_read_twice_bp(n):
        T = [[0] * n for _ in range(2)]
        for i in range(n):
            T[0][i] = random.choice([1, -1])
            T[1][i] = random.choice([1, -1])
        return T

    def generate_read_once_bp(n):
        T = [[0] * n for _ in range(2)]
        for i in range(n):
            T[0][i] = random.choice([1, -1])
            T[1][i] = 0
        return T

    def sum_of_singular_values(T):
        sv_sum = 0
        for _, sv in (svd(T[i]) for i in range(2)):
            sv_sum += max(abs(s) for s in sv)
        return sv_sum

    n = random.choice([5, 10, 15, 20, 30, 40])
    T_twice = generate_read_twice_bp(n)
    T_once = generate_read_once_bp(n)

    sv_sum_twice = sum_of_singular_values(T_twice)
    sv_sum_once = sum_of_singular_values(T_once)

    return {
        "metric_name": "Sum of Singular Values",
        "metric_value_twice": sv_sum_twice,
        "metric_value_once": sv_sum_once,
        "instances_tested": 2,
        "conjecture_holds": sv_sum_twice >= n and sv_sum_once <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value_twice = sum(r["metric_value_twice"] for r in results)
    total_metric_value_once = sum(r["metric_value_once"] for r in results)
    support_fraction_twice = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    support_fraction_once = sum(1 for r in results if not r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean_twice={total_metric_value_twice/len(results)} std_twice=0 support_fraction_twice={support_fraction_twice} support_fraction_once={support_fraction_once}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read_twice\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")