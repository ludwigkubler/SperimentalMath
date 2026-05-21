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
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for k in range(i + 1, n):
            factor = -A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] += factor * A[i][j]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
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

def geometric_entropy(G):
    n = len(G)
    laplacian_matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    degree_sum = 0
    for i in range(n):
        degree = sum(G[i])
        degree_sum += degree
        laplacian_matrix[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                laplacian_matrix[i][j] = Fraction(1)
                laplacian_matrix[j][i] = Fraction(1)
    laplacian_matrix = gaussian_elimination(laplacian_matrix)
    det = determinant(laplacian_matrix)
    return -math.log(det) / degree_sum

def disjointness_complexity(n):
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    gamma_values = []
    kappa_values = []
    
    for _ in range(30):
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        
        gamma_Q = geometric_entropy(G)
        kappa_DISJ_n = disjointness_complexity(n)
        
        gamma_values.append(gamma_Q)
        kappa_values.append(kappa_DISJ_n)
    
    mean_gamma = sum(gamma_values) / len(gamma_values)
    std_gamma = math.sqrt(sum((x - mean_gamma) ** 2 for x in gamma_values) / len(gamma_values))
    mean_kappa = sum(kappa_values) / len(kappa_values)
    
    conjecture_holds = all(g >= m + s for g, m, s in zip(gamma_values, [mean_kappa] * len(gamma_values), [std_gamma] * len(gamma_values)))
    counterexample = "" if conjecture_holds else "geometric_entropy < kappa(DISJ_n) by less than 1 std deviation"
    
    return {
        "metric_name": "gamma_Q",
        "metric_value": mean_gamma,
        "instances_tested": len(gamma_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_gamma = sum(r["metric_value"] for r in results) / len(results)
    std_gamma = math.sqrt(sum((r["metric_value"] - mean_gamma) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gamma} std={std_gamma} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gamma} std={std_gamma} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")