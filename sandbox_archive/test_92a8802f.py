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

def generate_instance(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def construct_mapping(instance):
    # Placeholder for the actual mapping logic
    return "mapping_undefined"

def measure_resolution_width(instance):
    def dpll():
        if not instance:
            return 0
        var = find_pure_literal(instance)
        if var is None:
            return 1 + min(dpll(), dpll())
        polarity = random.choice([True, False])
        new_instance = [clause for clause in instance if not (var == abs(clause[0]))]
        return 1 + dpll()
    def find_pure_literal(clauses):
        pure_literals = set()
        for literal in set(lit for clause in clauses for lit in clause):
            if all(lit != -x and -lit != x for clause in clauses for x in clause):
                pure_literals.add(literal)
        return random.choice(pure_literals) if pure_literals else None
    return dpll()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = generate_instance(n)
    mapping = construct_mapping(instance)
    if mapping == "mapping_undefined":
        return {
            "metric_name": "OrderCrossedProduct",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    width = measure_resolution_width(instance)
    return {
        "metric_name": "OrderCrossedProduct",
        "metric_value": width,  # Placeholder for actual computation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(v is not None for v in metric_values):
        correlation = calculate_correlation(metric_values, [r["instances_tested"] for r in results])
        if correlation >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and r['metric_value'] is not None))]}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_unsupported")

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
    return cov_xy / (std_x * std_y)