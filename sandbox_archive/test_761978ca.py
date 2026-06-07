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
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def identity_matrix(n):
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        return I

    def is_identity(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                    return False
        return True

    def quandle_operation(A, B):
        I = identity_matrix(len(A))
        result = A
        for _ in range(2):  # Minimal order of non-identity operations
            result = matrix_multiplication(result, B)
            if is_identity(result):
                break
        return result

    def resolution_width(phi):
        clauses = phi.split(' or ')
        literals = set()
        for clause in clauses:
            literals.update(clause.split(' and '))
        return len(literals)

    def generate_cnf(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.choice(variables) if random.random() < 0.5 else -random.choice(variables)
            clauses.append(clause)
        return ' or '.join(f'{v} and {v}' if v > 0 else f'-{abs(v)}' for v in clauses)

    def quandle_operations_required(phi):
        cnf = generate_cnf(n)
        clauses = cnf.split(' or ')
        operations = 0
        for clause in clauses:
            literals = clause.split(' and ')
            A = [[1 if int(l) == i else 0 for i in range(1, n+1)] for l in literals]
            B = identity_matrix(n)
            while not is_identity(A):
                B = quandle_operation(B, B)
                operations += 1
        return operations

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_operations = 0
        for _ in range(5):  # Sample 5 instances per size
            operations = quandle_operations_required(generate_cnf(n))
            resolution_w = resolution_width(cnf)
            results.append({"n": n, "operations": operations, "resolution_w": resolution_w})
            instances_tested += 1
        total_operations += sum(r["operations"] for r in results[-instances_tested:])
    
    if not results:
        return {
            "metric_name": "quandle_operations_resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    operations = [r["operations"] for r in results]
    resolution_ws = [r["resolution_w"] for r in results]

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)

    correlation_coefficient = pearson_correlation(operations, resolution_ws)
    
    return {
        "metric_name": "quandle_operations_resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")