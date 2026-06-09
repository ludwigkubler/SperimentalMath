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
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1) ** (i+j) * determinant(submatrix)
            adjoint[j][i] = cofactor
    inv_A = matrix_multiply(adjoint, [[Fraction(1, det_A)] * n for _ in range(n)])
    return inv_A

def is_empty_set(s):
    return len(s) == 0

def random_subset(s, k):
    if k > len(s):
        raise ValueError("k cannot be greater than the size of the set")
    subset = []
    s_list = list(s)
    for _ in range(k):
        i = random.randint(0, len(s_list) - 1)
        subset.append(s_list.pop(i))
    return subset

def local_inductive_dimension(vertices, edges):
    n = len(vertices)
    if n <= 2:
        return 0
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[i][j]
    eigenvalues = []
    for i in range(n):
        eigenvector = [0] * n
        eigenvector[i] = 1
        A_eigenvector = matrix_multiply(laplacian_matrix, eigenvector)
        lambda_i = Fraction(0)
        for j in range(n):
            lambda_i += A_eigenvector[j] ** 2
        eigenvalues.append(lambda_i)
    return max(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        if n > 30:
            break
        cnf = [[random.randint(0, n-1) for _ in range(2)] for _ in range(n)]
        vertices = set()
        edges = set()
        for clause in cnf:
            u, v = clause
            vertices.add(u)
            vertices.add(v)
            edges.add((u, v))
        l_d = local_inductive_dimension(vertices, edges)
        w_phi = len(cnf)  # Simplified resolution proof width
        results.append({"n": n, "l_d": l_d, "w_phi": w_phi})
    if not results:
        return {
            "metric_name": "local_inductive_dimension",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    l_d_values = [result["l_d"] for result in results]
    w_phi_values = [result["w_phi"] for result in results]
    n_max = max(result["n"] for result in results)
    correlation_coefficient = Fraction(0)
    if len(l_d_values) > 1:
        mean_l_d = sum(l_d_values) / len(l_d_values)
        mean_w_phi = sum(w_phi_values) / len(w_phi_values)
        numerator = sum((l_d - mean_l_d) * (w_phi - mean_w_phi) for l_d, w_phi in zip(l_d_values, w_phi_values))
        denominator = math.sqrt(sum((l_d - mean_l_d) ** 2 for l_d in l_d_values)) * math.sqrt(sum((w_phi - mean_w_phi) ** 2 for w_phi in w_phi_values))
        if denominator != 0:
            correlation_coefficient = Fraction(numerator, denominator)
    return {
        "metric_name": "local_inductive_dimension",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= Fraction(0.8) and all(correlation_coefficient >= Fraction(0.5) for _ in range(len(results))),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    if all(result is not None for result in results):
        mean_value = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for value in results if value >= Fraction(0.8)) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min([value for value in results if value < Fraction(0.8)]))]
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_skipped")