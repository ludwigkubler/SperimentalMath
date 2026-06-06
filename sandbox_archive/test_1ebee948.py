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

def generate_k_clique(n: int, k: int) -> tuple:
    if n < k or k <= 0:
        return None
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    return vertices, edges

def matrix_representation(vertices, edges):
    n = len(vertices)
    A = [[0] * n for _ in range(n)]
    B = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
        B[u][v] = 1
        B[v][u] = 1
    return A, B

def frobenius_quotient(A, B):
    n = len(A)
    det_A = determinant(A)
    det_B = determinant(B)
    if det_A == 0 or det_B == 0:
        return None
    return abs(det_A / det_B)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def communication_complexity_rank(A, B):
    n = len(A)
    rank_A = gaussian_elimination(A)
    rank_B = gaussian_elimination(B)
    return max(rank_A, rank_B)

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] for row in matrix]
    rank = 0
    for i in range(n):
        if rank == n:
            break
        pivot_row = -1
        for j in range(i, n):
            if augmented_matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        for j in range(n + 1):
            augmented_matrix[i][j] /= augmented_matrix[i][i]
        for j in range(n):
            if j != i and augmented_matrix[j][i] != 0:
                factor = augmented_matrix[j][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    k_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max_encountered = 0

    for k in k_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            vertices, edges = generate_k_clique(n_max + 1, k)
            if vertices is None or edges is None:
                continue
            A, B = matrix_representation(vertices, edges)
            fq = frobenius_quotient(A, B)
            if fq is not None:
                cc_rank = communication_complexity_rank(A, B)
                if cc_rank > 0:
                    metric_values.append((math.log2(fq), math.log2(cc_rank)))
                    instances_tested += 1
                    n_max_encountered = max(n_max_encountered, n_max)

    if not metric_values:
        return {
            "metric_name": "log_frobenius_quotient_vs_log_communication_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max_encountered,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    log_fq, log_cc_rank = zip(*metric_values)
    correlation_coefficient = sum((x - mean(log_fq)) * (y - mean(log_cc_rank)) for x, y in zip(log_fq, log_cc_rank)) / (len(metric_values) * stdev(log_fq) * stdev(log_cc_rank))
    
    return {
        "metric_name": "log_frobenius_quotient_vs_log_communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max_encountered,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def stdev(lst):
    avg = mean(lst)
    variance = sum((x - avg) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_value = mean([result["metric_value"] for result in results])
        std_value = stdev([result["metric_value"] for result in results])
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")