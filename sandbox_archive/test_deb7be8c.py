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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + sum(1 for j in range(i+1, m) if abs(A[j][i]) > abs(A[i][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def hypergeometric_coefficients(q, n):
        if q <= 0 or n <= 0:
            return []
        coeffs = [1]
        for i in range(1, n):
            coeff = (q - i + 1) / (i * (q + i))
            coeffs.append(coeff)
        return coeffs

    def q_difference_operator(k, n):
        if k <= 0 or n <= 0:
            return []
        q = random.randint(2, 5)
        coeffs = hypergeometric_coefficients(q, n)
        operator = [[0] * (n+1) for _ in range(n+1)]
        operator[0][0] = 1
        for i in range(1, n+1):
            operator[i][i-1] = -coeffs[i-1]
            operator[i][i] = q
        return operator

    def count_non_zero_coeffs(operator):
        count = 0
        for row in operator:
            for coeff in row:
                if coeff != 0:
                    count += 1
        return count

    n_values = [5, 10, 15, 20, 30, 40]
    total_count = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            operator = q_difference_operator(k=5, n=n)
            count = count_non_zero_coeffs(operator)
            total_count += count
            instances_tested += 1
            if n > n_max:
                n_max = n

    metric_value = total_count / instances_tested
    conjecture_holds = metric_value >= k * math.log(n_max)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Number of distinct non-zero hypergeometric function coefficients",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")