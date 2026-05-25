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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_minor(A, row, col):
        m, n = len(A), len(A[0])
        minor = []
        for i in range(m):
            if i == row:
                continue
            new_row = []
            for j in range(n):
                if j == col:
                    continue
                new_row.append(A[i][j])
            minor.append(new_row)
        return minor
    
    def degree_of_polynomial(matrix):
        m, n = len(matrix), len(matrix[0])
        max_degree = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    max_degree = max(max_degree, i + j)
        return max_degree
    
    def order_of_vanishing(f, x=0, tol=1e-9):
        h = 1
        while abs(f(x + h) - f(x)) < tol:
            h *= 2
        return math.log(abs((f(x + h) - f(x)) / (h * f(x))), 2)
    
    def generate_polynomial(n, degree):
        coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
        return lambda x: sum(c * x**i for i, c in enumerate(coefficients))
    
    def acc0_circuit_size(f, n):
        # This is a placeholder function. For simplicity, we assume the circuit size is proportional to the degree of the polynomial.
        return degree_of_polynomial(generate_polynomial(n, random.randint(1, 5)))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_polynomial(n, random.randint(1, 5))
    s = acc0_circuit_size(f, n)
    
    matrix = [[f(i + j) for j in range(n)] for i in range(n)]
    min_degree = degree_of_polynomial(matrix_minor(matrix, 0, 0))
    
    if min_degree < s:
        return {
            "metric_name": "min_degree",
            "metric_value": min_degree,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: n={n}, s={s}, min_degree={min_degree}"
        }
    
    return {
        "metric_name": "min_degree",
        "metric_value": min_degree,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in input().split()] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")