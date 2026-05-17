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

def generate_random_matrix(n, rho, seed):
    random.seed(seed)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() < rho:
                matrix[i][j] = 1
    return matrix

def perm_n(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    if n == 1:
        return matrix[0][0]
    total = 0
    for j in range(n):
        if matrix[0][j] == 1:
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            total += perm_n(submatrix)
    return total

def enumerate_permutations(matrix):
    n = len(matrix)
    permutations = []
    stack = [(0, [])]

    while stack:
        i, current = stack.pop()
        if i == n:
            permutations.append(current)
            continue
        for j in range(n):
            if matrix[i][j] == 1:
                new_current = current + [j]
                stack.append((i + 1, new_current))
    return permutations

def cycle_type(perm):
    n = len(perm)
    visited = [False] * n
    cycles = []

    for i in range(n):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(cycle)

    cycle_lengths = [len(cycle) for cycle in cycles]
    cycle_lengths.sort(reverse=True)
    return tuple(cycle_lengths)

def murnaghan_nakayama(n, lambda_):
    if n == 0:
        return 1 if lambda_ == () else 0
    total = 0
    for i in range(len(lambda_)):
        new_lambda = lambda_[:i] + (lambda_[i] - 1,) + lambda_[i+1:]
        new_lambda = tuple(sorted(filter(lambda x: x > 0, new_lambda), reverse=True))
        total += (-1)**(n - 1 - i) * murnaghan_nakayama(n - 1, new_lambda)
    return total

def immanant(matrix, lambda_):
    n = len(matrix)
    if n != len(lambda_):
        return 0
    if n == 0:
        return 1
    total = 0
    for perm in enumerate_permutations(matrix):
        if cycle_type(perm) == lambda_:
            sign = 1
            for i in range(n):
                for j in range(i + 1, n):
                    if perm[i] > perm[j]:
                        sign *= -1
            total += sign
    return total

def w(S):
    n = len(S)
    lambda_values = list(itertools.product(*[range(n + 1)] * n))
    lambda_values = [tuple(sorted(l, reverse=True)) for l in lambda_values if sum(l) == n]
    unique_lambda = set(lambda_values)
    count = 0
    for lambda_ in unique_lambda:
        if immanant(S, lambda_) > 0:
            count += 1
    return count

def generate_covers(n, max_covers):
    covers = []
    for _ in range(max_covers):
        cover = set()
        for i in range(n - 1):
            cover.add((i, random.randint(0, n - 1)))
        covers.append(cover)
    return covers

def d_KW(S, covers):
    n = len(S)
    sigma = enumerate_permutations(S)
    if not sigma:
        return 0
    edges = set()
    for s in sigma:
        for i in range(n):
            edges.add((i, s[i]))
    max_depth = 0
    for cover in covers:
        depth = 0
        remaining_edges = edges.copy()
        while remaining_edges:
            hit_edges = set()
            for edge in remaining_edges:
                if edge in cover:
                    hit_edges.add(edge)
            if not hit_edges:
                break
            remaining_edges -= hit_edges
            depth += 1
        max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed):
    n_values = [3, 4, 5, 6]
    rho_values = [0.4, 0.6, 0.8]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for rho in rho_values:
            S = generate_random_matrix(n, rho, seed)
            if perm_n(S) == 0:
                continue
            instances_tested += 1
            sigma = enumerate_permutations(S)
            if not sigma:
                continue
            w_S = w(S)
            covers = generate_covers(n, 1500)
            d_KW_S = d_KW(S, covers)
            metric_values.append(d_KW_S - math.ceil(math.log2(w_S)))
            if d_KW_S < math.ceil(math.log2(w_S)):
                conjecture_holds = False
                counterexample = f"n={n}, rho={rho}, d_KW={d_KW_S}, w={w_S}"

    if not metric_values:
        return {
            "metric_name": "d_KW - log2(w)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "d_KW - log2(w)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    seeds = [int(seed) for seed in seeds]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += result["instances_tested"]
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.95 and mean_metric >= 0:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")