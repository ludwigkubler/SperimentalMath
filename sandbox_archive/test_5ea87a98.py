# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction
from collections import defaultdict

def matrix_mult(a, b):
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[Fraction(0, 1) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_add(a, b):
    n = len(a)
    m = len(a[0])
    result = [[Fraction(0, 1) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = a[i][j] + b[i][j]
    return result

def matrix_scalar_mult(s, a):
    n = len(a)
    m = len(a[0])
    result = [[Fraction(0, 1) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = s * a[i][j]
    return result

def characteristic_polynomial(matrix):
    n = len(matrix)
    if n == 0:
        return [Fraction(1, 1)]
    char_poly = [Fraction(0, 1) for _ in range(n + 1)]
    char_poly[-1] = Fraction(1, 1)
    identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for i in range(n):
        if i == 0:
            a = matrix
        else:
            a = matrix_mult(matrix, a)
        trace = Fraction(0, 1)
        for j in range(n):
            trace += a[j][j]
        char_poly[n - i - 1] = (-1) ** (i + 1) * trace / Fraction(i + 1, 1)
    return char_poly

def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n = n // 2
        count += 1
    return count

def lower_convex_hull(points):
    points = sorted(points, key=lambda x: (x[0], -x[1]))
    hull = []
    for point in points:
        while len(hull) >= 2 and (hull[-1][1] - hull[-2][1]) * (point[0] - hull[-2][0]) <= (hull[-1][0] - hull[-2][0]) * (point[1] - hull[-2][1]):
            hull.pop()
        hull.append(point)
    return hull

def compute_newton_slope_count(char_poly):
    points = []
    for i, coeff in enumerate(char_poly):
        if coeff != 0:
            points.append((i, v2(coeff.numerator)))
    hull = lower_convex_hull(points)
    slopes = set()
    for i in range(1, len(hull)):
        dx = hull[i][0] - hull[i-1][0]
        dy = hull[i][1] - hull[i-1][1]
        if dx != 0:
            slope = Fraction(dy, dx)
            slopes.add(slope)
    return len(slopes)

def generate_disjointness_matrix(n, rows, cols):
    matrix = [[0 for _ in range(len(cols))] for _ in range(len(rows))]
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            intersection = set(row) & set(col)
            matrix[i][j] = (-1) ** (1 if intersection else 0)
    return matrix

def generate_random_matrix(n, k):
    matrix = [[0 for _ in range(k)] for _ in range(k)]
    for i in range(k):
        for j in range(k):
            matrix[i][j] = random.choice([-1, 1])
    return matrix

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 10, 14, 18, 22]
    metric_values = []
    random_metric_values = []
    for n in n_values:
        k = min(2 * n, 40)
        rows = [random.sample(range(2 ** n), k) for _ in range(30)]
        cols = [random.sample(range(2 ** n), k) for _ in range(30)]
        disj_metric_values = []
        random_metric_values_n = []
        for row, col in zip(rows, cols):
            disj_matrix = generate_disjointness_matrix(n, row, col)
            char_poly = characteristic_polynomial(disj_matrix)
            disj_metric_values.append(compute_newton_slope_count(char_poly))
            random_matrix = generate_random_matrix(n, k)
            random_char_poly = characteristic_polynomial(random_matrix)
            random_metric_values_n.append(compute_newton_slope_count(random_char_poly))
        metric_values.extend(disj_metric_values)
        random_metric_values.extend(random_metric_values_n)
    disj_median = sorted(metric_values)[len(metric_values) // 2]
    random_median = sorted(random_metric_values)[len(random_metric_values) // 2]
    ratio = disj_median / random_median if random_median != 0 else float('inf')
    conjecture_holds = ratio >= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 1.5 for seed {seed}"
    return {
        "metric_name": "2-adic Newton slope count",
        "metric_value": disj_median,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_seeds = [i for i, r in enumerate(results) if not r["conjecture_holds"]]
        first_failing_seed = seeds[failing_seeds[0]] if failing_seeds else None
        counterexample = results[failing_seeds[0]]["counterexample"] if failing_seeds else ""
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")