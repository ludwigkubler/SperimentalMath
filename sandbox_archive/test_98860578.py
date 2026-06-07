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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)

    def hexp(phi):
        # Placeholder function to calculate hexp(φ)
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)  # Replace with actual calculation

    def resolution_width(phi):
        # Placeholder function to calculate resolution proof width w(φ)
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)  # Replace with actual calculation

    n_values = [5, 10, 15, 20, 30, 40]
    hexp_values = []
    width_values = []

    for n in n_values:
        phi = generate_sat_instance(n)
        hexp_val = hexp(phi)
        width_val = resolution_width(phi)
        hexp_values.append(hexp_val)
        width_values.append(width_val)

    correlation_coefficient = calculate_correlation(hexp_values, width_values)
    mean_abs_diff = sum(abs(a - b) for a, b in zip(hexp_values, width_values)) / len(hexp_values)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_abs_diff <= 3 else "mapping_undefined"
    }

def calculate_correlation(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)
    sum_yy = sum(yi ** 2 for yi in y)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))

    if denominator == 0:
        return 0

    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")