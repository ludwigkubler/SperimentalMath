# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

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
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n+1):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    return [b[i]/A[i][i] if A[i][i] != 0 else None for i in range(n)]

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_sub(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1)**(c % 2)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def matrix_inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    adjoint = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1)**(i+j)
            adjoint[j][i] = sign * determinant(submatrix)
    return matrix_multiply(adjoint, Fraction(1, det_A))

def matroid_rank(circuit):
    n = len(circuit)
    rank_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if circuit[i][j] == 1:
                rank_matrix[i][j] = 1
                rank_matrix[j][i] = 1
    return len(gaussian_elimination(rank_matrix, [0]*(n+1)))

def tropical_hodge_dimension(circuit):
    n = matroid_rank(circuit)
    # Placeholder for actual computation of thd(C)
    return n

def communication_complexity_rank_variance(circuit):
    n = len(circuit)
    rank_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if circuit[i][j] == 1:
                rank_matrix[i][j] = 1
                rank_matrix[j][i] = 1
    return sum(sum(row) for row in rank_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    thd_values = []
    rcv_values = []
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):
            circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            if len(circuit) != n or any(len(row) != n for row in circuit):
                continue
            thd = tropical_hodge_dimension(circuit)
            rcv = communication_complexity_rank_variance(circuit)
            thd_values.append(thd)
            rcv_values.append(rcv)
            instances_tested += 1
    
    if not thd_values or not rcv_values:
        return {
            "metric_name": "thd vs rcv",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_thd = sum(thd_values) / len(thd_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    std_rcv = math.sqrt(sum((x - mean_rcv)**2 for x in rcv_values) / len(rcv_values))
    correlation_coefficient = (sum((thd_values[i] - mean_thd) * (rcv_values[i] - mean_rcv) for i in range(len(thd_values))) /
                                (len(thd_values) * std_rcv * math.sqrt(sum((x - mean_thd)**2 for x in thd_values))))
    
    return {
        "metric_name": "thd vs rcv",
        "metric_value": correlation_coefficient,
        "instances_tested": len(thd_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")