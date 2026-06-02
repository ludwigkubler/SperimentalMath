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

def generate_cnf(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    cnf = []
    for _ in range(m):
        k = random.randint(1, n)
        clause = random.sample(variables, k)
        cnf.append(clause)
    return cnf

def min_order(cnf: list) -> int:
    from itertools import combinations
    def is_partition(partition):
        for subset in partition:
            if not any(all(abs(x) == abs(y) for x, y in zip(subset, subset[1:]))) and len(set(abs(x) for x in subset)) != len(subset):
                return False
        return True

    n = len(cnf)
    min_order = float('inf')
    for r in range(1, n + 1):
        for partition in combinations(range(n), r):
            if is_partition(partition):
                min_order = min(min_order, r)
    return min_order

def resolution_width(cnf: list) -> int:
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            return False
        literal = unit_clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = literal > 0
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[abs(literal)] = not literal > 0
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)

    assignment = {}
    return len(cnf) - sum(dpll(cnf, assignment) for _ in range(10))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(n, 2 * n))
            instances_tested += 1
            min_order_val = min_order(cnf)
            width_val = resolution_width(cnf)
            metric_values.append(min_order_val / width_val)

    if len(metric_values) < 30:
        return {
            "metric_name": "min_order_over_resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, [sum(metric_values) / len(metric_values)] * len(metric_values))) / (len(metric_values) * math.sqrt(sum((x - mean) ** 2 for x in metric_values)) * math.sqrt(sum((y - mean) ** 2 for y in [sum(metric_values) / len(metric_values)] * len(metric_values))))
    if abs(correlation_coefficient) < 0.7 or max(metric_values) > 1.5:
        conjecture_holds = False
        counterexample = "correlation_threshold_not_met"

    return {
        "metric_name": "min_order_over_resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported")