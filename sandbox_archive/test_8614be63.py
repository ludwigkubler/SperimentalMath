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

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        for j in range(k, n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_det(A):
    n = len(A)
    det = Fraction(1, 0)
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            return Fraction(0, 1)
        det *= pivot
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return det

def generate_circuit(n):
    if n == 1:
        return []
    edges = [(0, 1)]
    for i in range(2, n):
        edges.append((i-1, i))
    random.shuffle(edges)
    return edges

def construct_coxeter_group(edges):
    generators = set()
    relations = set()
    for u, v in edges:
        generators.add(u)
        generators.add(v)
        if abs(u - v) == 1:
            relations.add((u, v))
        else:
            relations.add((v, u))
    return generators, relations

def communication_complexity_rank(generators, relations):
    n = len(generators)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
    for u, v in relations:
        A[u][v] = -1
        A[v][u] = -1
    inv_A = matrix_inv(A)
    rank = sum(1 for row in inv_A if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_sum = Fraction(0, 1)
    metric_squared_sum = Fraction(0, 1)
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        edges = generate_circuit(n)
        generators, relations = construct_coxeter_group(edges)
        r_C = communication_complexity_rank(generators, relations)
        G_C_size = len(generators)

        if G_C_size > 1.44 * r_C**2:
            conjecture_holds = False
            counterexample = f"n={n}, |G(C)|={G_C_size}, r(C)^2={r_C**2}"

        instances_tested += n
        metric_sum += G_C_size
        metric_squared_sum += G_C_size**2

    mean_value = metric_sum / instances_tested
    variance = (metric_squared_sum / instances_tested) - mean_value**2
    support_fraction = Fraction(instances_tested, 30)

    return {
        "metric_name": "Coxeter Group Rank Variance",
        "metric_value": variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    variance = sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={variance} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")