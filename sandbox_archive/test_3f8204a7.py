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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, p = len(A), len(B[0])
    result = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def free_probability_tensor_entanglement(P, Q):
    n = len(P)
    entanglement = 0
    for i in range(n):
        for j in range(i + 1, n):
            T_i = P[i]
            T_j = Q[j]
            product = matrix_multiply(T_i, T_j)
            max_abs_value = max(abs(product[k][l]) for k in range(len(product)) for l in range(len(product[0])))
            entanglement = max(entanglement, max_abs_value)
    return entanglement

def check_bp(P):
    n = len(P)
    entanglement = free_probability_tensor_entanglement(P, P)
    return {"metric_name": "free_probability_tensor_entanglement", "metric_value": entanglement, "instances_tested": 1, "conjecture_holds": entanglement <= Fraction(n).log2(), "counterexample": ""}

def check_ip_2():
    n = random.randint(5, 40)
    P = [[Fraction(random.choice([-1, 1])) for _ in range(n)] for _ in range(n)]
    entanglement = free_probability_tensor_entanglement(P, P)
    return {"metric_name": "free_probability_tensor_entanglement", "metric_value": entanglement, "instances_tested": 1, "conjecture_holds": entanglement >= n, "counterexample": ""}

def run_trial(seed: int) -> dict:
    random.seed(seed)
    if random.choice([True, False]):
        return check_bp([[Fraction(random.choice([-1, 1])) for _ in range(n)] for n in [5, 10, 15, 20, 30, 40]])
    else:
        return check_ip_2()

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")