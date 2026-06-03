# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def circuit_monotone_width(f):
    n = int(math.log2(len(f)))
    width = 0
    for i in range(1 << n):
        if any(f[i] > f[j] for j in range(i) if (i & (1 << j)) == 0):
            width += 1
    return width

def grothendieck_group_order(f):
    n = int(math.log2(len(f)))
    G = [0] * (1 << n)
    G[0] = 1
    for i in range(1, 1 << n):
        for j in range(n):
            if i & (1 << j) != 0:
                G[i] += G[i ^ (1 << j)]
    return sum(G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            w_f = circuit_monotone_width(f)
            order = grothendieck_group_order(f)
            results.append((n, w_f, math.log(order)))
    if not results:
        return {
            "metric_name": "log_grothendieck_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    log_grothendieck_group_orders = [log_order for _, _, log_order in results]
    w_f_values = [w_f for _, w_f, _ in results]
    mean_log_grothendieck_group_order = sum(log_grothendieck_group_orders) / instances_tested
    mean_w_f = sum(w_f_values) / instances_tested
    correlation_coefficient = (sum((log_grothendieck_group_orders[i] - mean_log_grothendieck_group_order) * (w_f_values[i] - mean_w_f) for i in range(instances_tested)) /
                               math.sqrt(sum((log_grothendieck_group_orders[i] - mean_log_grothendieck_group_order)**2 for i in range(instances_tested)) *
                                         sum((w_f_values[i] - mean_w_f)**2 for i in range(instances_tested))))
    conjecture_holds = abs(correlation_coefficient) >= 0.95
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    return {
        "metric_name": "log_grothendieck_group_order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"RESULT: FALSIFIED counterexample=\"correlation_coefficient={result['metric_value']}\" first_failing_seed={first_failing_seed}"
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    print(RESULT)