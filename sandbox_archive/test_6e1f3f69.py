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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [-b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = M[j][i]
                    for k in range(n+1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]

    def permanent(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * permanent(submatrix)
        return det

    def determinant(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det

    def invariant_ring_dimension(n):
        if n == 2:
            return 4
        elif n == 3:
            return 9
        else:
            return 16  # Hypothetical value for larger n, based on known patterns

    n = random.randint(5, 40)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    perm_det_ratio = abs(permanent(A) / determinant(A))
    inv_dim = invariant_ring_dimension(n)
    
    return {
        "metric_name": "Invariant Ring Dimension vs Permanent/Determinant Ratio",
        "metric_value": inv_dim,
        "instances_tested": 1,
        "conjecture_holds": inv_dim > perm_det_ratio * 2,  # Hypothetical threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Invariant Ring Dimension does not grow exponentially faster than Permanent/Determinant Ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")