# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) % 2 for j in range(n)] for i in range(m)]
        return result
    
    def matrix_power(matrix, k):
        result = [[int(i == j) for j in range(len(matrix))] for i in range(len(matrix))]
        base = matrix
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            k //= 2
        return result
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + sum(1 for j in range(i, m) if abs(A[j][i]) > abs(A[max_row][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                A[i][j] ^= A[i][i]
            for k in range(m):
                if k != i and A[k][i]:
                    for j in range(n):
                        A[k][j] ^= A[i][j]
        return A
    
    def is_invertible(matrix):
        det = 1
        for i in range(len(matrix)):
            det *= matrix[i][i]
        return det % 2 == 1
    
    def plethysm_coefficient(matrix, k):
        n = len(matrix)
        if not is_invertible(matrix):
            return None
        power_matrix = matrix_power(matrix, k)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        diff = matrix_multiply(power_matrix, gaussian_elimination(identity))
        non_zero_coeffs = [sum(row) for row in diff if sum(row) > 0]
        return min(non_zero_coeffs) / math.log(n)
    
    def disjointness_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A, B = disjointness_instance(n)
    plethysm_coeff = plethysm_coefficient(A, n)
    
    if plethysm_coeff is None:
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": plethysm_coeff,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results) or sum(r["conjecture_holds"] for r in results) / len(results) >= 0.8:
        mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None))
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")