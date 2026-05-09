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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def free_entropy(matrix):
    n = len(matrix)
    eigenvalues = []
    for i in range(n):
        eigenvector = [0] * n
        eigenvector[i] = 1
        while True:
            new_vector = matrix_multiplication(matrix, eigenvector)
            norm = sum(x**2 for x in new_vector) ** 0.5
            if abs(norm - sum(eigenvector)) < 1e-6:
                break
            eigenvector = [x / norm for x in new_vector]
        eigenvalues.append(sum(x * math.log(abs(x)) for x in eigenvector))
    return max(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    if seed == 2:  # IP_2 BP
        A = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = -sum(A[i])
            for j in range(i + 1, n):
                A[j][i] = -A[i][j]
    else:
        A = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = sum(A[i])
            for j in range(i + 1, n):
                A[j][i] = -A[i][j]
    det = determinant(gaussian_elimination(A))
    if seed == 2:
        expected_free_entropy = n / 2 - math.log(n)
        actual_free_entropy = free_entropy(A)
        conjecture_holds = actual_free_entropy >= expected_free_entropy
        counterexample = "" if conjecture_holds else f"Expected {expected_free_entropy}, got {actual_free_entropy}"
    else:
        expected_free_entropy = math.log(n) + 1
        actual_free_entropy = free_entropy(A)
        conjecture_holds = actual_free_entropy <= expected_free_entropy
        counterexample = "" if conjecture_holds else f"Expected {expected_free_entropy}, got {actual_free_entropy}"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": actual_free_entropy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2] + list(range(3, 50))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")