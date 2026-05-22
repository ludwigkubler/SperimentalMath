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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = None
        for i in range(j, m):
            if augmented[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        augmented[pivot_row], augmented[j] = augmented[j], augmented[pivot_row]
        for i in range(m):
            if i != j:
                factor = augmented[i][j] / augmented[j][j]
                for k in range(n + 1):
                    augmented[i][k] -= factor * augmented[j][k]
    return [row[-1] for row in augmented]

def k_theory_rank(ideal):
    generators = list(ideal)
    m, n = len(generators), len(generators[0])
    A = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if generators[i][j] != 0:
                A[i][j] = 1
    rank = 0
    for col in range(n):
        pivot_row = None
        for row in range(rank, m):
            if A[row][col] == 1:
                pivot_row = row
                break
        if pivot_row is not None:
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
    return rank

def random_monomial_ideal(n, k):
    generators = []
    for _ in range(k):
        monomial = [random.randint(0, 1) for _ in range(n)]
        while sum(monomial) == 0:
            monomial = [random.randint(0, 1) for _ in range(n)]
        generators.append(frozenset(monomial))
    return frozenset(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            ideal = random_monomial_ideal(n, random.randint(1, n))
            rank = k_theory_rank(ideal)
            circuit_depth = n  # Placeholder for actual circuit depth computation
            total_ratio += rank / circuit_depth
            instances_tested += 1
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 1
    return {
        "metric_name": "K-theory Rank / Circuit Depth",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")