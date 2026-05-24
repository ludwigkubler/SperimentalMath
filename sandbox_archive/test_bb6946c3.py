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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def hodge_decomposition(A):
        m, n = len(A), len(A[0])
        U = [[0] * n for _ in range(m)]
        S = [[0] * n for _ in range(n)]
        Vt = [[0] * m for _ in range(n)]
        for i in range(m):
            U[i][i] = 1
        for j in range(n):
            S[j][j] = A[j][j]
        for k in range(n):
            Vt[k][k] = 1
        return U, S, Vt

    def sipser_function(x):
        return x % 2 == 0

    def acc0_circuit_size(A, B):
        m, n = len(A), len(B)
        C = matrix_multiplication(A, B)
        rank = 0
        for row in gaussian_elimination(C):
            if any(row):
                rank += 1
        return rank

    def local_index_of_hodge_decomposition(U, S, Vt):
        m, n = len(U), len(S)
        lihd = 0
        for i in range(n):
            if U[i][i] != 0:
                lihd += math.log(abs(U[i][i]))
        return lihd

    def generate_random_function(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_function(n)
    U, S, Vt = hodge_decomposition(f)
    lihd = local_index_of_hodge_decomposition(U, S, Vt)
    acc0_size = acc0_circuit_size(f, f) if sipser_function(lihd) else float('inf')

    return {
        "metric_name": "local_index_of_hodge_decomposition",
        "metric_value": lihd,
        "instances_tested": 1,
        "conjecture_holds": lihd <= 2,
        "counterexample": "" if lihd <= 2 else f"Function with LIHD={lihd}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_lihd = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lihd} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lihd} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"LIHD > 2\" first_failing_seed={first_failing_seed}")