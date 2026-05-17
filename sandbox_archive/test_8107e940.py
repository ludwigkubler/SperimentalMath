# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_matrix(n, rho, seed):
    random.seed(seed)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() < rho:
                matrix[i][j] = 1
    return matrix

def perm_n(matrix):
    n = len(matrix)
    count = 0
    for perm in itertools.permutations(range(n)):
        valid = True
        for i in range(n):
            if matrix[i][perm[i]] == 0:
                valid = False
                break
        if valid:
            count += 1
    return count

def cycle_type(perm):
    visited = [False] * len(perm)
    cycles = []
    for i in range(len(perm)):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(len(cycle))
    return tuple(sorted(cycles))

def murnaghan_nakayama(n, lambda_):
    if n == 0:
        return 1 if lambda_ == () else 0
    total = 0
    for k in range(len(lambda_)):
        new_lambda = list(lambda_)
        new_lambda[k] -= 1
        new_lambda = tuple(sorted([x for x in new_lambda if x > 0], reverse=True))
        total += (-1)**k * murnaghan_nakayama(n-1, new_lambda)
    return total

def imm_lambda(matrix, lambda_):
    n = len(matrix)
    if sum(lambda_) != n:
        return 0
    total = 0
    for perm in itertools.permutations(range(n)):
        if cycle_type(perm) == lambda_:
            product = 1
            for i in range(n):
                product *= matrix[i][perm[i]]
            total += product
    return total

def w_S(matrix):
    n = len(matrix)
    lambda_values = []
    for lambda_ in itertools.product(range(n+1), repeat=n):
        lambda_ = tuple(sorted(lambda_, reverse=True))
        if sum(lambda_) == n:
            lambda_values.append(lambda_)
    unique_lambda = set(lambda_values)
    count = 0
    for lambda_ in unique_lambda:
        if imm_lambda(matrix, lambda_) > 0:
            count += 1
    return count

def generate_covers(matrix, n_covers):
    n = len(matrix)
    covers = []
    for _ in range(n_covers):
        cover = set()
        for i in range(n):
            if random.random() < 0.5:
                cover.add(i)
        covers.append(cover)
    return covers

def d_KW(matrix, covers):
    n = len(matrix)
    max_depth = 0
    for cover in covers:
        depth = 0
        remaining = set(range(n))
        while remaining:
            new_remaining = set()
            for i in remaining:
                if i not in cover:
                    new_remaining.add(i)
            if not new_remaining:
                break
            depth += 1
            remaining = new_remaining
        max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed):
    n = random.choice([3, 4, 5, 6])
    rho = random.choice([0.4, 0.6, 0.8])
    matrix = generate_matrix(n, rho, seed)
    if perm_n(matrix) == 0:
        return {
            "metric_name": "d_KW_minus_log2_w_S",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    w_S_value = w_S(matrix)
    if w_S_value <= 0:
        return {
            "metric_name": "d_KW_minus_log2_w_S",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    covers = generate_covers(matrix, 1500)
    d_KW_value = d_KW(matrix, covers)
    metric_value = d_KW_value - math.ceil(math.log2(w_S_value))
    conjecture_holds = metric_value >= 0
    counterexample = "" if conjecture_holds else f"d_KW({n}) = {d_KW_value} < log2(w_S) = {math.ceil(math.log2(w_S_value))}"
    return {
        "metric_name": "d_KW_minus_log2_w_S",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append((seed, result["counterexample"]))

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0.0

    if counterexamples:
        first_seed, first_counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_seed}")
    elif support_fraction >= 0.95 and mean_metric >= 0.0:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")