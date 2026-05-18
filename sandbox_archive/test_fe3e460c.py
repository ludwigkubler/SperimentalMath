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
from fractions import Fraction
from itertools import product

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def generate_function(n, seed, func_type):
    random.seed(seed)
    if func_type == "constant":
        return lambda x: random.randint(0, 1)
    elif func_type == "x_1":
        return lambda x: x[0]
    elif func_type == "AND_n":
        return lambda x: all(x)
    elif func_type == "OR_n":
        return lambda x: any(x)
    elif func_type == "PARITY_n":
        return lambda x: sum(x) % 2
    elif func_type == "MAJ_n":
        return lambda x: sum(x) > n // 2
    elif func_type == "ADDR_k":
        k = random.randint(2, n)
        return lambda x: x[:k] == [1] * k
    elif func_type.startswith("random-k-junta"):
        k = int(func_type.split("-")[-1])
        indices = random.sample(range(n), k)
        return lambda x: sum(x[i] for i in indices) % 2
    elif func_type.startswith("recursive-AND-OR-tree"):
        depth = int(func_type.split("-")[-1])
        def recursive_tree(x, current_depth):
            if current_depth == depth:
                return random.choice([0, 1])
            if current_depth % 2 == 0:
                return all(recursive_tree(x, current_depth + 1) for _ in range(2))
            else:
                return any(recursive_tree(x, current_depth + 1) for _ in range(2))
        return lambda x: recursive_tree(x, 0)
    else:
        return lambda x: random.randint(0, 1)

def compute_D(f, n, memo={}):
    key = tuple(f(x) for x in product([0, 1], repeat=n))
    if key in memo:
        return memo[key]
    if all(v == key[0] for v in key):
        memo[key] = 0
        return 0
    D = float('inf')
    for i in range(n):
        for b in [0, 1]:
            new_f = lambda x: f(x[:i] + (b,) + x[i+1:])
            D = min(D, compute_D(new_f, n, memo))
    memo[key] = D + 1
    return D + 1

def build_M_f(f, n):
    M_f = []
    for a in product([0, 1], repeat=n):
        row = []
        for b in product([0, 1], repeat=n):
            row.append(f(xor(a, b)))
        M_f.append(row)
    return M_f

def count_distinct_substrings(row, n):
    substrings = set()
    for i in range(len(row) - n + 1):
        substrings.add(tuple(row[i:i+n]))
    return len(substrings)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10]
    func_types = [
        "constant", "x_1", "AND_n", "OR_n", "PARITY_n", "MAJ_n",
        "ADDR_k", "random-k-junta-2", "random-k-junta-4", "random-k-junta-6", "random-k-junta-8",
        "recursive-AND-OR-tree-2", "recursive-AND-OR-tree-3"
    ]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for func_type in func_types:
            f = generate_function(n, seed, func_type)
            D_f = compute_D(f, n)
            M_f = build_M_f(f, n)
            SC_f = 0
            for row in M_f:
                p_a = count_distinct_substrings(row, n)
                SC_f += p_a
            SC_f /= 2 ** n
            instances_tested += 1
            if SC_f > n * 2 ** D_f:
                conjecture_holds = False
                counterexample = f"n={n}, func_type={func_type}, SC_f={SC_f}, D_f={D_f}"
                break
            metric_values.append(math.log2(SC_f) - D_f - math.log2(n))

    if not conjecture_holds:
        return {
            "metric_name": "log2(SC(f)) - D(f) - log2(n)",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    # Calculate Pearson correlation
    D_values = []
    log_SC_values = []
    for n in n_values:
        for func_type in func_types:
            f = generate_function(n, seed, func_type)
            D_f = compute_D(f, n)
            M_f = build_M_f(f, n)
            SC_f = 0
            for row in M_f:
                p_a = count_distinct_substrings(row, n)
                SC_f += p_a
            SC_f /= 2 ** n
            D_values.append(D_f)
            log_SC_values.append(math.log2(SC_f))

    n = len(D_values)
    sum_D = sum(D_values)
    sum_log_SC = sum(log_SC_values)
    sum_D_log_SC = sum(d * s for d, s in zip(D_values, log_SC_values))
    sum_D_sq = sum(d ** 2 for d in D_values)
    sum_log_SC_sq = sum(s ** 2 for s in log_SC_values)

    numerator = sum_D_log_SC - (sum_D * sum_log_SC) / n
    denominator = math.sqrt((sum_D_sq - (sum_D ** 2) / n) * (sum_log_SC_sq - (sum_log_SC ** 2) / n))

    if denominator == 0:
        r = 0
    else:
        r = numerator / denominator

    if r < 0.6:
        conjecture_holds = False
        counterexample = f"Pearson correlation r={r} < 0.6"

    return {
        "metric_name": "log2(SC(f)) - D(f) - log2(n)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')