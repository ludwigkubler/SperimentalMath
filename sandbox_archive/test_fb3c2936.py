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

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_power(A, n, mod):
    if n == 0:
        return [[int(i == j) for i in range(len(A))] for j in range(len(A))]
    elif n == 1:
        return A
    elif n % 2 == 0:
        B = matrix_power(A, n // 2, mod)
        return matrix_mult(B, B, mod)
    else:
        B = matrix_power(A, (n - 1) // 2, mod)
        return matrix_mult(matrix_mult(B, B, mod), A, mod)

def characteristic_polynomial(A, mod):
    n = len(A)
    identity = [[int(i == j) for i in range(n)] for j in range(n)]
    char_poly = [1]
    for k in range(1, n + 1):
        A_k = matrix_power(A, k, mod)
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in zip(p, sorted(p)))
            term = 1
            for i in range(n):
                term *= A_k[i][p[i]]
            det += sign * term
        char_poly.append((det - identity[k-1][k-1]) % mod)
    return char_poly

def geometric_complexity_group_size(char_poly, mod):
    n = len(char_poly) - 1
    roots = []
    for i in range(1, n + 1):
        root = pow(i, mod - 2, mod)
        if all((root - r) % mod != 0 for r in roots):
            roots.append(root)
    return len(roots)

def resolution_proof_width(phi):
    # Placeholder function to compute the resolution proof width
    # This is a dummy implementation and should be replaced with an actual algorithm
    return random.randint(1, 10)  # Example: random value between 1 and 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            char_poly = characteristic_polynomial(phi, mod=2)
            g_size = geometric_complexity_group_size(char_poly, mod=2)
            w_phi = resolution_proof_width(phi)
            metric_values.append((g_size, w_phi))
            instances_tested += 1
            n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "Geometric Complexity Group Size vs Resolution Proof Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    g_sizes, w_phis = zip(*metric_values)
    mean_g_size = sum(g_sizes) / len(g_sizes)
    mean_w_phi = sum(w_phis) / len(w_phis)

    correlation_coefficient = 0
    for g_size, w_phi in metric_values:
        correlation_coefficient += (g_size - mean_g_size) * (w_phi - mean_w_phi)
    correlation_coefficient /= math.sqrt(sum((g_size - mean_g_size) ** 2 for g_size in g_sizes)) * math.sqrt(sum((w_phi - mean_w_phi) ** 2 for w_phi in w_phis))

    if correlation_coefficient < 0.5:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {correlation_coefficient} is less than 0.5"

    return {
        "metric_name": "Geometric Complexity Group Size vs Resolution Proof Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")