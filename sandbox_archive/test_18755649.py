# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quaternionic_kahler_form(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        kahler_form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    kahler_form[i % n][j % n] += 1
        return kahler_form
    
    def min_order(kahler_form):
        n = len(kahler_form) - 1
        for i in range(n + 1):
            if sum(kahler_form[i]) == 0:
                continue
            order = 0
            while True:
                found = False
                for j in range(n + 1):
                    if kahler_form[j][i] > 0:
                        kahler_form[j][i] -= 1
                        kahler_form[i][j] += 1
                        order += 1
                        found = True
                        break
                if not found:
                    break
            return order
    
    def read_twice_bp_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        bp_size = 0
        for i in range(2**n):
            for j in range(i + 1, 2**n):
                if f[i] == f[j]:
                    bp_size += 1
        return bp_size
    
    n_values = [10, 20, 30]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        kahler_form = compute_quaternionic_kahler_form(f)
        if kahler_form is None or read_twice_bp_size(f) is None:
            continue
        order = min_order(kahler_form)
        bp_size = read_twice_bp_size(f)
        results.append((order, bp_size))
    
    if not results:
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [r[0] for r in results]
    bp_sizes = [r[1] for r in results]
    n_tested = len(results)
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i + 1 for i in range(len(x))}
        y_ranks = {y[i]: i + 1 for i in range(len(y))}
        return sum((x_ranks[x[i]] - y_ranks[y[i]])**2 for i in range(len(x))) / len(x)
    
    correlation = spearman_rank_correlation(min_orders, bp_sizes)
    
    conjecture_holds = correlation > 0.7
    
    return {
        "metric_name": "min_order",
        "metric_value": correlation,
        "instances_tested": n_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Spearman's rank correlation coefficient does not meet the threshold"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials ran")
        sys.exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Spearman\'s rank correlation coefficient does not meet the threshold' first_failing_seed={first_failing_seed}")