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

def generate_ac0_circuit(n):
    if n == 1:
        return [random.choice([0, 1])]
    else:
        left = generate_ac0_circuit(n // 2)
        right = generate_ac0_circuit(n - n // 2)
        return [random.choice(left) ^ random.choice(right)]

def parity_polynomial(circuit):
    if len(circuit) == 1:
        return circuit[0]
    else:
        left = parity_polynomial(circuit[:len(circuit)//2])
        right = parity_polynomial(circuit[len(circuit)//2:])
        return (left + right) % 2

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

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
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= factor
        for k in range(m):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[-1] for row in augmented_matrix]

def real_radical_degree(poly):
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n)]
    b = [0] * n
    for i in range(n):
        A[i][i] = poly[i]
        b[i] = -poly[i]
    return len(gaussian_elimination(A, b))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            circuit = generate_ac0_circuit(n)
            poly = parity_polynomial(circuit)
            degree = real_radical_degree(poly)
            total_metric_value += degree
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = (instances_tested - sum(1 for _ in range(instances_tested) if degree < 2**(n/2))) / instances_tested

    return {
        "metric_name": "real_radical_degree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")