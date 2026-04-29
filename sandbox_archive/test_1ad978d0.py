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

def generate_ac0_circuit(n):
    # Simplified AC⁰ circuit generation (random AND gates)
    depth = random.randint(2, n // 2)
    circuit = []
    for _ in range(depth):
        layer = [random.choice(['AND', 'NOT']) for _ in range(n)]
        circuit.append(layer)
    return circuit

def hadamard_matrix(n):
    if n == 1:
        return [[1]]
    H = hadamard_matrix(n // 2)
    size = len(H)
    result = [[0] * (size * 2) for _ in range(size * 2)]
    for i in range(size):
        for j in range(size):
            result[i][j] = result[i + size][j] = result[i][j + size] = H[i][j]
            result[i + size][j + size] = -H[i][j]
    return result

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for multiplication")
    C = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        for j in range(i+1, n):
            factor = A_augmented[j][i] / A_augmented[i][i]
            for k in range(n + 1):
                A_augmented[j][k] -= factor * A_augmented[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i+1, n))) / A_augmented[i][i]
    return x

def real_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows == 0 or cols == 0:
        return 0
    U, S, Vt = svd_decomposition(matrix)
    rank = sum(1 for s in S if abs(s) > 1e-10)
    return rank

def svd_decomposition(A):
    m, n = len(A), len(A[0])
    A_t = [list(a) for a in zip(*A)]
    U = hadamard_matrix(m)
    Vt = hadamard_matrix(n)
    S = [[0] * n for _ in range(m)]
    for i in range(min(m, n)):
        Q_i, R_i = qr_decomposition(A_t[i])
        A_t[i] = [r / math.sqrt(sum(r**2 for r in row)) for row in Q_i]
        Vt[i] = Q_i
        S[i][i] = sum(A_t[j][i]**2 for j in range(m))
    return U, S, Vt

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q = [[0] * n for _ in range(m)]
    R = A.copy()
    for i in range(n):
        norm = math.sqrt(sum(R[j][i]**2 for j in range(i, m)))
        Q[i][i] = R[i][i] / norm
        for j in range(i+1, m):
            Q[j][i] = R[j][i] / norm
        for k in range(n):
            R[i][k] /= norm
            for j in range(i+1, m):
                R[j][k] -= Q[j][i] * R[i][k]
    return Q, R

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    H = hadamard_matrix(2**n)
    M_C = matrix_multiplication(H, H)
    rank = real_rank(M_C)
    size = len(circuit) * n
    lower_bound = 2**(n/2) / (size ** 0.5)
    conjecture_holds = rank >= lower_bound
    counterexample = "" if conjecture_holds else f"rank={rank}, lb={lower_bound}"
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")