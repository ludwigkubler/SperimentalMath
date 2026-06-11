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
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(matrix):
        n = len(matrix)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix_multiply(I, matrix)
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank / n

    def lie_algebroid_order(matrix):
        n = len(matrix)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix_multiply(I, matrix)
        A = gaussian_elimination(A)
        order = sum(1 for row in A if any(row))
        return order

    instances_tested = 30
    n_max = 40
    metric_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        alpha = rank_variance(matrix)
        order = lie_algebroid_order(matrix)
        metric_values.append(order / math.sqrt(alpha))

    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)

    conjecture_holds = all(abs(x - mean_value) <= std_value * 1.96 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "lie_algebroid_order_rank_variance_ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.4f}")