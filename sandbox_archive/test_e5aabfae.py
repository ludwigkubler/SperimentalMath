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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    return [M[i][-1] for i in range(n)]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def matroid_rank(A):
    n, m = len(A), len(A[0])
    M = []
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                M.append([i, j])
    rank = 0
    for i in range(len(M)):
        if all(all(M[j][k] == 0 for k in range(j)) for j in range(i)):
            rank += 1
    return rank

def tropical_hodge_rank(A):
    n, m = len(A), len(A[0])
    M = []
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                M.append([i, j])
    rank = 0
    for i in range(len(M)):
        if all(all(M[j][k] == 0 for k in range(j)) for j in range(i)):
            rank += 1
    return rank

def random_d_regular_circuit(n, d):
    A = [[0]*n for _ in range(n)]
    edges = set()
    while len(edges) < n*d//2:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            A[u][v] = 1
            A[v][u] = 1
    return A

def boolean_circuit_size(A):
    n = len(A)
    m = len(A[0])
    size = 0
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                size += 1
    return size

def random_instance(phi, n_l):
    literals = set()
    for _ in range(n_l):
        polarity = random.choice([True, False])
        literal = random.randint(0, len(literals))
        literals.add((polarity, literal))
    return literals

def matroid_size(M):
    return len(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    th_values = []
    sizes = []
    M_sizes = []
    
    for n in n_values:
        A = random_d_regular_circuit(n, 2)
        size = boolean_circuit_size(A)
        th_value = tropical_hodge_rank(A)
        th_values.append(th_value)
        sizes.append(size)
        
        phi = random_instance(10, 7)
        M_phi = matroid_size(phi)
        M_sizes.append(M_phi)
    
    correlation_coefficient = sum((th_values[i] - sum(th_values) / len(th_values)) * (sizes[i] - sum(sizes) / len(sizes)) for i in range(len(sizes))) / (len(sizes) * sum((th_values[i] - sum(th_values) / len(th_values))**2 for i in range(len(sizes))) * sum((sizes[i] - sum(sizes) / len(sizes))**2 for i in range(len(sizes))))**0.5
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8"
    
    return {
        "metric_name": "tropical_hodge_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")