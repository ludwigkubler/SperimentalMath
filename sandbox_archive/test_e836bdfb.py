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

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def minimal_index(matrix):
        if not matrix:
            return 0
        n = len(matrix)
        identity = [[int(i == j) for i in range(n)] for j in range(n)]
        augmented_matrix = [row + [1] for row in matrix]
        reduced_row_echelon_form = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_row_echelon_form if any(row[i] != 0 for i in range(n)))
        return n - rank

    def characteristic_polynomial(matrix):
        n = len(matrix)
        identity = [[int(i == j) for i in range(n)] for j in range(n)]
        char_poly = [1]
        for k in range(1, n+1):
            A_k = matrix_multiply(matrix, matrix)
            char_poly.append(-sum(determinant(A_k[:k][:k]) for k in range(k)))
        return char_poly

    def AC0_circuit_complexity(char_poly):
        degree = len(char_poly) - 1
        depth = degree * 2
        size = (degree + 1) * (depth + 1)
        return depth, size

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            k = random.randint(1, 10)
            N = random.randint(1, 40)
            f = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            I_f = minimal_index(f)
            char_poly = characteristic_polynomial(f)
            h = AC0_circuit_complexity(char_poly)
            I_h = max(I_f, h[0], h[1])
            
            if I_h <= I_f:
                depth, size = h
                if depth < 2 * k or size < N:
                    return {
                        "metric_name": "AC0 Circuit Complexity",
                        "metric_value": I_h,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"Depth {depth} and Size {size} for n={n}, k={k}, N={N}"
                    }
    
    return {
        "metric_name": "AC0 Circuit Complexity",
        "metric_value": sum(I_f for _, I_f, _ in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > mean) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r <= mean for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")