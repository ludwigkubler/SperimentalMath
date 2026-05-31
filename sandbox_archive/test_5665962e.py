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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def resolution_width(cnf):
    clauses = list(cnf)
    n = len(clauses)
    width = 0
    for i in range(n):
        for j in range(i+1, n):
            if -clauses[i][0] in clauses[j]:
                width = max(width, len(set(clauses[i]) | set(clauses[j])))
    return width

def hyperbolic_metric_entropy(G):
    n = len(G)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in G[u]:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
    laplacian_matrix = [[0] * n for _ in range(n)]
    degree_sum = sum(sum(row) for row in adjacency_matrix)
    for i in range(n):
        laplacian_matrix[i][i] = degree_sum - 2 * sum(adjacency_matrix[i])
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[j][i]
    eigenvalues = []
    for _ in range(n):
        largest_eigenvalue = float('-inf')
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        for _ in range(100):
            Av = matrix_multiplication(laplacian_matrix, v)
            Av /= max(abs(x) for x in Av)
            v = Av
            largest_eigenvalue = max(largest_eigenvalue, abs(v[0]))
        eigenvalues.append(largest_eigenvalue)
    return sum(math.log(eig) / n for eig in eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_metric_value = 0
        max_n = n
        conjecture_holds = True
        counterexample = ""
        for _ in range(5):
            m = random.randint(n, 2*n)
            cnf = {i: set(random.sample(range(-n, n+1), random.randint(1, n))) for i in range(m)}
            G = {i: [] for i in range(n)}
            for clause in cnf.values():
                for literal in clause:
                    if literal > 0:
                        G[literal-1].append(literal-n)
                        G[literal+n-1].append(-literal+1)
                    else:
                        G[-literal-1].append(-literal+n)
                        G[-literal+n-1].append(literal+1)
            metric_value = hyperbolic_metric_entropy(G)
            width = resolution_width(cnf)
            if width == 0:
                continue
            instances_tested += 1
            total_metric_value += metric_value / width
            max_n = max(max_n, n)
            if metric_value / width < 0.5:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}"
        results.append({
            "metric_name": "H(G(φ)) / w(φ)",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["results"])
    metric_values = [r[0]["metric_value"] for r in results for r in r]
    support_fraction = sum(1 for r in results for r in r if r[0]["conjecture_holds"]) / len(results)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) for r in result if not r[0]["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result[0]['counterexample']}\" first_failing_seed={first_failing_seed}")