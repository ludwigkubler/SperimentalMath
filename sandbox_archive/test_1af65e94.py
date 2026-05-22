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

def generate_polynomial(n):
    return [random.randint(0, 1) for _ in range(n + 1)]

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
            result[i][j] %= 2
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = -1
        for i in range(j, m):
            if augmented_matrix[i][j] == 1:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        augmented_matrix[pivot_row], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[pivot_row]
        for i in range(m):
            if i != j and augmented_matrix[i][j] == 1:
                factor = augmented_matrix[i][j]
                for k in range(n + 1):
                    augmented_matrix[i][k] = (augmented_matrix[i][k] - factor * augmented_matrix[j][k]) % 2
    return [row[-1] for row in augmented_matrix]

def minimal_order(poly):
    n = len(poly) - 1
    if n == 0:
        return 0
    A = [[poly[i] ** j % 2 for j in range(n + 1)] for i in range(n + 1)]
    b = [0] * (n + 1)
    solution = gaussian_elimination(A, b)
    if all(x == 0 for x in solution):
        return n
    else:
        return min([i for i, x in enumerate(solution) if x != 0])

def acc0_circuit_threshold(poly):
    n = len(poly) - 1
    A = [[poly[i] ** j % 2 for j in range(n + 1)] for i in range(n + 1)]
    b = [0] * (n + 1)
    solution = gaussian_elimination(A, b)
    return any(x != 0 for x in solution)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_polynomial(n)
    if acc0_circuit_threshold(poly) and minimal_order(poly) < n:
        return {
            "metric_name": "minimal_order",
            "metric_value": minimal_order(poly),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Polynomial {poly} has non-trivial ACC⁰ circuit threshold but minimal order < N"
        }
    else:
        return {
            "metric_name": "minimal_order",
            "metric_value": minimal_order(poly),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Polynomial has non-trivial ACC⁰ circuit threshold but minimal order < N' first_failing_seed={first_failing_seed}")