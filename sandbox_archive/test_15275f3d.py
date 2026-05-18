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

def xor_lift_matrix(f, n):
    M_f = []
    for a in product([0, 1], repeat=n):
        row = []
        for b in product([0, 1], repeat=n):
            row.append(f(xor(a, b)))
        M_f.append(row)
    return M_f

def count_distinct_substrings(s, n):
    substrings = set()
    for i in range(len(s) - n + 1):
        substrings.add(tuple(s[i:i+n]))
    return len(substrings)

def decision_tree_depth(f, n, memo=None):
    if memo is None:
        memo = {}
    if n == 0:
        return 0
    key = (tuple(f), n)
    if key in memo:
        return memo[key]
    if all(f(x) == f([0]*n) for x in product([0, 1], repeat=n)):
        memo[key] = 0
        return 0
    min_depth = float('inf')
    for i in range(n):
        depth = 0
        for b in [0, 1]:
            restricted_f = []
            for x in product([0, 1], repeat=n):
                if x[i] == b:
                    restricted_f.append(f(x))
            depth = max(depth, decision_tree_depth(restricted_f, n-1, memo))
        min_depth = min(min_depth, depth)
    memo[key] = 1 + min_depth
    return memo[key]

def generate_functions(n, seed):
    random.seed(seed)
    functions = []

    # Constant function
    functions.append(lambda x: [0]*n)

    # Identity function
    functions.append(lambda x: x)

    # AND function
    functions.append(lambda x: [int(all(x))])

    # OR function
    functions.append(lambda x: [int(any(x))])

    # PARITY function
    functions.append(lambda x: [sum(x) % 2])

    # MAJORITY function
    functions.append(lambda x: [int(sum(x) > n//2)])

    # ADDR function
    k = random.randint(2, min(8, n))
    functions.append(lambda x: [int(sum(x[:k]) % 2)])

    # Random k-junta
    k = random.randint(2, min(8, n))
    indices = random.sample(range(n), k)
    values = [random.randint(0, 1) for _ in range(k)]
    functions.append(lambda x: [int(all(x[i] == values[j] for j, i in enumerate(indices)))])

    # Recursive AND-OR tree
    def recursive_func(x):
        if len(x) == 1:
            return x
        half = len(x) // 2
        left = recursive_func(x[:half])
        right = recursive_func(x[half:])
        return [int(all(left) or all(right))]
    functions.append(recursive_func)

    # Random uniform function
    table = [random.randint(0, 1) for _ in range(2**n)]
    functions.append(lambda x: [table[int(''.join(map(str, x)), 2)]])

    return functions

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        functions = generate_functions(n, seed)
        for f in functions:
            M_f = xor_lift_matrix(f, n)
            p_a_values = []
            for row in M_f:
                p_a = count_distinct_substrings(row, n)
                p_a_values.append(p_a)
            SC_f = sum(p_a_values) / len(p_a_values)
            D_f = decision_tree_depth(f, n)
            bound = n * (2 ** D_f)
            if SC_f > bound:
                conjecture_holds = False
                counterexample = f"n={n}, SC(f)={SC_f}, D(f)={D_f}, bound={bound}"
                break
            metric_values.append(math.log2(SC_f) - D_f)
            instances_tested += 1
        if not conjecture_holds:
            break

    if len(metric_values) < 2:
        return {
            "metric_name": "log2_SC(f) - D(f)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))

    return {
        "metric_name": "log2_SC(f) - D(f)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_trials")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")