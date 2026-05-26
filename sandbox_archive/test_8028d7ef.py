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
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def identity_matrix(n):
        I = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        return I
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def minimal_index_of_entanglement(state):
        n = len(state)
        identity = identity_matrix(n)
        A = matrix_multiplication(state, state) - identity
        eigenvalues = []
        for i in range(100):  # Perform a few iterations of Gaussian elimination to approximate eigenvalues
            b = [random.random() for _ in range(n)]
            x = gaussian_elimination(A, b)
            lambda_i = sum(x[j] * state[j][i] for j in range(n))
            eigenvalues.append(abs(lambda_i))
        return min(eigenvalues) if eigenvalues else float('inf')
    
    def degree_of_first_nonzero_eigenvalue(state):
        n = len(state)
        identity = identity_matrix(n)
        A = matrix_multiplication(state, state) - identity
        eigenvalues = []
        for i in range(100):  # Perform a few iterations of Gaussian elimination to approximate eigenvalues
            b = [random.random() for _ in range(n)]
            x = gaussian_elimination(A, b)
            lambda_i = sum(x[j] * state[j][i] for j in range(n))
            eigenvalues.append(abs(lambda_i))
        nonzero_eigenvalues = [lambda_ for lambda_ in eigenvalues if lambda_ > 1e-6]
        return min(nonzero_eigenvalues) if nonzero_eigenvalues else float('inf')
    
    state = [[random.random() for _ in range(4)] for _ in range(4)]
    min_index = minimal_index_of_entanglement(state)
    degree = degree_of_first_nonzero_eigenvalue(state)
    
    return {
        "metric_name": "Ratio of Minimal Index to Eigenvalue Degree",
        "metric_value": min_index / (degree + 1e-6),
        "instances_tested": 1,
        "conjecture_holds": min_index <= degree,
        "counterexample": "" if min_index <= degree else "Mapping undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=All trials used n=1")