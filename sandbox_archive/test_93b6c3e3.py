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
    
    def tl_algebra(n):
        if n == 0:
            return [[1]]
        elif n == 2:
            return [[1, -1], [-1, 1]]
        else:
            prev_matrix = tl_algebra(n - 2)
            size = len(prev_matrix)
            new_matrix = []
            for row in prev_matrix:
                new_row = [0] * (size + 2)
                new_row[0] = 1
                new_row[-1] = -1
                for i in range(size):
                    new_row[i + 1] = row[i]
                new_matrix.append(new_row)
            return new_matrix
    
    def matrix_multiply(A, B):
        result = []
        for i in range(len(A)):
            row = [0] * len(B[0])
            for j in range(len(B[0])):
                for k in range(len(B)):
                    row[j] += A[i][k] * B[k][j]
            result.append(row)
        return result
    
    def matrix_determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            sub_matrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1) ** i * matrix[0][i] * matrix_determinant(sub_matrix)
        return det
    
    def min_categorical_dimension(graph):
        n = len(graph)
        tl_matrix = tl_algebra(n)
        det = matrix_determinant(tl_matrix)
        if det == 0:
            return float('inf')
        else:
            return math.log2(abs(det))
    
    def dpll_tree_height(graph):
        if not graph:
            return 1
        max_height = 0
        for neighbor in graph[0]:
            height = dpll_tree_height(graph[1:])
            if height > max_height:
                max_height = height
        return max_height + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if not any(graph[i][j] == graph[j][i] for i in range(n) for j in range(i + 1, n)):
            continue
        min_dim = min_categorical_dimension(graph)
        height = dpll_tree_height(graph)
        metrics.append((min_dim, height))
    
    if len(metrics) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    x, y = zip(*metrics)
    correlation = pearson_correlation(x, y)
    k = 3
    all_hold = all(abs(a - b) <= k for a, b in metrics)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all_hold,
        "counterexample": "" if correlation >= 0.8 and all_hold else "not_enough_support"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")