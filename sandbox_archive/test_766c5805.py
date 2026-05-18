# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from itertools import product

def compute_D(f, n, memo):
    if n == 0:
        return 0
    key = tuple(f(x) for x in product([0, 1], repeat=n))
    if key in memo:
        return memo[key]
    if all(v == key[0] for v in key):
        memo[key] = 0
        return 0
    D = float('inf')
    for i in range(n):
        for b in [0, 1]:
            new_f = lambda x, i=i, b=b: f(x[:i] + (b,) + x[i+1:])
            D = min(D, compute_D(new_f, n-1, memo))
    memo[key] = 1 + D
    return memo[key]

def generate_function(n, seed, func_type):
    random.seed(seed)
    if func_type == 'constant':
        return lambda x: random.randint(0, 1)
    elif func_type == 'x_1':
        return lambda x: x[0]
    elif func_type == 'AND_n':
        return lambda x: all(x)
    elif func_type == 'OR_n':
        return lambda x: any(x)
    elif func_type == 'PARITY_n':
        return lambda x: sum(x) % 2
    elif func_type == 'MAJ_n':
        return lambda x: sum(x) > n // 2
    elif func_type.startswith('ADDR_'):
        k = int(func_type.split('_')[1])
        return lambda x: sum(x[i] * (2 ** i) for i in range(k)) < (2 ** k)
    elif func_type.startswith('random-k-junta'):
        k = int(func_type.split('-')[1])
        indices = random.sample(range(n), k)
        return lambda x: sum(x[i] for i in indices) % 2
    elif func_type.startswith('recursive-AND-OR-tree'):
        d = int(func_type.split('-')[-1])
        def tree_func(x, depth):
            if depth == 0:
                return x[0]
            half = len(x) // 2
            left = tree_func(x[:half], depth-1)
            right = tree_func(x[half:], depth-1)
            return left if depth % 2 == 0 else left or right
        return lambda x: tree_func(x, d)
    else:
        return lambda x: random.randint(0, 1)

def build_M_f(f, n):
    M_f = []
    for a in product([0, 1], repeat=n):
        row = []
        for b in product([0, 1], repeat=n):
            xor = tuple(a_i ^ b_i for a_i, b_i in zip(a, b))
            row.append(f(xor))
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
        'constant', 'x_1', 'AND_n', 'OR_n', 'PARITY_n', 'MAJ_n',
        'ADDR_2', 'ADDR_4', 'ADDR_6', 'ADDR_8',
        'random-k-junta-2', 'random-k-junta-4', 'random-k-junta-6', 'random-k-junta-8',
        'recursive-AND-OR-tree-2', 'recursive-AND-OR-tree-3'
    ]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for func_type in func_types:
            f = generate_function(n, seed, func_type)
            memo = {}
            D = compute_D(f, n, memo)
            M_f = build_M_f(f, n)
            SC_f = 0
            for row in M_f:
                p_a = count_distinct_substrings(row, n)
                SC_f += p_a
            SC_f /= 2 ** n
            bound = n * (2 ** D)
            if SC_f > bound:
                conjecture_holds = False
                counterexample = f"n={n}, func_type={func_type}, SC_f={SC_f}, bound={bound}"
                break
            metric_values.append(math.log2(SC_f) - D)
            instances_tested += 1
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "log2_SC(f) - D(f)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2_SC(f) - D(f)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")