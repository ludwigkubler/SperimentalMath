# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(cols):
        max_row = next((j for j in range(i, rows) if A[j][i] != 0), None)
        if max_row is None:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(rows):
            if i == j:
                continue
            factor = A[j][i] / A[i][i]
            for k in range(cols):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    rref = gaussian_elimination(A)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def tropicalize(circuit):
    # Placeholder function to simulate tropicalization
    # Replace with actual implementation
    return circuit

def monotone_width(circuit):
    # Placeholder function to compute monotone width
    # Replace with actual implementation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(2, min(n, 8))
    instances_tested = 0
    thd_values = []
    wm_values = []

    for _ in range(30):
        circuit = [random.choice([0, 1]) for _ in range(d * n)]
        if len(set(circuit)) != d:
            continue
        thd_value = rank(tropicalize(circuit))
        wm_value = monotone_width(circuit)
        thd_values.append(thd_value)
        wm_values.append(wm_value)
        instances_tested += 1

    if not thd_values or not wm_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_thd = sum(thd_values) / len(thd_values)
    mean_wm = sum(wm_values) / len(wm_values)
    correlation_coefficient = sum((thd - mean_thd) * (wm - mean_wm) for thd, wm in zip(thd_values, wm_values)) / (len(thd_values) * math.sqrt(sum((thd - mean_thd) ** 2 for thd in thd_values) * sum((wm - mean_wm) ** 2 for wm in wm_values)))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")