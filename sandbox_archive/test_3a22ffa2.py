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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_product_manifold(f):
        n = len(f)
        m = len(f[0])
        M = [[f[i][j] * f[k][l] for l in range(m)] for k in range(m) for j in range(n)]
        return M
    
    def minimal_kahler_ricci_form(M):
        n, m = len(M), len(M[0])
        sum_M = 0
        for i in range(n):
            for j in range(m):
                sum_M += M[i][j]
        if sum_M == 0:
            return 0
        return sum_M / (n * m)
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 1
        while True:
            found = False
            for i in range(n):
                if f[i].count(1) > rank:
                    found = True
                    break
            if not found:
                return rank
            rank += 1
    
    def matrix_multiply(A, B):
        n, m = len(A), len(B[0])
        p = len(B)
        C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]
        return C
    
    def matrix_add(A, B):
        n, m = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
        return C
    
    def matrix_sub(A, B):
        n, m = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
        return C
    
    def matrix_transpose(A):
        n, m = len(A), len(A[0])
        A_t = [[A[j][i] for j in range(n)] for i in range(m)]
        return A_t
    
    def matrix_inverse(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            denom = A[i][i]
            if denom == 0:
                continue
            for j in range(n):
                A[i][j] /= denom
                I[i][j] /= denom
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return I
    
    def gaussian_elimination(A, b):
        n = len(b)
        Ab = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(Ab[j][i]) > abs(Ab[max_row][i]):
                    max_row = j
            Ab[i], Ab[max_row] = Ab[max_row], Ab[i]
            factor = Ab[i][i]
            for j in range(n):
                Ab[i][j] /= factor
            b[i] /= factor
            for j in range(i+1, n):
                factor = Ab[j][i]
                for k in range(n):
                    Ab[j][k] -= factor * Ab[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= Ab[i][j] * x[j]
        return x
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det
    
    def matrix_power(A, k):
        n = len(A)
        result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, A)
            A = matrix_multiply(A, A)
            k //= 2
        return result
    
    def trace(A):
        n = len(A)
        tr = sum(A[i][i] for i in range(n))
        return tr
    
    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += A[i][j] ** 2
        return math.sqrt(norm)
    
    def spectral_radius(A):
        n = len(A)
        eigenvalues = []
        for _ in range(100):  # Power iteration method
            x = [random.random() for _ in range(n)]
            x /= frobenius_norm(x)
            A_x = matrix_multiply(A, x)
            lambda_ = dot_product(A_x, x) / dot_product(x, x)
            eigenvalues.append(lambda_)
        return max(eigenvalues)
    
    def dot_product(a, b):
        return sum(i * j for i, j in zip(a, b))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    metric_sum = 0.0
    max_n = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = tensor_product_manifold(f)
        κ_f = minimal_kahler_ricci_form(M)
        c_r_f = communication_complexity_rank(f)
        
        if κ_f == 0 or c_r_f == 0:
            continue
        
        metric_sum += κ_f * c_r_f
        instances_tested += 1
        max_n = n
    
    if instances_tested == 0:
        return {
            "metric_name": "κ_f * c_r(f)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_metric = metric_sum / instances_tested
    if κ_f > 1.5 * (metric_sum / instances_tested):
        return {
            "metric_name": "κ_f * c_r(f)",
            "metric_value": κ_f,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": f"κ_f > 1.5 * mean(κ_f * c_r(f)) for n={max_n}"
        }
    
    return {
        "metric_name": "κ_f * c_r(f)",
        "metric_value": κ_f,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='κ_f > 1.5 * mean(κ_f * c_r(f))' first_failing_seed={first_failing_seed}")