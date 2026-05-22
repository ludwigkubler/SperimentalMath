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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def resultant(poly1, poly2):
    n = len(poly1) - 1
    m = len(poly2) - 1
    if n < m:
        poly1, poly2 = poly2, poly1
        n, m = m, n
    R = [[0] * (n + m + 1) for _ in range(n + m + 1)]
    for i in range(m + 1):
        R[i][i] = poly1[0]
        R[n + m - i][m - i] = poly2[0]
    for k in range(1, n + m + 1):
        for i in range(k - m, min(k, n) + 1):
            R[k][i] = poly1[i] * R[k-1][i-1] - poly1[i-1] * R[k-1][i]
    return determinant(R)

def characteristic_polynomial(dnf_formula):
    n = len(dnf_formula)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if dnf_formula[i][j]:
                A[i][j] = -1
            else:
                A[i][j] = 1
        A[i][n] = 1
    return resultant([Fraction(1), Fraction(-sum(A[i][i] for i in range(n)))], [Fraction(1)] + [-A[0][i] for i in range(1, n+1)])

def min_tropical_discriminant(poly):
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if poly[i][j]:
                A[i][j] = -1
            else:
                A[i][j] = 1
        A[i][n] = 1
    det = determinant(A)
    return det

def generate_dnf_formula(n, k):
    dnf_formula = [[False] * n for _ in range(n)]
    for i in range(k):
        indices = random.sample(range(n), 2)
        dnf_formula[indices[0]][indices[1]] = True
        dnf_formula[indices[1]][indices[0]] = True
    return dnf_formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_discriminants = []
    for n in n_values:
        instances_tested = 0
        for _ in range(5):
            dnf_formula = generate_dnf_formula(n, k)
            poly = characteristic_polynomial(dnf_formula)
            discriminant = min_tropical_discriminant(poly)
            if discriminant != 0:
                total_discriminants.append(discriminant)
                instances_tested += 1
    mean_value = sum(total_discriminants) / len(total_discriminants)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in total_discriminants) / len(total_discriminants))
    conjecture_holds = all(d >= n**(3/2) for d in total_discriminants)
    counterexample = "" if conjecture_holds else "n^1.5"
    return {
        "metric_name": "min_tropical_discriminant",
        "metric_value": mean_value,
        "instances_tested": len(total_discriminants),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")