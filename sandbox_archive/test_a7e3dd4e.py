# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
import json
from collections import defaultdict

def xor_tree(n):
    if n == 1:
        return [0]
    left = xor_tree(n // 2)
    right = xor_tree(n // 2)
    return [left[i] ^ right[i] for i in range(n)]

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def bfs_diameter(tree, root):
    queue = [(root, 0)]
    visited = set([root])
    max_dist = 0
    while queue:
        node, dist = queue.pop(0)
        max_dist = max(max_dist, dist)
        for neighbor in range(len(tree)):
            if tree[node] ^ tree[neighbor] == 1 and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return max_dist

def build_cochain_space(tree, R):
    n = len(tree)
    C0 = [[0 for _ in range(n)] for _ in range(n)]
    C1 = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hamming_distance(i, j) <= R:
                C0[i][j] = C0[j][i] = tree[i] ^ tree[j]
                C1[i][j] = C1[j][i] = random.choice([-1, 1])
    return C0, C1

def smith_normal_form(matrix):
    n = len(matrix)
    A = [row[:] for row in matrix]
    R = range(n)
    C = range(n)
    for k in range(n):
        pivot_row = max(R[k:], key=lambda r: abs(A[r][k]))
        A[pivot_row], A[R[k]] = A[R[k]], A[pivot_row]
        pivot_col = max(C[k:], key=lambda c: abs(A[R[k]][c]))
        A[R[k]][pivot_col], A[R[k]][C[k]] = A[R[k]][C[k]], A[R[k]][pivot_col]
        for r in R:
            if r != k:
                factor = A[r][k] / A[k][k]
                for c in C:
                    A[r][c] -= factor * A[k][c]
    return [sum(abs(A[i][j]) for j in C) for i in R]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 16, 32]
    results = []
    for n in n_values:
        tree = xor_tree(n)
        diameter = bfs_diameter(tree, 0)
        R_max = math.floor(0.5 * math.log2(n))
        HX1_R = [0] * (R_max + 1)
        for R in range(R_max + 1):
            C0, C1 = build_cochain_space(tree, R)
            delta_0 = [[sum(C0[i][j] * C0[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
            delta_1 = [[sum(C1[i][j] * C0[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
            ker_delta_1 = [row[:] for row in delta_1]
            im_delta_0 = [row[:] for row in delta_0]
            for r in range(R_max + 1):
                if r != R:
                    factor = sum(ker_delta_1[r][c] * im_delta_0[c][k] for c in range(n)) / sum(im_delta_0[R][c] ** 2 for c in range(n))
                    for k in range(n):
                        ker_delta_1[r][k] -= factor * im_delta_0[R][k]
            HX1_R[R] = len(smith_normal_form(ker_delta_1)) - len(smith_normal_form(im_delta_0))

        if all(HX1_R[:R_max + 1]) and any(HX1_R[R_max + 1:]):
            slope, intercept = 0, 0
            count = 0
            for R in range(R_max + 1, len(HX1_R)):
                if HX1_R[R]:
                    slope += math.log(abs(HX1_R[R])) / math.log(R)
                    intercept += math.log(R)
                    count += 1
            if count > 0:
                slope /= count
                intercept /= count
                results.append({
                    "n": n,
                    "slope": slope,
                    "intercept": intercept
                })

    if not results:
        return {
            "metric_name": "vanishing_threshold",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_slope = sum(result["slope"] for result in results) / len(results)
    std_slope = math.sqrt(sum((result["slope"] - mean_slope) ** 2 for result in results) / len(results))
    correlation = sum((result["slope"] - mean_slope) * (math.log2(result["n"]) - mean_log_n) for result in results) / (len(results) * std_slope * math.sqrt(sum((math.log2(result["n"]) - mean_log_n) ** 2 for result in results)))
    mean_log_n = sum(math.log2(result["n"]) for result in results) / len(results)

    return {
        "metric_name": "vanishing_threshold",
        "metric_value": mean_slope,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.95 and mean_slope >= math.log2(n_values[0]) - 2,
        "counterexample": "" if correlation >= 0.95 else f"correlation={correlation}, mean_slope={mean_slope}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_slope = sum(result["metric_value"] for result in results) / len(results)
    std_slope = math.sqrt(sum((result["metric_value"] - mean_slope) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")