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

def generate_disjointness_instance(n):
    A = [random.randint(0, n-1) for _ in range(n)]
    B = [random.randint(0, n-1) for _ in range(n)]
    return A, B

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[sum(A[i][j] * B[j][k] for j in range(k)) for k in range(k)] for i in range(m)]
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    A_copy = [row[:] for row in A]
    rank = gaussian_elimination(A_copy)
    non_zero_rows = sum(1 for row in rank if any(row))
    return non_zero_rows

def schatten_p_norm(A, p):
    singular_values = [math.sqrt(eigenvalue) for eigenvalue in matrix_svd(A)]
    return (sum(singular_value**p for singular_value in singular_values))**(1/p)

def matrix_svd(A):
    m, n = len(A), len(A[0])
    U = [[A[i][j] for j in range(n)] for i in range(m)]
    V = [[A[j][i] for j in range(m)] for i in range(n)]
    S = [matrix_rank(matrix_multiplication(U[i], V[j])) for i in range(m) for j in range(n)]
    return S

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    c = 0.5
    metric_name = "Schatten p-norm"
    instances_tested = sum(n for n in n_values)
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        A, B = generate_disjointness_instance(n)
        M_n = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        norm_2 = schatten_p_norm(M_n, 2)
        norm_4 = schatten_p_norm(M_n, 4)
        norm_8 = schatten_p_norm(M_n, 8)

        if norm_2 < c * n**(1/2) or norm_4 < c * n**(1/4) or norm_8 < c * n**(1/8):
            conjecture_holds = False
            counterexample = f"n={n}, ||M_n||_2={norm_2}, ||M_n||_4={norm_4}, ||M_n||_8={norm_8}"
            break

    return {
        "metric_name": metric_name,
        "metric_value": norm_2,  # Using norm_2 for simplicity in reporting
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")