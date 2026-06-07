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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiplication(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m = len(A)
        n = len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        
        for i in range(n):
            if i >= m:
                break
            max_row = i
            for j in range(i+1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(n+1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = augmented_matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= augmented_matrix[i][j] * x[j]
        return x
    
    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        A = [row[:] for row in matrix]
        r = gaussian_elimination(A, [0]*n)
        return sum(1 for val in r if abs(val) > 1e-9)
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                x = [i >> k & 1 for k in range(n)]
                y = [j >> k & 1 for k in range(n)]
                M[i][j] = f[x.index(0), y.index(0)]
        return M
    
    def local_cohomology(f, q):
        n = int(math.log2(len(f)))
        A = [[0] * (q**n) for _ in range(q**n)]
        b = [0] * (q**n)
        for i in range(q**n):
            x = [i >> k & (q-1) for k in range(n)]
            if f[x.index(0)] == 1:
                A[i][i] = 1
                b[i] = 1
        return gaussian_elimination(A, b)
    
    def standard_deviation(lst):
        mean = sum(lst) / len(lst)
        variance = sum((x - mean)**2 for x in lst) / len(lst)
        return math.sqrt(variance)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        q = random.randint(2, 5)
        H_f = local_cohomology(f, q)
        M = communication_matrix(f)
        ranks = [rank(submatrix) for submatrix in M]
        sigma_rank = standard_deviation(ranks)
        
        if len(H_f) == 0:
            continue
        
        min_H = min(abs(x) for x in H_f)
        results.append((min_H, sigma_rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_min_H = sum(min_H for min_H, _ in results) / len(results)
    mean_sigma_rank = sum(sigma_rank for _, sigma_rank in results) / len(results)
    correlation_coefficient = (sum((min_H - mean_min_H) * (sigma_rank - mean_sigma_rank) for min_H, sigma_rank in results) /
                               math.sqrt(sum((min_H - mean_min_H)**2 for min_H, _ in results) *
                                         sum((sigma_rank - mean_sigma_rank)**2 for _, sigma_rank in results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={res['seed']}")
                break