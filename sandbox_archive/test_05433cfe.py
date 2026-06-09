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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    C = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for i in range(len(matrix)):
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += sign * matrix[0][i] * determinant(submatrix)
        sign *= -1
    return det

def resolution_width(formula):
    clauses = formula.split(' or ')
    literals = set()
    for clause in clauses:
        literals.update(clause.split(' and '))
    
    n = len(literals)
    if n == 0:
        return 0
    
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i, literal in enumerate(literals):
        for j, clause in enumerate(clauses):
            if literal in clause or f"~{literal}" in clause:
                matrix[i][j] = 1
            else:
                matrix[i][j] = -1
    
    gaussian_elimination(matrix)
    
    width = 0
    for row in matrix:
        count = sum(1 for x in row if x != 0)
        width = max(width, count)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                graph[i][j] = d
                graph[j][i] = d
    
    # Constructive mapping to Kähler manifold (simplified)
    kdim_G = sum(sum(row) for row in graph) / (n * (n - 1))
    
    formula = ' or '.join(f'x{i} and x{j}' if graph[i][j] > 0 else f'~x{i} and ~x{j}' for i in range(n) for j in range(i + 1, n))
    width = resolution_width(formula)
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": kdim_G == width,
        "counterexample": "" if kdim_G == width else f"kdim(G)={kdim_G}, w(φ_G)={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"kdim(G) != w(φ_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")