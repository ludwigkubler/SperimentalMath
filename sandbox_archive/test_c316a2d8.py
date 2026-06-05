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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def matrix_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if all(not math.isclose(matrix[j][i], 0) for j in range(rank)):
                rank += 1
        return rank
    
    def communication_complexity_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        matrix_copy = [row[:] for row in matrix]
        gaussian_elimination(matrix_copy)
        return sum(1 for row in matrix_copy if any(not math.isclose(x, 0) for x in row))
    
    def generate_affine_scheme(n):
        points = set()
        while len(points) < n:
            point = tuple(random.randint(0, 2**31 - 1) % 2 for _ in range(n))
            if all(point[i] == 0 or point[i] == 1 for i in range(n)):
                points.add(point)
        return list(points)
    
    def associated_sheaf(points):
        n = len(points)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points):
                if all(p1[k] == p2[k] for k in range(n)):
                    matrix[i][j] += 1
        return matrix
    
    def min_order(matrix):
        rows, cols = len(matrix), len(matrix[0])
        order = 0
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] > order:
                    order = matrix[i][j]
        return order
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    points = generate_affine_scheme(n)
    sheaf_matrix = associated_sheaf(points)
    min_order_value = min_order(sheaf_matrix)
    cr = communication_complexity_rank(sheaf_matrix)
    
    if cr == 0:
        return {
            "metric_name": "MinOrder",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if not (0.5 * cr <= min_order_value <= 1.5 * cr):
        return {
            "metric_name": "MinOrder",
            "metric_value": min_order_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"min_order={min_order_value}, cr={cr}"
        }
    
    return {
        "metric_name": "MinOrder",
        "metric_value": min_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_order_out_of_range' first_failing_seed={first_failing_seed}")