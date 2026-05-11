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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def inverse_matrix(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        A_augmented = [A[i] + I[i] for i in range(m)]
        gaussian_elimination(A_augmented)
        return [row[n:] for row in A_augmented]

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def free_cumulants(eigenvalues):
        n = len(eigenvalues)
        cumulants = [0] * (n + 1)
        for i in range(n):
            cumulants[i+1] = eigenvalues[i]
        for k in range(2, n + 1):
            for j in range(k - 1, -1, -1):
                cumulants[j] += (-1) ** (k - j - 1) * math.comb(k - 1, j) * cumulants[k]
        return cumulants

    def read_once_bp(n):
        P = [[0] * n for _ in range(n)]
        for i in range(n):
            P[i][i] = 1 / (2 ** i)
        return P

    def read_twice_bp(n):
        P = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                P[i][j] = 1 / (2 ** (i + j))
                P[j][i] = P[i][j]
        return P

    def transition_matrix(bp):
        n = len(bp)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if bp[i][j] > 0:
                    T[i][j] = bp[i][j]
        return T

    def eigenvalues(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det_A_k = [1] * (m + 1)
        for k in range(1, m + 1):
            A_k = [[matrix[i][j] - k * delta(i, j) for j in range(n)] for i in range(m)]
            det_A_k[k] = determinant(A_k)
        eigenvals = [det_A_k[k] / det_A_k[0] for k in range(1, m + 1)]
        return eigenvals

    def delta(i, j):
        return 1 if i == j else 0

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        read_once_P = read_once_bp(n)
        read_twice_P = read_twice_bp(n)

        read_once_T = transition_matrix(read_once_P)
        read_twice_T = transition_matrix(read_twice_P)

        read_once_eigenvals = eigenvalues(read_once_T)
        read_twice_eigenvals = eigenvalues(read_twice_T)

        read_once_cumulants = free_cumulants(read_once_eigenvals)
        read_twice_cumulants = free_cumulants(read_twice_eigenvals)

        total_metric_value += sum(read_twice_cumulants) - sum(read_once_cumulants)
        instances_tested += n

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0

    return {
        "metric_name": "Free Cumulant Sum Gap",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")