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

def generate_cnf(n):
    cnf = []
    for _ in range(2**n - 1):  # Generate a CNF with n variables and 2^n - 1 clauses
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(lit not in clause and -lit not in clause for lit in cnf):
            cnf.append(clause)
    return cnf

def calculate_minimal_order(cnf):
    n = len(cnf[0])
    power_series = [0] * (n + 1)
    power_series[0] = 1
    for clause in cnf:
        coeff = random.choice([-1, 1])
        for lit in clause:
            if lit > 0:
                power_series[lit - 1] += coeff
            else:
                power_series[-lit - 1] -= coeff
    minimal_order = sum(abs(coeff) for coeff in power_series)
    return minimal_order

def calculate_resolution_width(cnf):
    width = 0
    for clause in cnf:
        width = max(width, len(clause))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_order = 0
    total_width = 0
    max_n = 0

    for n in n_values:
        cnf = generate_cnf(n)
        if len(cnf) < 10:  # Ensure there are at least 10 clauses
            continue
        order = calculate_minimal_order(cnf)
        width = calculate_resolution_width(cnf)
        total_instances += len(cnf)
        total_order += order
        total_width += width
        max_n = n

    mean_order = total_order / total_instances
    mean_width = total_width / total_instances
    correlation_coefficient = (total_order * total_width - total_instances * mean_order * mean_width) / \
                              math.sqrt((total_order**2 - total_instances * mean_order**2) *
                                        (total_width**2 - total_instances * mean_width**2))

    conjecture_holds = abs(correlation_coefficient) >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient too low' first_failing_seed={first_failing_seed}")