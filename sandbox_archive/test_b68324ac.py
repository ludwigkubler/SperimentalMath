# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_disjointness_matrix(n, rows, cols):
    matrix = []
    for i in rows:
        row = []
        for j in cols:
            intersection = set(bin(i)[2:].zfill(n)) & set(bin(j)[2:].zfill(n))
            if intersection:
                row.append(-1)
            else:
                row.append(1)
        matrix.append(row)
    return matrix

def generate_random_matrix(k):
    return [[random.choice([-1, 1]) for _ in range(k)] for _ in range(k)]

def matrix_multiply(a, b):
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_trace(m):
    return sum(m[i][i] for i in range(len(m)))

def faddeev_leverrier(matrix):
    n = len(matrix)
    char_poly = [Fraction(1)]
    for i in range(n):
        trace = matrix_trace(matrix)
        char_poly.append(-trace / (i + 1))
        if i < n - 1:
            matrix = matrix_multiply(matrix, matrix)
            for j in range(i + 1):
                matrix[j][j] += char_poly[i - j]
    return char_poly

def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def compute_newton_slope_count(coeffs):
    points = [(i, v2(abs(c))) for i, c in enumerate(coeffs) if c != 0]
    if not points:
        return 0
    points.sort()
    hull = [points[0]]
    for point in points[1:]:
        while len(hull) >= 2 and (hull[-1][1] - hull[-2][1]) * (point[0] - hull[-1][0]) <= (point[1] - hull[-1][1]) * (hull[-1][0] - hull[-2][0]):
            hull.pop()
        hull.append(point)
    slopes = []
    for i in range(1, len(hull)):
        dx = hull[i][0] - hull[i-1][0]
        dy = hull[i][1] - hull[i-1][1]
        if dx == 0:
            slope = float('inf')
        else:
            slope = dy / dx
        slopes.append(slope)
    return len(set(slopes))

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 10, 14, 18, 22]
    disj_slopes = []
    random_slopes = []
    for n in n_values:
        k = min(2 * n, 40)
        rows = random.sample(range(2**n), k)
        cols = random.sample(range(2**n), k)
        disj_matrix = generate_disjointness_matrix(n, rows, cols)
        disj_char_poly = faddeev_leverrier(disj_matrix)
        disj_slope_count = compute_newton_slope_count(disj_char_poly)
        disj_slopes.append(disj_slope_count)

        random_matrix = generate_random_matrix(k)
        random_char_poly = faddeev_leverrier(random_matrix)
        random_slope_count = compute_newton_slope_count(random_char_poly)
        random_slopes.append(random_slope_count)

    disj_median = sorted(disj_slopes)[len(disj_slopes) // 2]
    random_median = sorted(random_slopes)[len(random_slopes) // 2]
    ratio = disj_median / random_median if random_median != 0 else float('inf')

    conjecture_holds = ratio >= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 1.5 for seed {seed}"

    return {
        "metric_name": "median_newton_slope_count",
        "metric_value": disj_median,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={failing_seed}")