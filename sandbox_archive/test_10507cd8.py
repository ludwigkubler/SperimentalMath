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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b//a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Inverse doesn\'t exist')
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError('Matrices cannot be multiplied')

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C

def matrix_add(A, B):
    rows = len(A)
    cols = len(A[0])

    if rows != len(B) or cols != len(B[0]):
        raise ValueError('Matrices cannot be added')

    C = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]

    return C

def matrix_subtract(A, B):
    rows = len(A)
    cols = len(A[0])

    if rows != len(B) or cols != len(B[0]):
        raise ValueError('Matrices cannot be subtracted')

    C = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]

    return C

def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    T = [[matrix[j][i] for j in range(rows)] for i in range(cols)]

    return T

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * matrix[0][c] * sub_det
        return det

def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError('Matrix is not invertible')
    adjugate = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            cofactor = ((-1) ** (i+j)) * determinant(minor)
            row.append(cofactor)
        adjugate.append(row)
    inv_matrix = [[adjugate[j][i] / det for j in range(len(matrix))] for i in range(len(matrix))]
    return inv_matrix

def secant_variety_dimension(n):
    # Generate the disjointness matrix
    M = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    # Compute the rank of M
    rank_M = len([row for row in M if any(row)])
    
    # The dimension of the secant variety of the rank locus is at least n - rank(M)
    return max(0, n - rank_M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        dimension = secant_variety_dimension(n)
        metric_values.append(dimension)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(value >= n for value, n in zip(metric_values, n_values))
    counterexample = "" if conjecture_holds else f"n={min(n_values)}, dim={min(metric_values)}"
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={min(n_values)}, dim={min(metric_values)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")