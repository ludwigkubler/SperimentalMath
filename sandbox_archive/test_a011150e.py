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
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def number_of_distinct_roots(f):
        n = len(f)
        roots = set()
        for i in range(2**n):
            z = complex(i, 0)
            if abs(z) > 1e-6 and f[i] == 1:
                roots.add(z)
        return len(roots)
    
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
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        p = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(p):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Singular matrix")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        inv_A = [[adjoint[i][j] / det_A for j in range(n)] for i in range(n)]
        return inv_A
    
    def riemann_roch_theorem(f):
        n = len(f)
        rank = communication_complexity_rank(f)
        genus = (n - 1) // 2
        Riemann_Roch = rank + genus - 1
        return Riemann_Roch
    
    def number_of_distinct_roots_meromorphic_function(f):
        n = len(f)
        roots_count = 0
        for i in range(2**n):
            z = complex(i, 0)
            if abs(z) > 1e-6 and f[i] == 1:
                roots_count += 1
        return roots_count
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    roots_counts = []
    ranks = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        roots_count = number_of_distinct_roots_meromorphic_function(f)
        roots_counts.append(roots_count)
        ranks.append(rank)
    
    if len(roots_counts) < 30 or len(ranks) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(roots_counts),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = correlation_coefficient(ranks, roots_counts)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(roots_counts),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")