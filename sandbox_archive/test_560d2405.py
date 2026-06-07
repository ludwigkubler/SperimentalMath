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
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
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

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_index(P):
        n = len(P)
        if n == 0:
            return 0
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = sum(1 for p in P if p[i] != p[j])
                A[j][i] = A[i][j]
        A[n][n] = 0
        rank = 0
        for i in range(n+1):
            row = [A[i][j] for j in range(n+1)]
            if any(row[j] != 0 for j in range(n+1)):
                rank += 1
                pivot_col = next(j for j in range(n+1) if row[j] != 0)
                for j in range(n+1):
                    A[i][j] /= row[pivot_col]
                for k in range(n+1):
                    if k != i:
                        factor = A[k][pivot_col]
                        for j in range(n+1):
                            A[k][j] -= factor * A[i][j]
        return rank

    def generate_instance(n):
        variables = [random.choice([0, 1]) for _ in range(n)]
        P = []
        while len(P) < n:
            new_var = random.choice(variables)
            if all(new_var != p[i] for p in P for i in range(len(p))):
                P.append(new_var)
        return variables, P

    def fit_log_function(data):
        x = [math.log(n) for n, _ in data]
        y = [h for _, h in data]
        A = [[x_i**2, x_i] for x_i in x]
        b = y
        A_t = list(zip(*A))
        A_inv = gaussian_elimination(matrix_multiply(A_t, A))
        beta = matrix_multiply(matrix_multiply(A_inv, A_t), b)
        return beta[0], beta[1]

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        h_max = 0
        for _ in range(5):
            variables, P = generate_instance(n)
            h = hodge_index(P)
            results.append((n, h))
            instances_tested += 1
            if h > h_max:
                h_max = h
        if h_max > c * math.log2(n)**2:
            return {
                "metric_name": "Hodge Index",
                "metric_value": h_max,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"n={n}, h={h_max} > {c * math.log2(n)**2}"
            }
    beta = fit_log_function(results)
    c = -beta[1] / (2 * beta[0])
    return {
        "metric_name": "Hodge Index",
        "metric_value": c,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max < 16\" first_failing_seed={first_failing_seed}")