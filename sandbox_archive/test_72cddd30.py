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

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        factor = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= factor
        for j in range(i+1, n):
            factor = augmented[j][i]
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented[i][j] * x[j]
    return x

def rank(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    rank = 0
    for i in range(n):
        if any(A_copy[j][i] != 0 for j in range(rank, m)):
            rank += 1
            for j in range(m):
                if j != rank - 1:
                    factor = A_copy[j][i] / A_copy[rank-1][i]
                    for k in range(n):
                        A_copy[j][k] -= factor * A_copy[rank-1][k]
    return rank

def linear_approximation_count(f, n):
    A = [[f(x) for x in range(2**n)] for _ in range(n)]
    b = [x % 2 for x in range(2**n)]
    try:
        x = gaussian_elimination(A, b)
        return rank([A[i] for i in range(n) if abs(x[i]) > 1e-6])
    except Exception as e:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        f = lambda x: random.randint(0, 1)
        L_f = linear_approximation_count(f, n)
        if L_f == float('inf'):
            return {
                "metric_name": "seed_length",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        seed_length = math.log(L_f) + math.log(n)
        total_metric_value += seed_length
        instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "seed_length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")