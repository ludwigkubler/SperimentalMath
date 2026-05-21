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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def inverse_matrix(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                I[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return I

    def sdp_relaxation(A, b):
        n = len(b)
        x = [Fraction(0, 1)] * n
        for _ in range(10):  # Simple DPLL-like relaxation
            changed = False
            for i in range(n):
                if A[i][i] == 0:
                    continue
                sum_val = sum(A[i][j] * x[j] for j in range(n) if j != i)
                if b[i] - sum_val > 0:
                    x[i] += (b[i] - sum_val) / A[i][i]
                    changed = True
            if not changed:
                break
        return max(x)

    def fourier_transform(F):
        n = len(F)
        F_hat = [Fraction(0, 1)] * n
        for k in range(n):
            for i in range(n):
                F_hat[k] += F[i] * Fraction(math.cos(2 * math.pi * i * k / n), 1) + \
                             Fraction(math.sin(2 * math.pi * i * k / n), 1)
        return F_hat

    def dual_norm(F_hat):
        return max(abs(coeff) for coeff in F_hat)

    random.seed(seed)
    n = random.randint(5, 40)
    G = [i for i in range(n)]
    A = [[random.choice(G) for _ in range(n)] for _ in range(n)]
    b = [random.choice(G) for _ in range(n)]

    F = [Fraction(1, 1)] * n
    for i in range(n):
        F[i] = Fraction(1, 1) if A[0][i] == A[1][i] else Fraction(-1, 1)

    F_hat = fourier_transform(F)
    refutation_degree = sdp_relaxation(A, b)
    max_F_hat = dual_norm(F_hat)

    return {
        "metric_name": "refutation_degree",
        "metric_value": refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": refutation_degree <= max_F_hat,
        "counterexample": "" if refutation_degree <= max_F_hat else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")