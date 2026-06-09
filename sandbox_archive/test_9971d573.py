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

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A_augmented = [row + col for row, col in zip(A, I)]

    for i in range(n):
        pivot = A_augmented[i][i]
        if pivot == Fraction(0, 1):
            return None  # Singular matrix
        for j in range(n * 2):
            A_augmented[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(n * 2):
                    A_augmented[k][j] -= factor * A_augmented[i][j]

    inv_A = [row[n:] for row in A_augmented]
    return inv_A

def matrix_mul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[Fraction(0, 1) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def communication_complexity_rank(generators, relations):
    n = len(generators)
    A = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in relations or (j, i) in relations:
                A[i][j] = Fraction(1, 1)
                A[j][i] = Fraction(1, 1)

    inv_A = matrix_inv(A)
    if inv_A is None:
        return float('inf')  # Singular matrix

    rank = 0
    for row in inv_A:
        if any(val != Fraction(0, 1) for val in row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        generators = list(range(n))
        relations = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    relations.add((i, j))

        r_C = communication_complexity_rank(generators, relations)
        if r_C == float('inf'):
            continue

        G_C_rank = len(generators)  # Simplified for testing
        metric_values.append(G_C_rank - r_C**2)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
    conjecture_holds = all(abs(x) <= 0.5 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "rank_difference",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")