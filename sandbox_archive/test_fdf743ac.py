# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def operator_norm(A):
        m, n = len(A), len(A[0])
        max_row_sum = 0
        for i in range(m):
            row_sum = sum(abs(x) for x in A[i])
            if row_sum > max_row_sum:
                max_row_sum = row_sum
        return max_row_sum

    def noncommutative_fourier_transform(P, n):
        m = len(P)
        F = [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for x in range(m):
            g_x = [Fraction(x & (1 << i)) for i in range(n)]
            F[x] = matrix_multiply(P, g_x)
        return F

    def read_twice_bp(n):
        P = [[0] * n for _ in range(2 ** n)]
        for x in range(2 ** n):
            if x & 1 == 0:
                P[x][x ^ (1 << (n - 1))] = Fraction(1)
            else:
                P[x][x ^ (1 << (n - 1))] = Fraction(-1)
        return P

    def is_trivial_bp(P):
        m, n = len(P), len(P[0])
        for x in range(m):
            if sum(abs(p) for p in P[x]) != 1:
                return False
        return True

    n = 40
    P = read_twice_bp(n)
    F = noncommutative_fourier_transform(P, n)
    norm = operator_norm(F)

    metric_name = "operator_norm"
    metric_value = norm
    instances_tested = 1
    conjecture_holds = is_trivial_bp(P) and norm == Fraction(2 * n - 2) or not is_trivial_bp(P) and norm >= n
    counterexample = "" if conjecture_holds else "Nontrivial BP with small norm"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")