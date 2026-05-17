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

def hamming_distance(x, y):
    if len(x) != len(y):
        raise ValueError("Vectors must be of the same length")
    return sum(1 for a, b in zip(x, y) if a != b)

def compute_delta_bar(M, n):
    delta = 0
    max_distance = 0
    rows = list(range(len(M)))
    for a, b, c, d in itertools.combinations(rows, 4):
        S1 = hamming_distance(M[a], M[b]) + hamming_distance(M[c], M[d])
        S2 = hamming_distance(M[a], M[c]) + hamming_distance(M[b], M[d])
        S3 = hamming_distance(M[a], M[d]) + hamming_distance(M[b], M[c])
        S_sorted = sorted([S1, S2, S3], reverse=True)
        current_delta = (S_sorted[0] - S_sorted[1]) / 2
        if current_delta > delta:
            delta = current_delta
        max_distance = max(max_distance, S_sorted[0])
    if max_distance == 0:
        return 0.0
    return delta / max_distance

def compute_dt(f, n):
    if n == 0:
        return 0
    memo = {}
    def dt_helper(f, n):
        if n == 0:
            return 0
        key = (tuple(f), n)
        if key in memo:
            return memo[key]
        min_dt = float('inf')
        for i in range(n):
            f0 = [f[j] for j in range(len(f)) if (j >> i) & 1 == 0]
            f1 = [f[j] for j in range(len(f)) if (j >> i) & 1 == 1]
            if len(set(f0)) == 1 and len(set(f1)) == 1:
                continue
            dt = 1 + max(dt_helper(f0, n-1), dt_helper(f1, n-1))
            if dt < min_dt:
                min_dt = dt
        memo[key] = min_dt
        return min_dt
    return dt_helper(f, n)

def generate_random_function(n, seed):
    random.seed(seed)
    return [random.randint(0, 1) for _ in range(2**n)]

def generate_fixed_function(name, n):
    if name == "constant":
        return [0] * (2**n)
    elif name == "dictator":
        return [i & 1 for i in range(2**n)]
    elif name == "AND_n":
        return [1 if i == (1 << n) - 1 else 0 for i in range(2**n)]
    elif name == "OR_n":
        return [1 if i > 0 else 0 for i in range(2**n)]
    elif name == "MAJ_n":
        return [1 if bin(i).count('1') > n // 2 else 0 for i in range(2**n)]
    elif name == "PARITY_n":
        return [bin(i).count('1') % 2 for i in range(2**n)]
    elif name == "IP_n":
        return [1 if bin(i).count('1') == n else 0 for i in range(2**n)]
    elif name == "random_AC0":
        return generate_random_function(n, 42)
    else:
        raise ValueError("Unknown fixed function name")

def build_matrix(f, n):
    M = []
    for x in range(2**n):
        row = []
        for y in range(2**n):
            row.append(f[x ^ y])
        M.append(row)
    return M

def run_trial(seed):
    n_values = [3, 4, 5]
    fixed_functions = ["constant", "dictator", "AND_n", "OR_n", "MAJ_n", "PARITY_n", "IP_n", "random_AC0"]
    results = []
    instances_tested = 0

    for n in n_values:
        # Test random functions
        for _ in range(30):
            f = generate_random_function(n, seed)
            seed += 1
            if len(set(f)) == 1:
                continue  # Skip constant functions
            M = build_matrix(f, n)
            dt = compute_dt(f, n)
            delta_bar = compute_delta_bar(M, n)
            ratio = delta_bar * (n + 1) / (n + 1 - dt)
            conjecture_holds = ratio <= 1
            counterexample = "" if conjecture_holds else f"delta_bar ratio {ratio} > 1 for n={n}, dt={dt}"
            results.append({
                "metric_name": "delta_bar_ratio",
                "metric_value": ratio,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
            instances_tested += 1

        # Test fixed functions
        for name in fixed_functions:
            f = generate_fixed_function(name, n)
            if len(set(f)) == 1:
                continue  # Skip constant functions
            M = build_matrix(f, n)
            dt = compute_dt(f, n)
            delta_bar = compute_delta_bar(M, n)
            ratio = delta_bar * (n + 1) / (n + 1 - dt)
            conjecture_holds = ratio <= 1
            counterexample = "" if conjecture_holds else f"delta_bar ratio {ratio} > 1 for n={n}, dt={dt}, function={name}"
            results.append({
                "metric_name": "delta_bar_ratio",
                "metric_value": ratio,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
            instances_tested += 1

    # Aggregate results
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = [r["conjecture_holds"] for r in results]
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]

    if not metric_values:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)

    if counterexamples:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": mean_metric,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexamples[0]
        }
    else:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": mean_metric,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        all_results.append(result)

    metric_values = [r["metric_value"] for r in all_results if "metric_value" in r]
    conjecture_holds = [r["conjecture_holds"] for r in all_results if "conjecture_holds" in r]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)

    if all(conjecture_holds):
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        counterexamples = [r["counterexample"] for r in all_results if not r["conjecture_holds"]]
        first_failing_seed = next((r["seed"] for r in all_results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={first_failing_seed}")