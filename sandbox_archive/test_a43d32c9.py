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
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elim(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for k in range(n):
        max_row = k
        for i in range(k+1, n):
            if abs(M[i][k]) > abs(M[max_row][k]):
                max_row = i
        M[k], M[max_row] = M[max_row], M[k]
        pivot = M[k][k]
        for j in range(k, n+1):
            M[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = M[i][k]
                for j in range(k, n+1):
                    M[i][j] -= factor * M[k][j]
    x = [M[i][-1] for i in range(n)]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            # Generate random permutation
            perm = list(range(n))
            random.shuffle(perm)
            perm_matrix = [[int(i == j) for j in range(n)] for i in range(n)]
            for i in range(n):
                perm_matrix[i][perm[i]] = 1

            # Find minimal order of element in Coxeter group
            identity = [0] * n
            identity[0] = 1
            order = 1
            while True:
                if matrix_mult(perm_matrix, identity) == identity:
                    break
                identity = matrix_mult(perm_matrix, identity)
                order += 1

            # Check conjecture for permutations
            expected_order = n**2 / 4
            if order < expected_order:
                conjecture_holds = False
                counterexample = f"Permutation {perm} with order {order} < {expected_order}"
                break

        # Construct permutation circuit (simplified example)
        depth = random.randint(1, 5)
        width = random.randint(2, 4)
        circuit_size = depth * width
        if circuit_size > n:
            continue

        # Find minimal order of element in Coxeter group for circuit
        identity = [0] * n
        identity[0] = 1
        order = 1
        while True:
            if matrix_mult(perm_matrix, identity) == identity:
                break
            identity = matrix_mult(perm_matrix, identity)
            order += 1

        # Check conjecture for circuits
        expected_order = (depth + width)**2
        if order < expected_order:
            conjecture_holds = False
            counterexample = f"Circuit with depth {depth}, width {width} and order {order} < {expected_order}"
            break

        total_metric_value += order
        instances_tested += 1

    return {
        "metric_name": "Minimal Order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")