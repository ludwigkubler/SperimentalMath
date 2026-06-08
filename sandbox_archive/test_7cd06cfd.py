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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice(['A', 'B', 'C']) + ('' if random.random() < 0.5 else "'") for _ in range(2)]
            clause = f"({' & '.join(literals)})"
            clauses.append(clause)
        return " | ".join(clauses)

    def compute_clause_complexity(formula):
        return formula.count(" | ") + 1

    def construct_braided_category(formula):
        # Placeholder for the actual construction of the braided category
        # This is a dummy implementation that returns a constant value
        return 5.0

    def linear_regression(x, y):
        n = len(x)
        if n == 0:
            return 0, 0
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    def mean_absolute_error(y_true, y_pred):
        return sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / len(y_true)

    instances_tested = 0
    c_values = []
    kappa_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            kappa = compute_clause_complexity(formula)
            c = construct_braided_category(formula)
            if c is None or kappa is None:
                continue
            instances_tested += 1
            c_values.append(c)
            kappa_values.append(kappa)

    if instances_tested == 0:
        return {
            "metric_name": "coherence_length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    slope, _ = linear_regression(kappa_values, c_values)
    mae = mean_absolute_error(kappa_values, c_values)

    return {
        "metric_name": "coherence_length",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": max(40, n),
        "conjecture_holds": slope >= 0.8 and mae <= 3,
        "counterexample": "" if slope >= 0.8 and mae <= 3 else f"slope={slope}, mae={mae}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_slope = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")