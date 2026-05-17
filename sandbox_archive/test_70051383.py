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
            cycles.append(tuple(sorted(cycle)))
    return tuple(sorted(cycles))

def murnaghan_nakayama(matrix, n):
    imm = defaultdict(int)
    for perm in itertools.permutations(range(n)):
        ct = cycle_type(perm)
        imm[ct] += 1
    return imm

def w(S):
    n = len(S)
    imm = murnaghan_nakayama(S, n)
    return len(imm)

def generate_covers(n, max_covers):
    covers = []
    for _ in range(max_covers):
        cover = set()
        for i in range(n - 1):
            cover.add((i, random.randint(0, n - 1)))
        covers.append(cover)
    return covers

def kw_depth(S, covers):
    n = len(S)
    Sigma = []
    for perm in itertools.permutations(range(n)):
        valid = True
        for i in range(n):
            if S[i][perm[i]] == 0:
                valid = False
                break
        if valid:
            Sigma.append(perm)

    if not Sigma:
        return 0

    depth = 0
    current_level = [Sigma]
    while True:
        next_level = []
        for group in current_level:
            if len(group) == 1:
                continue
            for cover in covers:
                subsets = defaultdict(list)
                for sigma in group:
                    hit = False
                    for (i, j) in cover:
                        if sigma[i] == j:
                            hit = True
                            break
                    if hit:
                        subsets[cover].append(sigma)
                if len(subsets) > 1:
                    for subset in subsets.values():
                        next_level.append(subset)
                    break
        if not next_level:
            break
        current_level = next_level
        depth += 1
    return depth

def run_trial(seed):
    n_values = [3, 4, 5, 6]
    rho_values = [0.4, 0.6, 0.8]
    total_instances = 0
    total_support = 0
    metric_values = []
    counterexamples = []

    for n in n_values:
        for rho in rho_values:
            matrix = generate_random_matrix(n, rho, seed)
            if perm_n(matrix) == 0:
                continue

            total_instances += 1
            w_S = w(matrix)
            covers = generate_covers(n, 1500)
            d_KW = kw_depth(matrix, covers)

            metric_value = d_KW - math.ceil(math.log2(w_S))
            metric_values.append(metric_value)

            if d_KW < math.ceil(math.log2(w_S)):
                counterexamples.append((matrix, n, rho, seed))

            if d_KW >= math.ceil(math.log2(w_S)):
                total_support += 1

    if total_instances == 0:
        return {
            "metric_name": "d_KW - log2(w(S))",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid matrices generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = total_support / total_instances

    if counterexamples:
        counterexample = f"Matrix: {counterexamples[0][0]}, n: {counterexamples[0][1]}, rho: {counterexamples[0][2]}, seed: {counterexamples[0][3]}"
    else:
        counterexample = ""

    return {
        "metric_name": "d_KW - log2(w(S))",
        "metric_value": mean_metric,
        "instances_tested": total_instances,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    total_instances = 0
    total_support = 0
    metric_values = []
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_instances += result["instances_tested"]
        if result["conjecture_holds"]:
            total_support += 1
        metric_values.append(result["metric_value"])
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])

    if total_instances == 0:
        print("RESULT: INCONCLUSIVE reason=no_valid_matrices")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = total_support / len(seeds)

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.95 and mean_metric >= 0:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")