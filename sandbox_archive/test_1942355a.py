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
        return lambda x: sum(x[:k]) % 2
    elif func_type == "random_k_junta":
        k = random.randint(2, n)
        indices = random.sample(range(n), k)
        return lambda x: sum(x[i] for i in indices) % 2
    elif func_type == "recursive_AND_OR":
        depth = random.randint(2, 4)
        def recursive_func(x):
            if depth == 1:
                return x[0]
            else:
                half = len(x) // 2
                left = recursive_func(x[:half])
                right = recursive_func(x[half:])
                return left and right if depth % 2 == 0 else left or right
        return recursive_func
    else:
        return lambda x: random.randint(0, 1)

def compute_decision_tree_depth(f, n):
    memo = {}
    def dt_depth(assignment):
        if tuple(assignment) in memo:
            return memo[tuple(assignment)]
        if all(v is not None for v in assignment):
            return 0
        for i in range(n):
            if assignment[i] is None:
                depth = 1 + max(
                    dt_depth(assignment[:i] + (0,) + assignment[i+1:]),
                    dt_depth(assignment[:i] + (1,) + assignment[i+1:])
                )
                memo[tuple(assignment)] = depth
                return depth
    return dt_depth(tuple([None] * n))

def xor_lift_matrix(f, n):
    M = []
    for a in itertools.product([0, 1], repeat=n):
        row = []
        for b in itertools.product([0, 1], repeat=n):
            xor = tuple((a_i + b_i) % 2 for a_i, b_i in zip(a, b))
            row.append(f(xor))
        M.append(row)
    return M

def count_distinct_substrings(row, n):
    substrings = set()
    for i in range(len(row) - n + 1):
        substrings.add(tuple(row[i:i+n]))
    return len(substrings)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10]
    func_types = ["constant", "x_1", "AND_n", "OR_n", "PARITY_n", "MAJ_n", "ADDR_k", "random_k_junta", "recursive_AND_OR"]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for func_type in func_types:
            f = generate_function(n, seed, func_type)
            D_f = compute_decision_tree_depth(f, n)
            M_f = xor_lift_matrix(f, n)
            p_a_values = []
            for row in M_f:
                p_a = count_distinct_substrings(row, n)
                p_a_values.append(p_a)
            SC_f = sum(p_a_values) / (2 ** n)
            instances_tested += 1
            if SC_f > n * (2 ** D_f):
                conjecture_holds = False
                counterexample = f"n={n}, func_type={func_type}, SC_f={SC_f}, D_f={D_f}"
                break
            metric_values.append(math.log2(SC_f) - D_f - math.log2(n))

    if conjecture_holds:
        if len(metric_values) < 2:
            return {
                "metric_name": "log2(SC(f)) - D(f) - log2(n)",
                "metric_value": 0.0,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        if mean > 0 or std == 0:
            return {
                "metric_name": "log2(SC(f)) - D(f) - log2(n)",
                "metric_value": mean,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }

    return {
        "metric_name": "log2(SC(f)) - D(f) - log2(n)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
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
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        instances_tested += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = trial["counterexample"]

    mean = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials) if trials else 0.0

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')