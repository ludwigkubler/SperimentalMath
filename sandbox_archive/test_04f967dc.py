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
from fractions import Fraction
from math import gcd

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + sum(1 for j in range(i, m) if abs(A[j][i]) > abs(A[i][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(matrix):
        rref = gaussian_elimination([row[:] for row in matrix])
        return sum(1 for row in rref if any(row[i] != 0 for i in range(len(row))))
    
    def random_read_twice_bp(depth, n_vars):
        bp = []
        for _ in range(depth):
            layer = [random.choice([-1, 1]) for _ in range(n_vars)]
            bp.append(layer)
        return bp
    
    def defining_polynomial(bp):
        n_vars = len(bp[0])
        poly = [[Fraction(0) for _ in range(n_vars)] for _ in range(n_vars)]
        for layer in bp:
            for i, val in enumerate(layer):
                if val == 1:
                    for j in range(n_vars):
                        poly[i][j] += Fraction(1)
                elif val == -1:
                    for j in range(n_vars):
                        poly[j][i] -= Fraction(1)
        return poly
    
    def hodge_diamond(poly):
        n = len(poly)
        diamond = [[Fraction(0)] * (2*n-1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    diamond[i][n-i] += poly[i][j]
                elif i > j:
                    diamond[i-j][n-i] += poly[i][j]
                else:
                    diamond[n-1-(i+j)][n-i] -= poly[i][j]
        return diamond
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def mean_absolute_error(slope, intercept, x, y):
        return sum(abs(yi - (slope * xi + intercept)) for xi, yi in zip(x, y))
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    for depth in depths:
        for _ in range(20):
            bp = random_read_twice_bp(depth, n_vars=depth)
            poly = defining_polynomial(bp)
            diamond = hodge_diamond(poly)
            rank_value = rank(diamond)
            results.append((depth, rank_value))
    
    x, y = zip(*results)
    slope, intercept = linear_regression(x, y)
    mae = mean_absolute_error(slope, intercept, x, y)
    
    return {
        "metric_name": "mean_absolute_error",
        "metric_value": mae,
        "instances_tested": len(results),
        "conjecture_holds": mae <= 5 and slope >= 0.8 * depth,
        "counterexample": "" if mae <= 5 else f"MAE={mae}, Slope={slope}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mae = sum(r["metric_value"] for r in results) / len(results)
    std_mae = (sum((r["metric_value"] - mean_mae) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mae} std={std_mae} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mae} std={std_mae} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='MAE too high' first_failing_seed={first_failing_seed}")