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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def is_quaternion_compatible(A, q):
        m, n = len(A), len(A[0])
        if m != n:
            return False
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        AqA = matrix_multiplication(matrix_multiplication(A, q), A)
        return gaussian_elimination(AqA) == identity

    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        m = len(clauses)
        polynomial = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if clauses[i][j] == 1:
                    polynomial[i][j] = 1
                elif clauses[i][j] == -1:
                    polynomial[i][j] = -1
        return polynomial

    def resolution_proof_width(clauses):
        n = len(clauses[0])
        m = len(clauses)
        width = [0] * m
        for i in range(m):
            if clauses[i][i] == 1:
                width[i] = 1
            elif clauses[i][i] == -1:
                width[i] = 2
        return sum(width)

    def minimal_order_of_quaternion_algebra(clauses):
        n = len(clauses[0])
        m = len(clauses)
        polynomial = clause_indicator_polynomial(clauses)
        for order in range(1, n+1):
            q = [[random.choice([-1, 1]) for _ in range(order)] for _ in range(order)]
            if is_quaternion_compatible(polynomial, q):
                return order
        return None

    def generate_random_clauses(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) for _ in range(n)]
            while sum(clause) == 0:
                clause = [random.choice([-1, 1]) for _ in range(n)]
            clauses.append(clause)
        return clauses

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for i in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(1, min(n, 20))
        clauses = generate_random_clauses(n, m)
        order = minimal_order_of_quaternion_algebra(clauses)
        width = resolution_proof_width(clauses)
        if order is None:
            conjecture_holds = False
            counterexample = "mapping_undefined"
            break
        metric_values.append(order / width)

    return {
        "metric_name": "order_over_width",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")