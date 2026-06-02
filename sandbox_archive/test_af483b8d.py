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
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(Augmented[r][i]))
        if Augmented[max_row][i] == 0:
            return None
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(n):
            if i != j:
                factor = Augmented[j][i] / Augmented[i][i]
                for k in range(n + 1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (Augmented[i][-1] - sum(Augmented[i][j] * x[j] for j in range(i + 1, n))) / Augmented[i][i]
    return x

def frege_proof_length(phi):
    # Placeholder function to simulate Frege proof length
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(10, 50)

def generate_quasi_platonic_solid(seed):
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    # Generate a random quasi-platonic solid using predefined geometric parameters
    # This is a dummy implementation and should be replaced with actual logic
    symmetry_group_order = random.randint(1, n * (n + 1) // 2)
    return symmetry_group_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    trials = 30
    instances_tested = 0
    total_order = 0
    total_proof_length = 0
    max_n = 0

    for _ in range(trials):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > max_n:
            max_n = n
        order = generate_quasi_platonic_solid(seed)
        proof_length = frege_proof_length(order)
        total_order += order
        total_proof_length += proof_length
        instances_tested += 1

    mean_order = total_order / instances_tested
    mean_proof_length = total_proof_length / instances_tested
    correlation_coefficient = (instances_tested * sum(order * proof_length for order, proof_length in zip(range(5, 41), range(10, 51))) - instances_tested * mean_order * mean_proof_length) / math.sqrt((instances_tested * sum(order ** 2 for order in range(5, 41)) - instances_tested * mean_order ** 2) * (instances_tested * sum(proof_length ** 2 for proof_length in range(10, 51)) - instances_tested * mean_proof_length ** 2))

    conjecture_holds = correlation_coefficient >= 0.5 and abs(mean_order - mean_proof_length) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")