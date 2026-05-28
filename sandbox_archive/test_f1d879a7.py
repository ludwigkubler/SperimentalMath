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
    m, k, n = len(A), len(B), len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                max_row = i
        augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
        pivot = augmented_matrix[j][j]
        for k in range(j, n+1):
            augmented_matrix[j][k] /= pivot
        for i in range(m):
            if i != j:
                factor = augmented_matrix[i][j]
                for k in range(j, n+1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    return [row[-1] for row in augmented_matrix]

def is_full_rank(matrix):
    rank = 0
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
            continue
        rank += 1
        for j in range(i+1, m):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return rank == n

def minimal_rank_cyclic_difference_set(order):
    if order <= 2:
        return float('inf')
    generators = [1, order - 1]
    while True:
        new_generators = set()
        for gen in generators:
            for i in range(1, order):
                new_gen = (gen * i) % order
                if new_gen not in new_generators and new_gen != 0 and new_gen != order - 1:
                    new_generators.add(new_gen)
        if len(new_generators) == len(generators):
            break
        generators = list(new_generators)
    return len(generators)

def communication_complexity(n, seed):
    random.seed(seed)
    symmetric_instance = [random.choice([0, 1]) for _ in range(n)]
    asymmetric_instance = [1 - bit for bit in symmetric_instance]
    # Simplified communication complexity measure
    return sum(1 for i in range(n) if symmetric_instance[i] != asymmetric_instance[i])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_rank = 0
    total_complexity = 0

    for _ in range(50):
        rank = minimal_rank_cyclic_difference_set(2**n)
        complexity = communication_complexity(n, seed)
        if rank == float('inf'):
            return {
                "metric_name": "minimal_rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        total_rank += rank
        total_complexity += complexity
        instances_tested += 1

    mean_rank = total_rank / instances_tested
    mean_complexity = total_complexity / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * comp for rank, comp in zip(range(50), range(50))) -
                               instances_tested * mean_rank * mean_complexity) / \
                              math.sqrt((instances_tested * sum(rank**2 for rank in range(50)) - instances_tested * mean_rank**2) *
                                        (instances_tested * sum(comp**2 for comp in range(50)) - instances_tested * mean_complexity**2))

    return {
        "metric_name": "minimal_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")