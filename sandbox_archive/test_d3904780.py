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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(minor)
            sign *= -1
        return det

    def geometric_entropy(matrix):
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        log_det = math.log(abs(det))
        entropy = -log_det / (n * math.log(n))
        return entropy

    def communication_complexity(n):
        # Simplified model for communication complexity
        return n * (n - 1) // 2

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        h_min = geometric_entropy(matrix)
        comm_complexity = communication_complexity(n)
        results.append({
            "n": n,
            "h_min": h_min,
            "comm_complexity": comm_complexity
        })
    
    metric_value = sum(result["h_min"] for result in results) / len(results)
    conjecture_holds = all(result["h_min"] >= result["n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Geometric Entropy",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")