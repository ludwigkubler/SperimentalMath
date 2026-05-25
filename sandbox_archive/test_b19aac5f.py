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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_subtract(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_transpose(A):
    m, n = len(A), len(A[0])
    C = [[A[j][i] for j in range(m)] for i in range(n)]
    return C

def matrix_inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    A_augmented = [A[i] + I[i] for i in range(m)]
    for i in range(m):
        pivot = A_augmented[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for j in range(n * 2):
            A_augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A_augmented[j][i]
                for k in range(n * 2):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    return [row[n:] for row in A_augmented]

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    A_b = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        pivot_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A_b[i], A_b[pivot_row] = A_b[pivot_row], A_b[i]
        for j in range(n + 1):
            A_b[i][j] /= A_b[i][i]
        for j in range(m):
            if j != i:
                factor = A_b[j][i]
                for k in range(n + 1):
                    A_b[j][k] -= factor * A_b[i][k]
    return [row[n] for row in A_b]

def min_rank(A):
    m, n = len(A), len(A[0])
    if m == 0 or n == 0:
        return 0
    rank = 0
    for i in range(min(m, n)):
        if A[i][i] != 0:
            rank += 1
    return rank

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def randomized_circuit_complexity(f, n):
    m = len(f)
    k = int(math.log(m, 2))
    if k == 0:
        return 1
    A = [[f[i] ^ f[j] for j in range(m)] for i in range(m)]
    B = [[random.choice([0, 1]) for _ in range(k)] for _ in range(m)]
    C = matrix_multiply(A, B)
    D = [sum(C[i][j] * (2**j) for j in range(k)) for i in range(m)]
    return k + randomized_circuit_complexity(D, n-1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = random_boolean_function(n)
        A_f = [[f[i] ^ f[j] for j in range(2**n)] for i in range(2**n)]
        R_f = randomized_circuit_complexity(f, n)
        MinRank_A_f = min_rank(A_f)
        results.append({
            "n": n,
            "MinRank_A_f": MinRank_A_f,
            "log_R_f": math.log(R_f),
            "ratio": MinRank_A_f / math.log(n) if n > 0 else float('inf')
        })
    metric_value = sum(result["ratio"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["ratio"] >= 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "MinRank(A_f) / log(n)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")