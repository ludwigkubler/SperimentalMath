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
    
    def generate_disjointness_matrix(n):
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if bin(i & j).count('1') == 1:
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        for j in range(n):
            max_row = j
            for i in range(j+1, m):
                if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                    max_row = i
            augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
            pivot = augmented_matrix[j][j]
            for k in range(n+1):
                augmented_matrix[j][k] /= pivot
            for i in range(m):
                if i != j:
                    factor = augmented_matrix[i][j]
                    for k in range(n+1):
                        augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
        return [row[-1] for row in augmented_matrix]
    
    def secant_variety_dimension(matrix):
        n = len(matrix)
        if n % 2 != 0:
            return None
        A = matrix
        B = [[A[i][j] + A[j][i] for j in range(n)] for i in range(n)]
        C = matrix_multiplication(A, B)
        det_C = 1
        for i in range(n):
            det_C *= C[i][i]
        return math.log2(det_C) / n
    
    def disjointness_communication_complexity(n):
        A = generate_disjointness_matrix(n)
        dimension = secant_variety_dimension(A)
        if dimension is None:
            return None
        return dimension
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        result = disjointness_communication_complexity(n)
        if result is None:
            continue
        results.append(result)
    
    if not results:
        return {
            "metric_name": "disjointness_communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(x >= n for n, x in zip(n_values, results))
    counterexample = "" if conjecture_holds else f"n={max(n_values)}, dimension={min(results)}"
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")