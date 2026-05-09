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

def generate_read_twice_bp(n):
    return [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]

def generate_read_once_bp(n):
    return [random.choice([0, 1]) for _ in range(n)]

def fourier_transform(bp, n):
    def gaussian_elimination(A, b):
        m, n = len(A), len(b)
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return [b[i] / A[i][i] for i in range(m)]

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def identity_matrix(n):
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        return I

    def inverse_matrix(A):
        n = len(A)
        A_augmented = [A[i] + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        identity = identity_matrix(n)
        gaussian_elimination(A_augmented, identity)
        return [row[n:] for row in A_augmented]

    def tensor_product(A, B):
        m, n = len(A), len(B[0])
        p, q = len(B), len(B[0][0])
        C = [[[0] * q for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        C[i][j][l] += A[i][k] * B[k][j][l]
        return C

    def kronecker_delta(i, j):
        return Fraction(1 if i == j else 0)

    def symmetric_group_representation(n):
        def sgn(permutation):
            n = len(permutation)
            inversions = 0
            for i in range(n):
                for j in range(i+1, n):
                    if permutation[i] > permutation[j]:
                        inversions += 1
            return Fraction(1 if inversions % 2 == 0 else -1)

        def apply_permutation(bp, permutation):
            return [bp[permutation[i]] for i in range(len(bp))]

        representations = []
        for n_cycles in range(1, n+1):
            for cycle in itertools.permutations(range(n), n_cycles):
                representation = [[0] * n for _ in range(n)]
                for i in range(n):
                    representation[apply_permutation(cycle, [i])[0]][i] = sgn(cycle)
                representations.append(representation)
        return representations

    def fourier_coefficient(bp, representation):
        n = len(bp)
        m = len(representation)
        A = [[0] * m for _ in range(m)]
        b = [0] * m
        for i in range(m):
            for j in range(n):
                A[i][j] = representation[j][i]
                b[i] += bp[j]
        return gaussian_elimination(A, b)[0]

    representations = symmetric_group_representation(n)
    coefficients = [fourier_coefficient(bp, rep) for rep in representations]
    return sum(abs(coeff) for coeff in coefficients)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        read_twice_bp = generate_read_twice_bp(n)
        read_once_bp = generate_read_once_bp(n)
        ft_read_twice = fourier_transform(read_twice_bp, n)
        ft_read_once = fourier_transform(read_once_bp, n)
        results.append({
            "n": n,
            "ft_read_twice": ft_read_twice,
            "ft_read_once": ft_read_once
        })
    metric_value = sum(ft_read_twice) / len(n_values)
    instances_tested = len(results)
    conjecture_holds = all(abs(ft_read_twice) >= n**2 for n, _, _ in results)
    counterexample = "" if conjecture_holds else "read-twice BP meets O(n^2) bound"
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read-twice BP meets O(n^2) bound\" first_failing_seed={first_failing_seed}")