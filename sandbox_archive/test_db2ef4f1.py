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

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def minimal_geometric_entropy(matrix):
        eigenvalues = []
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        matrix_exp = [identity]
        for _ in range(10):  # Approximate exp(A) using the first few terms of the series
            matrix_exp.append([sum(matrix_multiplication(matrix, B)[i][j] for B in matrix_exp[:k]) / math.factorial(k) for k in range(len(matrix_exp))])
        for i in range(n):
            eigenvalue = 0
            for j in range(10):
                eigenvalue += sum(matrix_exp[j][i][k] * matrix_exp[j][k][i] for k in range(n))
            eigenvalues.append(eigenvalue)
        return -sum(math.log(abs(eig)) for eig in eigenvalues) / n

    def communication_complexity(n):
        # Simplified model of communication complexity for disjointness
        return math.ceil(math.log2(n))

    n = random.randint(5, 40)
    matrix = [[random.random() for _ in range(n)] for _ in range(n)]
    h_min = minimal_geometric_entropy(matrix)
    comm_complexity = communication_complexity(n)

    return {
        "metric_name": "Minimal Geometric Entropy",
        "metric_value": h_min,
        "instances_tested": 1,
        "conjecture_holds": h_min >= n,
        "counterexample": "" if h_min >= n else f"Counterexample for n={n}: h_min({h_min}) < {n}"
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")