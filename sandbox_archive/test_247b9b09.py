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
    
    def characteristic_polynomial(f):
        n = int(math.log2(len(f)))
        A = [[f[i ^ j] ^ f[i] ^ f[j] for j in range(2**n)] for i in range(2**n)]
        return A
    
    def grothendieck_witt_class(A, mod=2):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = matrix_add(matrix_multiply(A, I, mod), I, mod)
        det = determinant(B, mod)
        return det
    
    def matrix_multiply(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_add(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C
    
    def determinant(matrix, mod):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix, mod)
        return det % mod
    
    def rank(matrix, mod=2):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(r)):
                matrix[r], matrix[i] = matrix[i], matrix[r]
                for j in range(r + 1, n):
                    factor = (matrix[j][i] * pow(matrix[r][i], -1, mod)) % mod
                    for k in range(n):
                        matrix[j][k] = (matrix[j][k] - factor * matrix[r][k]) % mod
                r += 1
        return r
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        A = characteristic_polynomial(f)
        max_rank = rank(A, 2)
        min_rank = 0
        for i in range(n + 1):
            B = [[A[j][k] % (2 ** i) for k in range(2**n)] for j in range(2**n)]
            min_rank = max(min_rank, rank(B, 2))
        return max_rank - min_rank
    
    def log_gw_class(gw_class):
        if gw_class == 0:
            return float('-inf')
        return math.log(abs(gw_class), 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        A = characteristic_polynomial(f)
        gw_class = grothendieck_witt_class(A)
        rank_variance = communication_complexity_rank_variance(f)
        results.append((n, rank_variance, log_gw_class(gw_class)))
    
    max_n = max(results, key=lambda x: x[0])[0]
    if max_n < 16:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_variances = [r for _, r, _ in results]
    gw_classes = [gw for _, _, gw in results]
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    mean_gw_class = sum(gw_classes) / len(gw_classes)
    std_rank_variance = math.sqrt(sum((r - mean_rank_variance) ** 2 for r in rank_variances) / len(rank_variances))
    corr_coeff = sum((rank_variances[i] - mean_rank_variance) * (gw_classes[i] - mean_gw_class) for i in range(len(results))) / (len(results) * std_rank_variance * math.sqrt(sum((gw_classes[i] - mean_gw_class) ** 2 for i in range(len(results)))))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": abs(corr_coeff) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")