# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction
from itertools import combinations

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

def matrix_power(a, power):
    n = len(a)
    result = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        result[i][i] = Fraction(1, 1)
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult(result, a)
        a = matrix_mult(a, a)
        power //= 2
    return result

def characteristic_poly(matrix):
    n = len(matrix)
    char_poly = [Fraction(0, 1) for _ in range(n + 1)]
    char_poly[-1] = Fraction(1, 1)
    identity = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        identity[i][i] = Fraction(1, 1)
    for i in range(n):
        power = n - i - 1
        power_matrix = matrix_power(matrix, power)
        trace = Fraction(0, 1)
        for j in range(n):
            trace += power_matrix[j][j]
        char_poly[power] = (-1) ** (i + 1) * trace
    return char_poly

def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def lower_convex_hull(points):
    points = sorted(points, key=lambda x: (x[0], -x[1]))
    hull = []
    for point in points:
        while len(hull) >= 2 and (hull[-1][1] - hull[-2][1]) * (point[0] - hull[-1][0]) <= (point[1] - hull[-1][1]) * (hull[-1][0] - hull[-2][0]):
            hull.pop()
        hull.append(point)
    return hull

def compute_nu2(char_poly):
    points = []
    for i, coeff in enumerate(char_poly):
        if coeff != 0:
            points.append((i, v2(coeff.numerator)))
    hull = lower_convex_hull(points)
    slopes = set()
    for i in range(1, len(hull)):
        x1, y1 = hull[i-1]
        x2, y2 = hull[i]
        if x1 != x2:
            slope = (y2 - y1) / (x2 - x1)
            slopes.add(slope)
    return len(slopes)

def generate_disjointness_matrix(n, rows, cols):
    matrix = [[Fraction(0, 1) for _ in range(len(cols))] for _ in range(len(rows))]
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            if any(bit in row and bit in col for bit in range(n)):
                matrix[i][j] = Fraction(-1, 1)
            else:
                matrix[i][j] = Fraction(1, 1)
    return matrix

def generate_random_matrix(n, m):
    matrix = [[Fraction(0, 1) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = Fraction(random.choice([-1, 1]), 1)
    return matrix

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 10, 14, 18, 22]
    nu2_disj = []
    nu2_random = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        k = min(2 * n, 40)
        rows = random.sample(range(2 ** n), k)
        cols = random.sample(range(2 ** n), k)
        disj_matrix = generate_disjointness_matrix(n, rows, cols)
        random_matrix = generate_random_matrix(k, k)

        char_poly_disj = characteristic_poly(disj_matrix)
        char_poly_random = characteristic_poly(random_matrix)

        nu2_disj.append(compute_nu2(char_poly_disj))
        nu2_random.append(compute_nu2(char_poly_random))
        instances_tested += 1

    median_disj = sorted(nu2_disj)[len(nu2_disj) // 2]
    median_random = sorted(nu2_random)[len(nu2_random) // 2]

    if median_disj < 1.5 * median_random:
        conjecture_holds = False
        counterexample = f"median_disj={median_disj} < 1.5 * median_random={median_random}"

    log_medians_disj = [math.log(m) for m in nu2_disj]
    log_n_values = [math.log(n) for n in n_values]

    slope = compute_slope(log_n_values, log_medians_disj)
    if not (0.35 <= slope <= 0.75):
        conjecture_holds = False
        counterexample = f"slope={slope} not in (0.35, 0.75)"

    return {
        "metric_name": "nu2_disj",
        "metric_value": median_disj,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_slope(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    return slope

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            first_failing_seed = seed
            break

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for seed in seeds if run_trial(seed)["conjecture_holds"]) / len(seeds)

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')