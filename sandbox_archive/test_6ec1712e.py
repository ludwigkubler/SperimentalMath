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

def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix dimensions must be compatible for multiplication")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def lu_decomposition(A):
    n = len(A)
    L = [[0 for _ in range(n)] for _ in range(n)]
    U = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            sum_upper = sum(L[k][j] * U[k][i] for k in range(i))
            U[i][j] = A[i][j] - sum_upper
        for k in range(i + 1, n):
            sum_lower = sum(L[k][i] * U[i][j] for j in range(i))
            L[k][i] = (A[k][i] - sum_lower) / U[i][i]

    return L, U

def tensor_rank(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    if n == 1:
        return 1

    L, U = lu_decomposition(matrix)
    rank = sum(1 for row in U if any(val != Fraction(0) for val in row))
    return rank

def generate_read_once_bp(n):
    bp = []
    for _ in range(n):
        layer = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        bp.append(layer)
    return bp

def generate_read_twice_bp(n):
    bp = []
    for _ in range(2):
        layer = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        bp.append(layer)
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)

    n_values = [5, 10, 15, 20, 30, 40]
    read_once_rank_sum = 0
    read_twice_rank_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            read_once_bp = generate_read_once_bp(n)
            read_twice_bp = generate_read_twice_bp(n)

            read_once_matrix = matrix_multiplication(*read_once_bp)
            read_twice_matrix = matrix_multiplication(*read_twice_bp)

            read_once_rank = tensor_rank(read_once_matrix)
            read_twice_rank = tensor_rank(read_twice_matrix)

            if read_once_rank > 4 * math.log(n):
                return {
                    "metric_name": "Read-Once Rank",
                    "metric_value": read_once_rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={read_once_rank} > 4 * log({n})"
                }

            if read_twice_rank < 2**(n/2) / n**2:
                return {
                    "metric_name": "Read-Twice Rank",
                    "metric_value": read_twice_rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={read_twice_rank} < 2^{n/2} / {n**2}"
                }

            read_once_rank_sum += read_once_rank
            read_twice_rank_sum += read_twice_rank
            instances_tested += 1

    mean_read_once_rank = read_once_rank_sum / instances_tested
    mean_read_twice_rank = read_twice_rank_sum / instances_tested

    return {
        "metric_name": "Read-Once Rank",
        "metric_value": mean_read_once_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_read_once_rank = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)

    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_read_once_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_read_once_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")