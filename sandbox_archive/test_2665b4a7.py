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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def hook_length_formula(shape):
    n = sum(shape)
    numerator = factorial(n)
    denominator = 1
    for row in shape:
        for cell in range(len(row)):
            h = row[cell] + len(shape) - cell - 1
            denominator *= (h + 1)
    return numerator // denominator

def sign_permutation(perm):
    n = len(perm)
    sgn = 1
    for i in range(n):
        if perm[i] != i:
            j = perm.index(i)
            perm[i], perm[j] = perm[j], perm[i]
            sgn *= -1
    return sgn

def young_symmetrizer(shape, sign):
    n = sum(shape)
    basis_element = [0] * factorial(n)
    for perm in itertools.permutations(range(n)):
        if sign_permutation(perm) == sign:
            index = 0
            for row in shape:
                for cell in range(len(row)):
                    i = perm.index(row[cell])
                    j = perm.index(cell + sum(shape[:row.index(row[cell])]))
                    index += math.factorial(sum(shape[:cell])) * binomial_coefficient(n - i, len(shape) - 1)
            basis_element[index] += 1
    return basis_element

def permanent(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    result = 0
    for sign in (-1, 1):
        perm = list(range(n))
        while True:
            result += sign * math.prod([matrix[i][perm[i]] for i in range(n)])
            next_permutation(perm)
            if perm == list(range(n)):
                break
    return abs(result)

def determinant(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    result = 0
    for sign in (-1, 1):
        perm = list(range(n))
        while True:
            result += sign * math.prod([matrix[i][perm[i]] for i in range(n)])
            next_permutation(perm)
            if perm == list(range(n)):
                break
    return result

def next_permutation(perm):
    n = len(perm)
    i = n - 2
    while i >= 0 and perm[i] >= perm[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = n - 1
    while perm[j] <= perm[i]:
        j -= 1
    perm[i], perm[j] = perm[j], perm[i]
    left, right = i + 1, n - 1
    while left < right:
        perm[left], perm[right] = perm[right], perm[left]
        left += 1
        right -= 1
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            matrix = [[random.choice([1, -1]) for _ in range(n)] for _ in range(n)]
            perm_basis = young_symmetrizer((n,), 1)
            det_basis = young_symmetrizer((n,), -1)

            perm_coeff_sum = sum(abs(perm_basis[i] * permanent(matrix)) for i in range(factorial(n)))
            det_coeff_sum = sum(abs(det_basis[i] * determinant(matrix)) for i in range(factorial(n)))

            if perm_coeff_sum <= 2**(n/4) * det_coeff_sum:
                conjecture_holds = False
                counterexample = f"n={n}, matrix={matrix}"
                break

            total_metric_value += perm_coeff_sum - det_coeff_sum
            instances_tested += 1

    return {
        "metric_name": "Exponential Gap",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [53, 67, 89, 101]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")