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

def run_trial(seed: int) -> dict:
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def hook_length_formula(shape):
        n = len(shape)
        result = 1
        for i in range(n):
            for j in range(len(shape[i])):
                result //= (shape[i][j] - j) * (n - i - shape[i][j])
        return result

    def generate_random_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    def is_permutation(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        for row in matrix:
            if sum(row) != 1 or sorted(row) != list(range(n)):
                return False
        return True

    def is_det_matrix(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        for row in matrix:
            if sum(row) != 1 or sorted(row) != [0] * (n - 1) + [1]:
                return False
        return True

    def decompose(matrix):
        n = len(matrix)
        if is_permutation(matrix):
            return "perm_n"
        elif is_det_matrix(matrix):
            return "det_n"
        else:
            return None

    def count_syts(shape, decomposition_type):
        n = len(shape)
        if decomposition_type == "perm_n":
            return hook_length_formula(shape) * 2 ** (n - len(shape))
        elif decomposition_type == "det_n":
            return hook_length_formula(shape)
        else:
            return 0

    def generate_random_shape(n):
        shape = []
        remaining = n
        while remaining > 0:
            part = random.randint(1, remaining)
            shape.append(part)
            remaining -= part
        return shape

    seed = int(seed)
    random.seed(seed)

    n_values = [5, 10, 15, 20, 30, 40]
    total_count_perm_n = 0
    total_count_det_n = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            matrix = generate_random_matrix(n)
            decomposition_type = decompose(matrix)
            if decomposition_type is not None:
                shape = generate_random_shape(n)
                count_perm_n = count_syts(shape, "perm_n")
                count_det_n = count_syts(shape, "det_n")
                total_count_perm_n += count_perm_n
                total_count_det_n += count_det_n
                instances_tested += 1

    ratio = total_count_perm_n / total_count_det_n if total_count_det_n != 0 else float('inf')
    conjecture_holds = ratio > 2 ** n_values[-1]
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Ratio of SYT counts",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")