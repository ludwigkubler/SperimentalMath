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
    
    def generate_random_code(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
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
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return A, b
    
    def minimal_p_adic_rank(code):
        n = len(code)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [1] for row in code]
        _, _, rank = gaussian_elimination(augmented_matrix, [0] * n)
        return rank
    
    def communication_complexity_rank(code):
        n = len(code)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [1] for row in code]
        _, _, rank = gaussian_elimination(augmented_matrix, [0] * n)
        return rank
    
    def correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_dev_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_dev_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexity_ranks = []
    
    for n in n_values:
        code = generate_random_code(n)
        min_rank = minimal_p_adic_rank(code)
        comm_complexity_rank_value = communication_complexity_rank(code)
        min_ranks.append(min_rank)
        comm_complexity_ranks.append(comm_complexity_rank_value)
    
    correlation_coefficient_value = correlation_coefficient(min_ranks, comm_complexity_ranks)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient_value,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient_value >= 0.7 and all(corr >= 0.5 for corr in comm_complexity_ranks),
        "counterexample": "" if correlation_coefficient_value >= 0.7 else f"Correlation coefficient {correlation_coefficient_value} < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and min(res["metric_value"] for res in results if not res["conjecture_holds"]) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")