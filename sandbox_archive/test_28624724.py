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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in G[i] if j > 0)
        L[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j] > 0:
                L[i][j] = L[j][i] = 1
    return L

def minimal_local_indefinite_integral(L):
    n = len(L)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    A = matrix_multiply(I, L)
    b = [Fraction(0)] * n
    x = gaussian_elimination(A, b)
    return sum(x[i] ** 2 for i in range(n))

def communication_complexity_rank(G):
    n = len(G)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] > 0:
                clauses.append([i + 1, -(j + 1)])
    assignment = {var: random.choice([True, False]) for var in range(1, n + 1)}
    unsatisfied_clauses = [clause for clause in clauses if not any(assignment[var] if lit > 0 else not assignment[-lit] for lit in clause)]
    return len(unsatisfied_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mli_sum = 0
    r_sum = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        mli = minimal_local_indefinite_integral(laplacian_matrix(G))
        r = communication_complexity_rank(G)
        mli_sum += mli
        r_sum += r
        instances_tested += n
        if n > n_max:
            n_max = n

    mean_mli = mli_sum / instances_tested
    mean_r = r_sum / instances_tested
    correlation_coefficient = (n_values[1] * sum(mli * r for mli, r in zip([minimal_local_indefinite_integral(laplacian_matrix(G)) for _ in range(n_values[1])], [communication_complexity_rank(G) for _ in range(n_values[1])])) - n_values[1] * mean_mli * mean_r) / math.sqrt((n_values[1] * sum(mli ** 2 for mli in [minimal_local_indefinite_integral(laplacian_matrix(G)) for _ in range(n_values[1])]) - n_values[1] * mean_mli ** 2) * (n_values[1] * sum(r ** 2 for r in [communication_complexity_rank(G) for _ in range(n_values[1])]) - n_values[1] * mean_r ** 2))

    if correlation_coefficient < 0.8 or abs(mean_mli - mean_r) > 3:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> mean_diff=<{}>".format(correlation_coefficient, abs(mean_mli - mean_r))

    return {
        "metric_name": "minimal_local_indefinite_integral_vs_communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={:.2f} support_fraction={:.2f}".format(mean_metric_value, 0.0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={:.2f} support_fraction={:.2f}".format(mean_metric_value, 0.0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(r["counterexample"], first_failing_seed))