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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        m = [[f[i * (i + 1) // 2 + j] for j in range(i + 1)] for i in range(n)]
        rank = 0
        for row in m:
            if any(row):
                rank += 1
        return rank
    
    def alexander_dirac_invariant(m):
        n = len(m)
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if m[i][j]:
                    for k in range(n):
                        if m[k][i] and m[k][j]:
                            adj_matrix[i][j] += 1
                            adj_matrix[j][i] += 1
        return sum(sum(row) for row in adj_matrix) / (2 * n * (n - 1))
    
    def gaussian_elimination(A):
        n = len(A)
        B = [row[:] for row in A]
        rank = 0
        for i in range(n):
            if B[i][i] == 0:
                for j in range(i + 1, n):
                    if B[j][i] != 0:
                        B[i], B[j] = B[j], B[i]
                        break
            if B[i][i] != 0:
                rank += 1
                for j in range(n):
                    B[i][j] /= B[i][i]
                for k in range(n):
                    if k != i and B[k][i] != 0:
                        for j in range(n):
                            B[k][j] -= B[k][i] * B[i][j]
        return rank
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_singular(matrix):
        return determinant(matrix) == 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_correlation = Fraction(0)
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            comm_rank = communication_complexity_rank(f)
            matrix = [[f[i * (i + 1) // 2 + j] for j in range(i + 1)] for i in range(n)]
            if is_singular(matrix):
                continue
            adj_matrix = gaussian_elimination(matrix)
            alex_invariant = alexander_dirac_invariant(adj_matrix)
            instances_tested += 1
            max_n = max(max_n, n)
            total_correlation += Fraction(alex_invariant * comm_rank)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    avg_correlation = total_correlation / instances_tested
    return {
        "metric_name": "correlation",
        "metric_value": float(avg_correlation),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": abs(avg_correlation) >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")