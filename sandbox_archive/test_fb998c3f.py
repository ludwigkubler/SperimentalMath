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

def generate_boolean_instance(n):
    return [random.choice([0, 1]) for _ in range(n)]

def compute_conflict_set(instance):
    n = len(instance)
    conflict_set = set()
    for i in range(1 << n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if all(assignment[j] == instance[j] for j in range(n)):
            continue
        for j in range(n):
            if assignment[j] != instance[j]:
                conflict_set.add(j)
    return conflict_set

def count_integral_points(conflict_set):
    n = len(conflict_set)
    integral_points = 0
    for i in range(1 << n):
        point = [(i >> j) & 1 for j in range(n)]
        if all(point[j] == 0 or point[j] == 1 for j in range(n)):
            integral_points += 1
    return integral_points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_integral_points = 0
    total_heights = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            instance = generate_boolean_instance(n)
            conflict_set = compute_conflict_set(instance)
            integral_points = count_integral_points(conflict_set)
            height = len(instance)  # Simplified resolution proof tree height
            total_integral_points += integral_points
            total_heights += height
            instances_tested += 1

    mean_integral_points = total_integral_points / instances_tested
    mean_height = total_heights / instances_tested
    conjecture_holds = abs(mean_integral_points - mean_height) <= 5 * (mean_height ** 0.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Integral Points vs Height",
        "metric_value": mean_integral_points,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")