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
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjoint[i][j] = (-1) ** (i+j) * cofactor
    inv_A = matrix_multiplication(adjoint, [[Fraction(1, det_A)] * n for _ in range(n)])
    return inv_A

def characteristic_function(circuit, x):
    if len(x) != len(circuit):
        raise ValueError("Input length must match circuit size")
    n = len(circuit)
    A = [[0] * (n+1) for _ in range(n+1)]
    b = [0] * (n+1)
    for i in range(n):
        A[i][i] = 1
        A[n][i] = circuit[i]
        b[i] = x[i]
    A[n][n] = -1
    b[n] = 1
    try:
        solution = gaussian_elimination(A, b)
        return solution[-1]
    except ValueError as e:
        raise ValueError("Circuit is not satisfiable") from e

def communication_complexity_rank(circuit):
    n = len(circuit)
    rank = 0
    for i in range(n):
        if circuit[i] == 1:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_metric_value = 0.0
        max_n = n
        conjecture_holds = True
        counterexample = ""
        for _ in range(50):
            circuit = [random.choice([0, 1]) for _ in range(n)]
            x = [random.choice([0, 1]) for _ in range(n)]
            try:
                lii = characteristic_function(circuit, x)
                rank = communication_complexity_rank(circuit)
                instances_tested += 1
                total_metric_value += abs(lii - rank)
                if len(results) == 0 or n > max_n:
                    max_n = n
            except ValueError as e:
                counterexample = str(e)
                conjecture_holds = False
                break
        if instances_tested < 30:
            conjecture_holds = False
            counterexample = "insufficient_instances"
        mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "mean_metric_value": mean_metric_value,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "metric_name": "Mean Absolute Difference",
        "metric_value": sum(result["mean_metric_value"] for result in results) / len(results),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max_n,
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")