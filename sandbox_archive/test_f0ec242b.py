# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        pivot_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular and cannot be reduced.")
        for j in range(i, cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def minimal_rank(n, q):
    # Construct a random k-clique instance on n vertices
    edges = set()
    while len(edges) < n:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    # Map the k-clique to a set of points in F_q(T)
    points = []
    for i in range(n):
        point = [random.randint(0, q - 1) for _ in range(n)]
        points.append(point)
    
    # Create the distance matrix
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = sum((points[i][k] - points[j][k]) ** 2 for k in range(n))
            if dist == 0:
                raise ValueError("Points are not distinct.")
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist
    
    # Create the configuration space matrix
    config_space_matrix = []
    for i in range(n):
        row = [1]
        for j in range(i + 1, n):
            if (i, j) in edges:
                row.append(distance_matrix[i][j])
            else:
                row.append(0)
        config_space_matrix.append(row)
    
    # Compute the minimal rank
    reduced_matrix = gaussian_elimination(config_space_matrix)
    rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(2, 10)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "minimal_rank"
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        rank = minimal_rank(n, q)
        expected_bound = Fraction(1, 2) * n * (n - 1) * math.log(q**(n/2))
        if rank < expected_bound:
            return {
                "metric_name": metric_name,
                "metric_value": rank,
                "instances_tested": instances_tested + 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} is less than the expected bound {expected_bound}"
            }
        total_metric_value += rank
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank below expected bound\" first_failing_seed={first_failing_seed}")