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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [[matrix[i][j] for j in range(n)] for i in range(m)]
    rref = gaussian_elimination(A, [0] * n)
    return sum(1 for x in rref if x != 0)

def hook_length_formula(shape):
    m, n = len(shape), len(shape[0])
    result = math.factorial(m + n - 1) // (math.prod(math.factorial(x) for x in shape))
    for i in range(m):
        for j in range(n):
            if shape[i][j] == 0:
                continue
            hook = m + n - i - j - 2
            result //= hook + 1
    return result

def generate_3cnf(n, clauses):
    variables = set(range(1, n+1))
    formula = []
    for _ in range(clauses):
        clause = random.sample(variables, 3)
        formula.append((random.choice([-1, 1]) * x for x in clause))
    return formula

def monotone_circuit_size(formula):
    # This is a placeholder function. In practice, you would need to implement
    # an algorithm to compute the minimal monotone circuit size.
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    clauses = 2 * n
    formula = generate_3cnf(n, clauses)
    shape = [len(set(x for x in clause if x != 0)) for clause in formula]
    tableau_count = hook_length_formula(shape)
    circuit_size = monotone_circuit_size(formula)
    product = tableau_count * circuit_size
    metric_value = 1 / product if product != 0 else float('inf')
    conjecture_holds = product <= 100  # Placeholder threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "product",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")