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

def hamming_distance(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)

def compute_dt(f, n):
    if n == 0:
        return 0
    if all(f[x] == f[x[:n-1] + [1-x[n-1]]] for x in itertools.product([0, 1], repeat=n)):
        return compute_dt(lambda x: f(x[:n-1] + [0]), n-1)
    return 1 + min(compute_dt(lambda x: f(x[:i] + [0] + x[i+1:]), n) for i in range(n))

def build_matrix(f, n):
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in itertools.product([0, 1], repeat=n):
        for y in itertools.product([0, 1], repeat=n):
            xor = [a ^ b for a, b in zip(x, y)]
            matrix[int(''.join(map(str, x)), 2)][int(''.join(map(str, y)), 2)] = f(xor)
    return matrix

def compute_delta(matrix, n):
    size = 2 ** n
    rows = [row for row in matrix]
    max_delta = 0
    for a, b, c, d in itertools.combinations(range(size), 4):
        d_ab = hamming_distance(rows[a], rows[b])
        d_cd = hamming_distance(rows[c], rows[d])
        d_ac = hamming_distance(rows[a], rows[c])
        d_bd = hamming_distance(rows[b], rows[d])
        d_ad = hamming_distance(rows[a], rows[d])
        d_bc = hamming_distance(rows[b], rows[c])
        s1 = d_ab + d_cd
        s2 = d_ac + d_bd
        s3 = d_ad + d_bc
        s_sorted = sorted([s1, s2, s3], reverse=True)
        delta = (s_sorted[0] - s_sorted[1]) / 2
        if delta > max_delta:
            max_delta = delta
    return max_delta

def compute_diam(matrix, n):
    size = 2 ** n
    rows = [row for row in matrix]
    max_dist = 0
    for a, b in itertools.combinations(range(size), 2):
        dist = hamming_distance(rows[a], rows[b])
        if dist > max_dist:
            max_dist = dist
    return max_dist

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate a random Boolean function
        f = lambda x: random.randint(0, 1)
        d = compute_dt(f, n)
        if d == 0:
            continue  # Skip constant functions
        matrix = build_matrix(f, n)
        delta = compute_delta(matrix, n)
        diam = compute_diam(matrix, n)
        if diam == 0:
            continue  # Skip if all rows are identical
        delta_bar = delta / diam
        ratio = delta_bar * (n + 1) / (n + 1 - d)
        metric_values.append(ratio)
        instances_tested += 1
        if ratio > 1:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, ratio={ratio}"
            break

    if conjecture_holds:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        instances_tested += result["instances_tested"]
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            break

    if conjecture_holds_all:
        mean = sum(metric_values) / len(metric_values) if metric_values else 0
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    else:
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={seeds[0]}")