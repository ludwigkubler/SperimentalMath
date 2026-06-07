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
    
    def generate_communication_protocol(n):
        # Generate a random n-ary communication protocol
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def compute_information_matrix(protocol):
        # Compute the information matrix from the protocol
        n = len(protocol)
        info_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                count = sum(1 for k in range(n) if protocol[i][k] != protocol[j][k])
                info_matrix[i][j] = info_matrix[j][i] = Fraction(count, n)
        return info_matrix
    
    def rank_variance(matrix):
        # Compute the rank variance of the matrix
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        rank = gaussian_elimination(matrix)
        return (n - rank) / n
    
    def gaussian_elimination(matrix):
        # Perform Gaussian elimination to find the rank of the matrix
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return float('inf')
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def determinant(matrix):
        # Compute the determinant of a square matrix
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def minimal_order_of_local_units(matrix):
        # Compute the minimal order of local units in the adjoint group
        n = len(matrix)
        adjoint_group = []
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] != 0:
                    adjoint_group.append((i, j))
        return min(abs(x - y) for x, y in adjoint_group)
    
    def pearson_correlation_coefficient(x, y):
        # Compute the Pearson correlation coefficient
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        protocol = generate_communication_protocol(n)
        info_matrix = compute_information_matrix(protocol)
        rank_var = rank_variance(info_matrix)
        min_order_units = minimal_order_of_local_units(info_matrix)
        results.append((min_order_units, rank_var))
    
    x = [res[0] for res in results]
    y = [res[1] for res in results]
    correlation_coefficient = pearson_correlation_coefficient(x, y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")