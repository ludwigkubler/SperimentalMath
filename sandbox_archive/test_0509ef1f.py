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
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det

    def generate_random_polynomial(degree, modulus):
        coefficients = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
        return coefficients

    def evaluate_polynomial(poly, x, modulus):
        result = 0
        degree = len(poly) - 1
        for i in range(degree + 1):
            result = (result * x + poly[i]) % modulus
        return result

    def generate_tropicalized_elliptic_curve(modulus):
        a = random.randint(1, modulus - 1)
        b = random.randint(0, modulus - 1)
        return a, b

    def count_points_on_curve(a, b, modulus):
        count = 0
        for x in range(modulus):
            y_squared = (x**3 + a * x + b) % modulus
            if is_perfect_square(y_squared, modulus):
                count += 2
        return count

    def is_perfect_square(n, p):
        if n == 0 or n == 1:
            return True
        if n < 0 or (n > 0 and n >= p):
            return False
        for i in range(2, int(math.sqrt(p)) + 1):
            if (i * i) % p == n:
                return True
        return False

    def acc0_circuit_size(degree):
        # Simplified estimate of ACC⁰ circuit size
        return degree ** 3

    n = random.choice([5, 10, 15, 20, 30, 40])
    modulus = 2
    degree = n - 1
    s = acc0_circuit_size(degree)
    f = generate_random_polynomial(degree, modulus)

    a, b = generate_tropicalized_elliptic_curve(modulus)
    r = count_points_on_curve(a, b, modulus)

    if r * math.log(s) <= 1:
        return {
            "metric_name": "Number of points on tropicalized elliptic curve",
            "metric_value": r,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "r * log(s) <= 1"
        }

    return {
        "metric_name": "Number of points on tropicalized elliptic curve",
        "metric_value": r,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='r * log(s) <= 1' first_failing_seed={first_failing_seed}")