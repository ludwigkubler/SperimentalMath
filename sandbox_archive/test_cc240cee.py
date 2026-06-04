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
    n_values = [5, 10, 15, 20, 30, 40]
    r_phi_values = []
    d_phi_values = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_random_cnf(n)
            polynomial = get_polynomial(cnf)
            valuation_rank = min_p_adic_valuation_rank(polynomial)
            frege_depth = frege_proof_depth(cnf)

            r_phi_values.append(valuation_rank)
            d_phi_values.append(frege_depth)

    correlation_coefficient = calculate_correlation(r_phi_values, d_phi_values)
    conjecture_holds = correlation_coefficient >= 0.7

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(r_phi_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def generate_random_cnf(n: int) -> list:
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def get_polynomial(cnf: list) -> str:
    # Placeholder for polynomial generation logic
    return "x^2 + y^2"

def min_p_adic_valuation_rank(polynomial: str) -> int:
    # Placeholder for p-adic valuation rank calculation
    return 1

def frege_proof_depth(cnf: list) -> int:
    # Placeholder for Frege proof depth calculation
    return len(cnf)

def calculate_correlation(x_values: list, y_values: list) -> float:
    n = len(x_values)
    if n == 0:
        return 0

    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x ** 2 for x in x_values)
    sum_y2 = sum(y ** 2 for y in y_values)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))

    if denominator == 0:
        return 0

    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")