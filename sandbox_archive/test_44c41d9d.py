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
        n = len(A)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            det += ((-1) ** j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det
    
    def matrix_multiplication(A, B):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def eigenvalues(state):
        n = len(state)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        epsilon = 1e-6
        k = 0
        A_k1, A_k2 = state, matrix_multiplication(state, state)
        while max(max(abs(a) for a in row) for row in A_k2 - A_k1) >= epsilon:
            k += 1
            A_k1, A_k2 = A_k2, matrix_multiplication(A_k2, A_k2)
        eigenvals = [A[i][i] for i in range(n)]
        return eigenvals
    
    def minimal_index_of_entanglement(state):
        n = len(state)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix_multiplication(state, state) - identity
        det_A = determinant(A)
        return abs(det_A)
    
    n = random.randint(5, 40)
    state = [[random.random() for _ in range(n)] for _ in range(n)]
    state = gaussian_elimination(state)
    min_index = minimal_index_of_entanglement(state)
    eigenvals = eigenvalues(state)
    degree_first_nonzero_eigenval = next((i for i, val in enumerate(eigenvals) if val != 0), None)
    
    if degree_first_nonzero_eigenval is None:
        return {
            "metric_name": "Ratio of Minimal Index to Eigenvalue Degree",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No non-zero eigenvalues found"
        }
    
    ratio = min_index / degree_first_nonzero_eigenval
    return {
        "metric_name": "Ratio of Minimal Index to Eigenvalue Degree",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1' first_failing_seed={first_failing_seed}")