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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_subtract(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_transpose(A):
    m = len(A)
    n = len(A[0])
    C = [[A[j][i] for j in range(m)] for i in range(n)]
    return C

def determinant(A):
    if len(A) == 1 and len(A[0]) == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def inverse(A):
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    m, n = len(A), len(A[0])
    adjoint = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjoint[j][i] = cofactor * (-1) ** (i + j)
    return matrix_multiply(adjoint, Fraction(1, det))

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    rref = gaussian_elimination(A)
    m, n = len(rref), len(rref[0])
    rank = 0
    for i in range(m):
        if any(rref[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def xor_and_circuit(n):
    if n == 1:
        return [[0], [1]]
    left = xor_and_circuit(n // 2)
    right = xor_and_circuit(n - n // 2)
    circuit = []
    for a in left:
        for b in right:
            circuit.append([a[0] ^ b[0]])
            circuit.append([a[0] & b[0]])
            circuit.append([a[0] ^ b[1]])
            circuit.append([a[0] & b[1]])
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 4) * 5
    if n < 5 or n > 40:
        return {
            "metric_name": "Minimal Rank of Monodromy Representations",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }
    circuit = xor_and_circuit(n)
    rank_value = rank(circuit)
    return {
        "metric_name": "Minimal Rank of Monodromy Representations",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value <= n**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")