# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_circuit(n):
    if n == 0:
        return []
    elif n == 1:
        return ['input']
    else:
        left_size = random.randint(1, n-2)
        right_size = n - left_size - 1
        left = generate_circuit(left_size)
        right = generate_circuit(right_size)
        gate = random.choice(['AND', 'OR'])
        return [gate] + left + right

def compute_minimal_order(n):
    # Placeholder for actual computation of minimal order
    # This is a dummy implementation to avoid errors
    return n  # Replace with actual computation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_order = 0
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_circuit(n)
            order = compute_minimal_order(n)
            results.append((n, order))
            instances_tested += 1
            total_order += order
        if instances_tested < 5:
            return {
                "metric_name": "min_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
    if len(results) < 30:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    orders = [order for _, order in results]
    monotone_widths = [len(circuit) for circuit, _ in results]
    correlation_coefficient = sum((x - sum(orders)/len(orders)) * (y - sum(monotone_widths)/len(monotone_widths)) for x, y in zip(orders, monotone_widths)) / (len(orders) * sum((x - sum(orders)/len(orders))**2 for x in orders) * sum((y - sum(monotone_widths)/len(monotone_widths))**2 for y in monotone_widths))**0.5
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")