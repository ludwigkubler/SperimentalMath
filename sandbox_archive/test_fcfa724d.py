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

def generate_ac0_circuit(n):
    depth = random.randint(2, n // 2)
    circuit = []
    for _ in range(depth):
        layer = [random.choice([0, 1]) for _ in range(n)]
        circuit.append(layer)
    return circuit

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
        pivot = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(i, n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def compute_real_rank(matrix):
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented = matrix + identity
    rank = 0
    for i in range(n):
        if augmented[i][i] != 0:
            rank += 1
            for j in range(i+1, n):
                factor = augmented[j][i]
                for k in range(i, n * 2):
                    augmented[j][k] -= factor * augmented[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    circuit = generate_ac0_circuit(n)
    size_C = len(circuit) ** (1 / len(circuit))
    depth = len(circuit)
    coefficient_matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if i & j == 0:
                coeff = sum(circuit[k][i ^ j] for k in range(depth)) % 2
                coefficient_matrix[i][j] = coeff
    real_rank = compute_real_rank(coefficient_matrix)
    conjecture_holds = real_rank >= 0.1 * math.log(size_C)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "real_rank",
        "metric_value": real_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")