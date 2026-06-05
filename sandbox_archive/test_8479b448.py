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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_quasi_random_sequence(n):
    return [random.randint(0, 1) for _ in range(n)]

def binary_string_to_boolean_function(binary_str):
    def f(x):
        index = int(''.join(str(bit) for bit in x), 2)
        return binary_str[index]
    return f

def circuit_monotone_width(f, n):
    max_ones = 0
    current_ones = 0
    for i in range(1 << n):
        if f(i) == 1:
            current_ones += 1
            max_ones = max(max_ones, current_ones)
        else:
            current_ones = 0
    return max_ones

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    all_orders = []
    all_widths = []

    for n in n_values:
        sequence = generate_quasi_random_sequence(n)
        binary_str = ''.join(str(bit) for bit in sequence)
        f = binary_string_to_boolean_function(binary_str)
        order = len(sequence)
        width = circuit_monotone_width(f, n)
        all_orders.append(order)
        all_widths.append(width)

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(all_orders, all_widths)) / (len(all_orders) * std_dev_x * std_dev_y)
    mean_order = sum(all_orders) / len(all_orders)
    std_dev_order = math.sqrt(sum((x - mean_order) ** 2 for x in all_orders) / len(all_orders))
    mean_width = sum(all_widths) / len(all_widths)
    std_dev_width = math.sqrt(sum((y - mean_width) ** 2 for y in all_widths) / len(all_widths))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")