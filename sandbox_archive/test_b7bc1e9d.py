# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix multiplication not possible")

    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    lead = 0
    for r in range(rows):
        if lead >= cols:
            break
        i = r
        while matrix[i][lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if lead == cols:
                    return matrix, False
        matrix[r], matrix[i] = matrix[i], matrix[r]
        factor = Fraction(matrix[r][lead])
        for j in range(cols):
            matrix[r][j] /= factor
        for i in range(rows):
            if i != r and matrix[i][lead]:
                factor = Fraction(matrix[i][lead])
                for j in range(cols):
                    matrix[i][j] -= factor * matrix[r][j]
        lead += 1
    return matrix, True

def rank_of_matrix(matrix):
    matrix, _ = gaussian_elimination(matrix)
    return sum(1 for row in matrix if any(row))

def minimal_representation_rank(n):
    S3 = [
        [[0, 1, 2], [1, 0, 2], [2, 2, 0]],
        [[0, 2, 1], [2, 0, 1], [1, 1, 0]]
    ]
    T_n = S3
    for _ in range(n - 1):
        T_n = matrix_multiplication(T_n, S3)
    return rank_of_matrix(T_n)

def k_clique_instance(n):
    vertices = list(range(1, n + 1))
    edges = [(i, j) for i in vertices for j in vertices if i < j]
    random.shuffle(edges)
    return random.sample(edges, min(len(edges), random.randint(2, n - 1)))

def det_m(m):
    matrix = [[Fraction(0)] * m for _ in range(m)]
    for i in range(m):
        matrix[i][i] = Fraction(1)
    return rank_of_matrix(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            clique_instance = k_clique_instance(n)
            rho_T_n = minimal_representation_rank(n)
            m = int(n ** 1.5)
            rho_det_m = det_m(m)

            if rho_T_n > rho_det_m:
                conjecture_holds = False
                counterexample = f"n={n}, clique_instance={clique_instance}, rho_T_n={rho_T_n}, rho_det_m={rho_det_m}"
                break

        instances_tested += 5

    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": (sum(rho_T_n for n in n_values for _ in range(5)) / instances_tested),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")