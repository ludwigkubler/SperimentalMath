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

def generate_random_entangled_state(n):
    state = [[Fraction(0, 1)] * n for _ in range(n)]
    for i in range(n):
        state[i][i] = Fraction(1, 2)
    return state

def matrix_multiplication(A, B):
    n = len(B[0])
    result = [[Fraction(0, 1) for _ in range(n)] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != Fraction(0, 1) for j in range(n)):
            rank += 1
    return rank

def distillable_entropy(state):
    n = len(state)
    v = [Fraction(1, math.sqrt(n))] * n
    Av = matrix_multiplication(state, v)
    max_value = max(abs(x) for row in Av for x in row)
    epsilon = 0.5 - max_value / 2
    return epsilon

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    state = generate_random_entangled_state(n)
    epsilon = distillable_entropy(state)
    if epsilon <= 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "distillable_entropy_non_positive"
        }
    Av = matrix_multiplication(state, v)
    max_value = max(abs(x) for row in Av for x in row)
    tau = rank(Av)
    return {
        "metric_name": "minimal_rank",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": tau >= Fraction(1, 10) * math.log(1 / epsilon),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 53))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_tau = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / len(results)
    std_tau = math.sqrt(sum((result["metric_value"] - mean_tau) ** 2 for result in results if result["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")