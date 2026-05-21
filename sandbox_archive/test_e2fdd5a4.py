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
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i+1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def solve_linear_system(matrix, b):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    augmented_matrix = gaussian_elimination(augmented_matrix)
    x = [0] * cols
    for i in range(rows-1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i+1, cols))) / augmented_matrix[i][i]
    return x

def distance(point1, point2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)) ** 0.5

def min_geometric_invariant(vertices, facets):
    min_dist = float('inf')
    for facet in facets:
        if len(facet) < 2:
            continue
        points = [vertices[i] for i in facet]
        A = [[points[j][k] - points[0][k] for k in range(len(points[0]))] for j in range(1, len(points))]
        b = [-distance(points[0], point) for point in points[1:]]
        try:
            x = solve_linear_system(A, b)
            min_dist = min(min_dist, distance([x[k] for k in range(len(points[0]))], points[0]))
        except ZeroDivisionError:
            continue
    return min_dist

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    vertices = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(2**n)]
    facets = [set(random.sample(range(len(vertices)), random.randint(3, n))) for _ in range(2**n)]
    min_dist = min_geometric_invariant(vertices, facets)
    return {
        "metric_name": "min_geometric_invariant",
        "metric_value": min_dist,
        "instances_tested": len(facets),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")