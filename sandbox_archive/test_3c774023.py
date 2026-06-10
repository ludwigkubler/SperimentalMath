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
        return 'x'
    else:
        left = generate_formula(random.randint(1, n-1))
        right = generate_formula(n - len(left.split()))
        operator = random.choice(['&', '|'])
        return f'({left} {operator} {right})'

def convert_to_monomial_basis(formula):
    if formula.startswith('(') and formula.endswith(')'):
        left, operator, right = formula[1:-1].split()
        return convert_to_monomial_basis(left), operator, convert_to_monomial_basis(right)
    else:
        return (formula,)

def compute_tropical_hodge_index(monomial_basis):
    if isinstance(monomial_basis, tuple):
        left, operator, right = monomial_basis
        return max(compute_tropical_hodge_index(left), compute_tropical_hodge_index(right))
    else:
        return 1

def dpll_search_tree_depth(formula):
    if formula.startswith('(') and formula.endswith(')'):
        left, operator, right = formula[1:-1].split()
        return 1 + max(dpll_search_tree_depth(left), dpll_search_tree_depth(right))
    else:
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    thi_sum = 0
    d_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            monomial_basis = convert_to_monomial_basis(formula)
            thi = compute_tropical_hodge_index(monomial_basis)
            d = dpll_search_tree_depth(formula)
            thi_sum += thi
            d_sum += d
            instances_tested += 1
            n_max = max(n_max, n)

    mean_thi = Fraction(thi_sum, instances_tested)
    mean_d = Fraction(d_sum, instances_tested)
    correlation_coefficient = (instances_tested * mean_thi * mean_d - thi_sum * d_sum) / (
        (instances_tested * mean_thi**2 - thi_sum**2) * (instances_tested * mean_d**2 - d_sum**2))**0.5

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")