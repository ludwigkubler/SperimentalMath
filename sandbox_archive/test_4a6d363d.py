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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(G[i])
        L[i][i] = -degree
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def heat_kernel_method(L, t=1.0):
    n = len(L)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    A = I
    while t > 0:
        if t >= 1:
            A = matrix_multiply(A, L)
            t -= 1
        else:
            A = matrix_multiply(A, L)
            t *= 2
            I = matrix_multiply(I, L)
    return gaussian_elimination(A)

def communication_complexity_rank(G):
    n = len(G)
    clauses = []
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                clauses.append([i+1, -j-1])
                clauses.append([-i-1, j+1])
    variables = set(abs(lit) for clause in clauses for lit in clause)
    assignment = {var: random.choice([True, False]) for var in variables}
    def evaluate(clause):
        return any(assignment[var] if lit > 0 else not assignment[-lit] for lit in clause)
    unsatisfied_clauses = [clause for clause in clauses if not evaluate(clause)]
    return len(unsatisfied_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mli_values = []
    r_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = sum(G[i])
        mli = heat_kernel_method(laplacian_matrix(G))
        r = communication_complexity_rank(G)
        mli_values.append(mli[0][0].numerator / mli[0][0].denominator)
        r_values.append(r)
        instances_tested += n
        n_max = max(n_max, n)

    correlation_coefficient = sum((mli - mli_avg) * (r - r_avg) for mli, r in zip(mli_values, r_values)) / math.sqrt(sum((mli - mli_avg)**2 for mli in mli_values) * sum((r - r_avg)**2 for r in r_values))
    mean_absolute_difference = sum(abs(mli - r) for mli, r in zip(mli_values, r_values)) / len(mli_values)

    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_absolute_difference=<{}>".format(correlation_coefficient, mean_absolute_difference)

    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))