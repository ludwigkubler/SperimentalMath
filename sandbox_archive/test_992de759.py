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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def isqrt(n):
        x = n
        y = (x + 1) // 2
        while y < x:
            x, y = y, (y + x) // 2
        return x
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def is_positive_definite(M):
        n = len(M)
        for i in range(n):
            if M[i][i] <= 0:
                return False
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                M[j][i:] = [M[j][k] - factor * M[i][k] for k in range(i, n)]
        return True
    
    def is_sum_of_squares(M):
        n = len(M)
        if not is_positive_definite(M):
            return False
        x = gaussian_elimination(M, [0] * n)
        return all(x[i]**2 <= M[i][i] for i in range(n))
    
    def max_cut_instance(n):
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(edges)
        return [random.choice([0, 1]) for _ in edges]
    
    def construct_polynomial(instance):
        n = len(instance)
        poly = sum(1 - instance[i] * instance[j] for i, j in enumerate(instance))
        return poly
    
    def moment_matrix(poly, n):
        m = len(poly)
        M = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(i, m + 1):
                if j == i:
                    M[i][j] = sum(1 for x in poly if x == i)
                else:
                    M[i][j] = sum(x * y for x, y in zip(poly[:i], poly[j - i:]))
        return M
    
    def sos_degree(M, epsilon):
        n = len(M)
        d = 0
        while True:
            d += 1
            A = [[0] * (d + 1) for _ in range(d + 1)]
            b = [0] * (d + 1)
            for i in range(n):
                for j in range(i, n):
                    if M[i][j] != 0:
                        A[i % (d + 1)][j % (d + 1)] += M[i][j]
                        b[i % (d + 1)] += M[i][j]
            x = gaussian_elimination(A, b)
            if all(x[i]**2 <= M[i][i] for i in range(n)):
                return d
    
    n = 40
    instance = max_cut_instance(n)
    poly = construct_polynomial(instance)
    M = moment_matrix(poly, n)
    
    if not is_positive_definite(M):
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_positive_definite"
        }
    
    if is_sum_of_squares(M):
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sum_of_squares"
        }
    
    epsilon = 0.95
    d = sos_degree(M, epsilon)
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": d >= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")