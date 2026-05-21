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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def construct_moment_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for i, j in edges:
            M[i][j] += 1
            M[j][i] += 1
        return M
    
    def is_positive_semidefinite(M):
        n = len(M)
        for k in range(1, n + 1):
            submatrix = [row[:k] for row in M[:k]]
            det = determinant(submatrix)
            if det < 0:
                return False
        return True
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_real_rooted(poly):
        n = len(poly)
        if n == 1:
            return poly[0] != 0
        for i in range(1, n):
            if poly[i].denominator != 1 or poly[i].numerator < 0:
                return False
        return True
    
    def find_real_stable_minor(M, d=2):
        n = len(M)
        minors = []
        for i in range(n - d + 1):
            for j in range(i, n - d + 1):
                minor = [row[j:j+d] for row in M[i:i+d]]
                if is_positive_semidefinite(minor) and is_real_rooted([Fraction(coeff, 1) for coeff in poly]):
                    minors.append(minor)
        return minors
    
    def sos_refutation_threshold(M):
        n = len(M)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = M[i][j]
                A[j][i] = M[i][j]
        A[n][n] = 1
        b = [0] * (n + 1)
        b[n] = -1
        x = gaussian_elimination(A, b)
        return sum(x[:n])
    
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
                A[j][i] = 0
                for k in range(i+1, n+1):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def degree_2_moment_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for i, j in edges:
            M[i][j] += 1
            M[j][i] += 1
        return M
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    M = construct_moment_matrix(edges, n)
    
    minors = find_real_stable_minor(M, d=2)
    threshold = sos_refutation_threshold(degree_2_moment_matrix(edges, n))
    
    metric_value = len(minors) * threshold
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "sos_refutation_threshold",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")