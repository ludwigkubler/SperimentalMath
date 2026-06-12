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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(i, n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return [row[-1] for row in A]

    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(1 for j in range(n) if G[i][j])
            L[i][i] = -degree
            for j in range(i+1, n):
                if G[i][j]:
                    L[i][j] = 1
                    L[j][i] = 1
        return L

    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        elif n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            return [d - a, -(a*d - b*c), a*b - c*d]
        else:
            det = 0
            for j in range(n):
                submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += (-1)**j * matrix[0][j] * determinant(submatrix)
            return [det]

    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(len(matrix)):
                submatrix = [[matrix[i][k] for k in range(1, len(matrix)) if k != j] for i in range(1, len(matrix))]
                det += (-1)**j * matrix[0][j] * determinant(submatrix)
            return det

    def hodge_bundle_metrics(laplacian):
        char_poly = characteristic_polynomial(laplacian)
        if len(char_poly) < 2:
            return None
        return abs(char_poly[-2])

    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    ranks = []

    for n in n_values:
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        laplacian = laplacian_matrix(G)
        char_poly = characteristic_polynomial(laplacian)
        h_value = hodge_bundle_metrics(laplacian)
        rank = communication_complexity_rank(G)

        if h_value is not None:
            h_values.append(h_value)
            ranks.append(rank)

    if len(h_values) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(h_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    correlation = sum((h - mean_h) * (r - mean_r) for h, r in zip(h_values, ranks)) / len(h_values)
    mean_diff = sum(abs(h - r) for h, r in zip(h_values, ranks)) / len(h_values)

    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(h_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_corr = (sum((result["metric_value"] - mean_corr)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")