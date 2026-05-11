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

def continued_fraction_approximation(x, max_denominator):
    if x == 0 or x == 1:
        return (x, 1)
    p0, q0 = 0, 1
    p1, q1 = 1, 1
    while True:
        a = int(x)
        f = x - a
        if f == 0:
            break
        p2 = a * p1 + p0
        q2 = a * q1 + q0
        if q2 > max_denominator:
            return (p1, q1)
        p0, p1 = p1, p2
        q0, q1 = q1, q2
        x = 1 / f
    return (p1, q1)

def fourier_coefficients(f, n):
    coeffs = [0] * (n // 2 + 1)
    for i in range(n):
        for j in range(n):
            if f[i // 2][j // 2] == (i ^ j) % 2:
                coeffs[(i & j) // 2] += 1
    return [c / n**2 for c in coeffs]

def randomized_discrepancy_estimator(f, n):
    m = 100 * n
    D = 0
    for _ in range(m):
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        D += abs(f[x][y] - f[(x + 1) % n][(y + 1) % n])
    return D / (2 * m)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    c = 1.0  # Constant for the inequality

    def xor_function(x, y):
        return [x[i] ^ y[i] for i in range(n)]

    def fourier_approximation_error(coeffs):
        max_error = 0
        for coeff in coeffs:
            approx_coeff = continued_fraction_approximation(coeff * n**2, n**2)
            max_error = max(max_error, abs(coeff - approx_coeff[0] / approx_coeff[1]))
        return max_error

    def communication_discrepancy(f):
        return randomized_discrepancy_estimator(f, n)

    f = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    coeffs = fourier_coefficients(f, n)
    epsilon_f = fourier_approximation_error(coeffs)
    D_f = communication_discrepancy(xor_function)

    if D_f < c / epsilon_f * math.log(n):
        return {
            "metric_name": "communication_discrepancy",
            "metric_value": D_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "D(f) < c/ε(f) · log n"
        }
    else:
        return {
            "metric_name": "communication_discrepancy",
            "metric_value": D_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"D(f) < c/ε(f) · log n\" first_failing_seed={first_failing_seed}")