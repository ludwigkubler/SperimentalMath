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

def matrix_mult(A, B):
    n = len(A)
    C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
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

def communication_complexity_rank(generators, relations):
    n = len(generators)
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i, j) in relations or (j, i) in relations:
                A[i][j] = Fraction(1)
    inv_A = matrix_inv(A)
    r_C = sum(sum(row[j] * inv_A[j][k] for j in range(n)) for k in range(n))
    return r_C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = Fraction(0)
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            generators = [(i, j) for i in range(n) for j in range(i+1, n)]
            relations = set()
            while len(relations) < n:
                u, v = random.sample(generators, 2)
                if abs(u[0] - v[0]) == abs(u[1] - v[1]):
                    relations.add((u, v))
            r_C = communication_complexity_rank(generators, relations)
            G_C_rank = len(relations) + 1
            instances_tested += 1
            total_metric_value += G_C_rank - r_C**2

            if G_C_rank > 1.44 * r_C**2:
                conjecture_holds = False
                counterexample = f"n={n}, |G(C)|={G_C_rank}, r(C)^2={r_C**2}"

    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = (sum((total_metric_value - Fraction(0))**2 for _ in range(instances_tested)) / instances_tested).sqrt()

    return {
        "metric_name": "Rank Variance",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results)).sqrt()
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")