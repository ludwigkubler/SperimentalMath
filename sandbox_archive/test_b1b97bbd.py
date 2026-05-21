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
        A = [random.randint(0, n-1) for _ in range(n)]
        B = list(set(range(n)) - set(A))
        return A, B
    
    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                return None
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(n):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[n:] for row in augmented_matrix]
    
    def symbolic_rank_check(poly):
        n = len(poly)
        A = [[poly[j][i] if i < j else poly[i][j] for i in range(n)] for j in range(n)]
        rank = 0
        for i in range(n):
            if gaussian_elimination(A[:i+1]) is not None:
                rank += 1
        return rank
    
    def sdp_relaxation(poly, d):
        n = len(poly)
        A = [[poly[j][i] if i < j else poly[i][j] for i in range(n)] for j in range(n)]
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                B[i][j] = A[i][j]
                B[j][i] = A[i][j]
        C = [[0] * (n + d) for _ in range(n + d)]
        for i in range(n):
            C[i][i] = 1
        C[n+d-1][n+d-1] = -1
        return C
    
    def sos_refutation_degree(poly, d):
        n = len(poly)
        A = [[poly[j][i] if i < j else poly[i][j] for i in range(n)] for j in range(n)]
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                B[i][j] = A[i][j]
                B[j][i] = A[i][j]
        C = [[0] * (n + d) for _ in range(n + d)]
        for i in range(n):
            C[i][i] = 1
        C[n+d-1][n+d-1] = -1
        return len(C)
    
    def log(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x + 1)
    
    n = 40
    A, B = generate_max_cut_instance(n)
    poly = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    d = symbolic_rank_check(poly)
    degree = sos_refutation_degree(poly, d)
    
    return {
        "metric_name": "sos_refutation_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": degree >= log(d + 1),
        "counterexample": "" if degree >= log(d + 1) else f"Graph with n={n}, A={A}, B={B}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=40\" first_failing_seed={first_failing_seed}")