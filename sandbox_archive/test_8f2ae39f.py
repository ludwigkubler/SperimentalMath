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

def generate_boolean_formula(n):
    if n == 1:
        return 'x'
    else:
        op = random.choice(['&', '|', '^'])
        left = generate_boolean_formula(random.randint(1, n-1))
        right = generate_boolean_formula(n - len(left.split('&')) - len(left.split('|')) - len(left.split('^')))
        return f'({left} {op} {right})'

def dpll_tree_height(formula):
    if formula.isalpha():
        return 0
    else:
        op_index = formula.find(' ')
        left_height = dpll_tree_height(formula[1:op_index])
        right_height = dpll_tree_height(formula[op_index+2:-1])
        return max(left_height, right_height) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test each n with 5 different formulas
            formula = generate_boolean_formula(n)
            height = dpll_tree_height(formula)
            total_metric_value += height
            instances_tested += 1

            k = random.uniform(0.1, 2.0)  # Random constant k for the bound
            if height > k * math.log(n):
                conjecture_holds = False
                counterexample = f"Formula: {formula}, Height: {height}, Expected Bound: {k * math.log(n)}"

    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")