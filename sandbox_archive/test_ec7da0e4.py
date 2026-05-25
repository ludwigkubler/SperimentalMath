# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import sys
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_minor(A, row, col):
        minor = []
        for i in range(len(A)):
            if i == row:
                continue
            new_row = []
            for j in range(len(A[0])):
                if j == col:
                    continue
                new_row.append(A[i][j])
            minor.append(new_row)
        return minor
    
    def degree_of_minor(minor):
        m, n = len(minor), len(minor[0])
        for i in range(m):
            for j in range(n):
                if minor[i][j] != 0:
                    return max(i + 1, j + 1)
        return 0
    
    def order_of_vanishing(f, x=0):
        h = 1
        while True:
            value = f(x + h) - f(x)
            if abs(value) < 1e-9:
                return Fraction(1, h).limit_denominator()
            h *= 2
    
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n+1)]
        return lambda x: sum(c * x**i for i, c in enumerate(coefficients))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_polynomial(n)
    A = [[f(i + j) for j in range(n)] for i in range(n)]
    A = gaussian_elimination(A)
    
    min_order = float('inf')
    for i in range(n):
        for j in range(n):
            minor = matrix_minor(A, i, j)
            degree = degree_of_minor(minor)
            if degree > 0:
                min_order = min(min_order, degree)
    
    order_vanishing = order_of_vanishing(f)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": n * n,
        "conjecture_holds": min_order >= order_vanishing,
        "counterexample": "" if min_order >= order_vanishing else f"Function with ACC⁰ circuit size {n} has a minor of degree less than the order of vanishing at 0."
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")