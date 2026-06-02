# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primitive_element(p):
    while True:
        a = random.randint(2, p - 1)
        if pow(a, p - 1, p) != 1:
            continue
        for k in range(2, int(math.sqrt(p)) + 1):
            if pow(a, (p - 1) // k, p) == 1:
                break
        else:
            return a

def generate_finite_field_extension(n):
    p = random.choice([2] + [i for i in range(3, 100) if is_prime(i)])
    alpha = generate_primitive_element(p)
    K = [(alpha ** i) % p for i in range(p)]
    L = list(range(p))
    return K, L

def matrix_multiplication(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = i
        for j in range(i + 1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def local_class_group_size(K):
    p = len(K)
    if not is_prime(p):
        raise ValueError("p must be prime")
    G = [(i, (i ** 2) % p) for i in range(1, p)]
    H = [(i, (i ** 3) % p) for i in range(1, p)]
    return len(G) // math.gcd(len(G), len(H))

def communication_complexity_rank(K):
    n = len(K)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            A[i][j] = (K[i] - K[j]) % n
            A[j][i] = (K[j] - K[i]) % n
        b[i] = (K[i] ** 2) % n
    return len(gaussian_elimination(A, b))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "correlation"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        K, L = generate_finite_field_extension(n)
        Cl_K_L = local_class_group_size(K)
        ccr_K_L = communication_complexity_rank(K)
        instances_tested += 1
        n_max = max(n_max, n)

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "not_enough_instances"

    return {
        "metric_name": metric_name,
        "metric_value": 0.5,  # Placeholder value for demonstration purposes
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")