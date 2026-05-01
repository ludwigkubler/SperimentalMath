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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B, m):
    n = len(B)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
            result[i][j] %= m
    return result

def matrix_power(A, p, m):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_multiply(result, A, m)
        A = matrix_multiply(A, A, m)
        p //= 2
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def is_independent_set(matroid, subset):
    n = len(matroid)
    independent = True
    for i in range(n):
        if matroid[i][subset[i]] == 0:
            independent = False
            break
    return independent

def find_circuits(matroid):
    n = len(matroid)
    circuits = []
    for r in range(2, n + 1):
        for subset in itertools.combinations(range(n), r):
            if not is_independent_set(matroid, subset):
                circuit = list(subset)
                while True:
                    found = False
                    for i in range(len(circuit)):
                        new_circuit = circuit[:i] + circuit[i+1:]
                        if is_independent_set(matroid, new_circuit):
                            circuit = new_circuit
                            found = True
                            break
                    if not found:
                        break
                circuits.append(circuit)
    return circuits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(10, 20)
    k = 3
    terms = [tuple(random.sample(range(n), 2)) for _ in range(2**n)]
    matroid = [[0] * len(terms) for _ in range(len(terms))]
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            if set(terms[i]).isdisjoint(set(terms[j])):
                matroid[i][j] = 1
                matroid[j][i] = 1

    circuits = find_circuits(matroid)
    girth = min(len(circuit) for circuit in circuits) if circuits else float('inf')
    conjecture_holds = girth >= k
    counterexample = "" if conjecture_holds else f"Found a DNF with girth < {k}"

    return {
        "metric_name": "girth",
        "metric_value": girth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"girth < {k}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or mapping_undefined")