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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_sub(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def identity_matrix(n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return I

def transpose(A):
    m, n = len(A), len(A[0])
    B = [[A[j][i] for j in range(m)] for i in range(n)]
    return B

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

def inverse_matrix(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            minor = determinant(submatrix)
            adjoint[j][i] = minor * (-1) ** (i + j)
    inv_A = matrix_mul(adjoint, [[1 / det_A] * n for _ in range(n)])
    return inv_A

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    B = [row[:] for row in A]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(B[j][i]) > abs(B[max_row][i]):
                max_row = j
        B[i], B[max_row] = B[max_row], B[i]
        pivot = B[i][i]
        for j in range(n):
            B[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = B[j][i]
                for k in range(n):
                    B[j][k] -= factor * B[i][k]
    return B

def matrix_power(A, k):
    n = len(A)
    result = identity_matrix(n)
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul(result, A)
        A = matrix_mul(A, A)
        k //= 2
    return result

def symmetric_group(n):
    elements = []
    def permute(arr, start=0):
        if start == n:
            elements.append(arr[:])
        else:
            for i in range(start, n):
                arr[start], arr[i] = arr[i], arr[start]
                permute(arr, start + 1)
                arr[start], arr[i] = arr[i], arr[start]
    permute(list(range(n)))
    return elements

def noncommutative_fourier_coefficient(f, P, S_n):
    n = len(P)
    m = len(S_n)
    result = 0
    for sigma in S_n:
        f_sigma = sum(f(tuple(sigma[i] for i in range(len(sigma)))) for _ in range(2))
        result += abs(f_sigma / m)
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    f = lambda x: sum(x[i] * (i + 1) % 2 for i in range(n))
    IP_2 = lambda x: sum(x[i] * x[j] for i in range(n) for j in range(i+1, n)) % 2
    S_n = symmetric_group(n)
    
    f_coeff_sum = noncommutative_fourier_coefficient(f, P, S_n)
    IP_2_coeff_sum = noncommutative_fourier_coefficient(IP_2, P, S_n)
    
    metric_name = "Noncommutative Fourier Coefficient Sum"
    metric_value = f_coeff_sum
    instances_tested = 1
    conjecture_holds = f_coeff_sum <= math.log(n) and IP_2_coeff_sum >= n**2 / 4
    counterexample = "" if conjecture_holds else "IP_2 function has too small Fourier coefficients"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")