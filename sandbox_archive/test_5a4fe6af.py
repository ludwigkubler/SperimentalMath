# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_disjointness_matrix(n):
    A = [random.randint(0, 1) for _ in range(n)]
    B = [random.randint(0, 1) for _ in range(n)]
    M_n = [[A[i] ^ B[j] for j in range(n)] for i in range(n)]
    return M_n

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(m)] for i in range(k)]
    return C

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [row[:] + [1] for row in matrix]
    U = []
    V = []
    for i in range(min(m, n)):
        max_row = max(range(i, m), key=lambda x: abs(A[x][i]))
        if A[max_row][i] == 0:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        U.append([1 if j == i else 0 for j in range(n)])
        V.append([1 if j == i else 0 for j in range(m)])
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
    rank = sum(1 for row in U if any(row))
    return rank

def schatten_p_norm(matrix, p):
    singular_values = []
    m, n = len(matrix), len(matrix[0])
    for i in range(min(m, n)):
        max_row = max(range(i, m), key=lambda x: abs(matrix[x][i]))
        if matrix[max_row][i] == 0:
            continue
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        singular_values.append(abs(matrix[i][i]))
    return sum(singular_value ** p for singular_value in singular_values) ** (1 / p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "Schatten_p_norm"
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            M_n = generate_disjointness_matrix(n)
            norm_2 = schatten_p_norm(M_n, 2)
            norm_4 = schatten_p_norm(M_n, 4)
            norm_8 = schatten_p_norm(M_n, 8)
            if norm_2 < n ** (1/2) or norm_4 < n ** (1/4) or norm_8 < n ** (1/8):
                conjecture_holds = False
                counterexample = f"n={n}, p=2: {norm_2}, p=4: {norm_4}, p=8: {norm_8}"
            total_metric_value += norm_2 + norm_4 + norm_8
            instances_tested += 3

    return {
        "metric_name": metric_name,
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif counterexample := [r["counterexample"] for r in results if r["counterexample"]][0]:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if r['conjecture_holds'] == False))]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")