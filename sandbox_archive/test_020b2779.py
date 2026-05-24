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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    matrix = [row[:] for row in matrix]
    gaussian_elimination(matrix)
    rank = 0
    for i in range(m):
        if any(matrix[i]):
            rank += 1
    return rank

def commutator(A, B):
    return matrix_multiply(matrix_multiply(A, B), -matrix_multiply(B, A))

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def random_quantum_channel(n):
    channel = []
    for _ in range(n):
        row = [random.random() for _ in range(n)]
        channel.append(row)
    return channel

def minimal_index_of_noncommutativity(channel):
    identity = identity_matrix(len(channel))
    rho = rank(commutator(identity, channel))
    return rho

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rho = 0
    instances_tested = 0
    
    for n in n_values:
        channel = random_quantum_channel(n)
        rho = minimal_index_of_noncommutativity(channel)
        total_rho += rho
        instances_tested += 1
    
    mean_rho = total_rho / len(n_values)
    conjecture_holds = all(5 <= rho <= 20 for rho in [minimal_index_of_noncommutativity(random_quantum_channel(n)) for n in range(5, 41)])
    
    return {
        "metric_name": "minimal_index_of_noncommutativity",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")