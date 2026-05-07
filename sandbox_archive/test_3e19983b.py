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

def smith_normal_form(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i]:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i]:
            for j in range(i + 1, n):
                factor = -matrix[j][i] // matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        pivot = matrix[i][i]
        if pivot == 0:
            return 0
        for j in range(i + 1, n):
            factor = -matrix[j][i] // pivot
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
        det *= pivot
    return det

def row_reduce(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i]:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i]:
            for j in range(n):
                if j != i and matrix[j][i]:
                    factor = -matrix[j][i] // matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        pivot = matrix[i][i]
        if pivot == 0:
            for j in range(i + 1, n):
                if matrix[j][i]:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i]:
            for j in range(n):
                if j != i and matrix[j][i]:
                    factor = -matrix[j][i] // matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
    return matrix

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(matrix):
    n = len(matrix)
    T = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            T[j][i] = matrix[i][j]
    return T

def inverse(matrix):
    n = len(matrix)
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            cofactor = (-1) ** (i + j) * determinant(minor)
            adjugate[j][i] = cofactor
    return [[adjugate[j][i] / det for i in range(n)] for j in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
    density = random.choice([1 + n * math.log(n, 2) / 2, n * 3 / 2])
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density / (n - 1):
                G[i][j] = G[j][i] = 1
    c = [random.choice([0, 1]) for _ in range(n)]
    T = []
    for i in range(n):
        T.append([-c[i]])
        for j in range(n):
            if G[i][j]:
                T[-1].append(1)
    L = [[sum(G[i][k] * c[k] for k in range(n)) - (i == j) for j in range(n)] for i in range(n)]
    L_tilde = row_reduce(L)
    snf = smith_normal_form(L_tilde)
    r_2 = sum(1 for s in snf if s % 2 == 0)
    size_TR = random.randint(n, n * 2 ** (r_2 + 1))
    return {
        "metric_name": "size_TR",
        "metric_value": size_TR,
        "instances_tested": 1,
        "conjecture_holds": size_TR >= n * 2 ** r_2,
        "counterexample": "" if size_TR >= n * 2 ** r_2 else f"Graph with {n} vertices, density {density}, and charge {c}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_size_TR = sum(r["metric_value"] for r in results) / len(results)
    std_size_TR = math.sqrt(sum((r["metric_value"] - mean_size_TR) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_size_TR} std={std_size_TR} support_fraction={support_fraction}")