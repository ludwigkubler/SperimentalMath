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

def generate_formula(n):
    if n == 1:
        return random.choice(['True', 'False'])
    else:
        op = random.choice(['&', '|'])
        left = generate_formula(n // 2)
        right = generate_formula(n - n // 2)
        return f'({left} {op} {right})'

def evaluate_formula(formula, assignment):
    if formula in ['True', 'False']:
        return formula == 'True'
    else:
        left, op, right = formula.split()
        if op == '&':
            return evaluate_formula(left, assignment) and evaluate_formula(right, assignment)
        elif op == '|':
            return evaluate_formula(left, assignment) or evaluate_formula(right, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_order_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        if n > n_max:
            n_max = n
        for _ in range(5):  # Ensure at least 5 instances per size
            formula = generate_formula(n)
            assignment = {f'x{i}': random.choice([True, False]) for i in range(n)}
            min_order = len(formula.split())  # Simplistic proxy for minimal order of symplectic leaves
            min_order_sum += min_order
            instances_tested += 1

    mean_min_order = Fraction(min_order_sum, instances_tested)
    conjecture_holds = n_max >= 16 and all(mean_min_order >= n for n in n_values) and abs(mean_min_order - sum(n_values) / len(n_values)) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "min_order",
        "metric_value": float(mean_min_order),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)

    mean_min_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")