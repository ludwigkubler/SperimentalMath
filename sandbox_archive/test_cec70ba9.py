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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(-A[i][i], A[i][i])
        for j in range(n):
            if i != j:
                factor = Fraction(-A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] += factor * A[i][k]
    return A

def resolution_width(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                A[i][literal - 1] = 1
            else:
                A[i][-1] += 1
    gaussian_elimination(A)
    width = max(sum(row) for row in A)
    return width

def tseitin_formula(graph, d):
    n = len(graph)
    clauses = []
    literals = {}
    for i in range(n):
        literals[i] = random.randint(1, 2*n)
        neg_i = -literals[i]
        clauses.append([literals[i]])
        for j in graph[i]:
            if j != i:
                clauses.append([neg_i, literals[j]])
                clauses.append([neg_i, -literals[j]])
    return clauses

def geometric_quantization(graph):
    n = len(graph)
    rho = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            if i != j:
                rho[i][j] = Fraction(1, 2*n)
    return rho

def norm(rho):
    n = len(rho)
    sum_squares = 0
    for i in range(n):
        for j in range(n):
            sum_squares += rho[i][j] ** 2
    return math.sqrt(sum_squares)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            continue

        graph = [[] for _ in range(n)]
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while len(neighbors) < d:
                neighbors.append(random.randint(0, n-1))
            graph[i] = list(set(neighbors))

        clauses = tseitin_formula(graph, d)
        width = resolution_width(clauses)

        rho = geometric_quantization(graph)
        norm_rho = norm(rho)

        instances_tested += 1
        metric_values.append((width, norm_rho))

    if instances_tested < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation_coefficient = 0
    for width, norm_rho in metric_values:
        if width == 0 or norm_rho == 0:
            continue
        correlation_coefficient += (width / norm_rho)
    correlation_coefficient /= instances_tested

    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"

    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")