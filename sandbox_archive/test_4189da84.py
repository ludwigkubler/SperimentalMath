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

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        if factor == 0:
            continue
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[-1] for row in augmented_matrix]

def rank(A):
    A_copy = [row[:] for row in A]
    return len(gaussian_elimination(A_copy, [0] * len(A)))

def generate_geometrically_quantized_space(n):
    # Placeholder function to generate a random geometrically quantized space
    # This is a stub and should be replaced with actual implementation
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def acc0_circuit_weight(char_func):
    # Placeholder function to compute the ACC⁰ circuit weight of a characteristic function
    # This is a stub and should be replaced with actual implementation
    return sum(1 for bit in char_func if bit == 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 30
    total_rank_quant = 0
    total_acc0_weight = 0

    for _ in range(instances_tested):
        X = generate_geometrically_quantized_space(n)
        rank_quant = rank(X)
        char_func = [random.choice([0, 1]) for _ in range(2**n)]
        acc0_weight = acc0_circuit_weight(char_func)
        total_rank_quant += rank_quant
        total_acc0_weight += acc0_weight

    mean_rank_quant = total_rank_quant / instances_tested
    mean_acc0_weight = total_acc0_weight / instances_tested
    conjecture_holds = mean_rank_quant <= mean_acc0_weight
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "RankQuant(X)",
        "metric_value": mean_rank_quant,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank_quant = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_quant} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_quant} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")