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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank(phi):
    n = int(math.log2(len(phi)))
    # Simplified version of a known algorithm for communication complexity rank
    # This is a placeholder and should be replaced with the actual algorithm
    return n

def l_function_arithmetic(phi):
    # Placeholder for L-Function arithmetic computation
    # This is a placeholder and should be replaced with the actual computation
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_boolean_function(n)
        r_phi = communication_complexity_rank(phi)
        order_k = l_function_arithmetic(phi)

        if r_phi == 0 or order_k == 0:
            continue

        instances_tested += 1
        n_max = max(n_max, n)
        metric_values.append((r_phi, order_k))

    if len(metric_values) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    r_phi, order_k = zip(*metric_values)
    correlation_coefficient = sum((x - y) * (x - y) for x, y in zip(r_phi, order_k)) / len(metric_values)
    mean_absolute_difference = sum(abs(x - y) for x, y in zip(r_phi, order_k)) / len(metric_values)

    if correlation_coefficient < 0.5 or mean_absolute_difference > 3:
        conjecture_holds = False
        counterexample = "Correlation coefficient too low or mean absolute difference too high"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")