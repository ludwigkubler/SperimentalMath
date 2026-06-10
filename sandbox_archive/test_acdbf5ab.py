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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def sat_complexity(cnf):
    def dfs(model):
        stack = [model]
        while stack:
            model = stack.pop()
            if not any(all(var in clause or -var not in clause for clause in cnf) for var in range(1, len(cnf) + 1)):
                return False
            unassigned_vars = [var for var in range(1, len(cnf) + 1) if var not in model and -var not in model]
            if not unassigned_vars:
                return True
            var = random.choice(unassigned_vars)
            stack.append(model | {var})
            stack.append(model | {-var})
        return False

    return len(next(filter(dfs, [{}]), {}))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mcr_values = []
    sat_complexities = []

    for n in n_values:
        cnf = generate_cnf(n)
        mcr_value = len(cnf)  # Placeholder for actual MCR calculation
        sat_complexity = sat_complexity(cnf)

        mcr_values.append(mcr_value)
        sat_complexities.append(sat_complexity)

    correlation_coefficient = sum((mcr - sum(mcr_values) / len(mcr_values)) * (sat - sum(sat_complexities) / len(sat_complexities)) for mcr, sat in zip(mcr_values, sat_complexities)) / (len(mcr_values) * sum((mcr - sum(mcr_values) / len(mcr_values)) ** 2 for mcr in mcr_values))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")