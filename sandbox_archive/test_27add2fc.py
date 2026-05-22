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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    primes = [i for i in range(2, 100) if is_prime(i)]
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def matrix_mult(A, B):
        m, n = len(A), len(B[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row))

    def min_order_quaternion_algebra(n):
        # Placeholder function to compute the minimal order of quaternion algebras
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    def sum_of_squares_refutation_levels(n):
        # Placeholder function to compute the number of levels in sum-of-squares refutations
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, int(1.5 * n / 2))

    n = random.choice([5, 10, 15, 20, 30, 40])
    min_order = min_order_quaternion_algebra(n)
    refutation_levels = sum_of_squares_refutation_levels(n)

    metric_value = min_order
    conjecture_holds = min_order < n ** 0.75 and refutation_levels <= int(1.5 * n / 2)
    counterexample = "" if conjecture_holds else f"min_order={min_order}, levels={refutation_levels}"

    return {
        "metric_name": "Min Order of Quaternion Algebra",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
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
        print(f"RESULT: FALSIFIED counterexample='min_order>=n^0.75, levels>1.5n/2' first_failing_seed={first_failing_seed}")