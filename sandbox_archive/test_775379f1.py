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
    for _ in range(10 * n):  # Generate 10 clauses per variable on average
        clause = [random.randint(-n, n) for _ in range(random.randint(2, 5))]
        if all(clause[i] != -clause[j] for j in range(i)):
            cnf.append(clause)
    return cnf

def dpll(cnf):
    def search(model):
        unit_clauses = [c for c in cnf if len(c) == 1]
        if not unit_clauses:
            unsatisfied_clauses = [c for c in cnf if any(lit in model for lit in c)]
            return not unsatisfied_clauses
        literal, _ = unit_clauses[0]
        if literal > 0:
            new_model = model | {literal}
        else:
            new_model = model - {-literal}
        return search(new_model) or search(model - {abs(literal)})
    return search(set())

def geometric_entropy(cnf):
    n = len(cnf)
    entropy = 0
    for clause in cnf:
        if len(clause) == 1:
            continue
        prob = 1 / (2 ** len(clause))
        entropy += -prob * math.log2(prob)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    dpll_lengths = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Test each size with 5 different CNF formulas
            cnf = generate_cnf(n)
            if not cnf:
                continue
            mge = geometric_entropy(cnf)
            length = dpll(cnf)
            mge_values.append(mge)
            dpll_lengths.append(length)
            instances_tested += 1
            n_max = max(n_max, n)

    if not mge_values or not dpll_lengths:
        return {
            "metric_name": "mge vs DPLL length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }

    mge_mean = sum(mge_values) / len(mge_values)
    dpll_length_mean = sum(dpll_lengths) / len(dpll_lengths)

    # Simple linear regression to check correlation
    slope = (len(mge_values) * sum(m * l for m, l in zip(mge_values, dpll_lengths)) - 
             sum(mge_values) * sum(dpll_lengths)) / \
            (len(mge_values) * sum(m ** 2 for m in mge_values) - sum(mge_values) ** 2)
    intercept = sum(mge_values) / len(mge_values) - slope * sum(dpll_lengths) / len(dpll_lengths)

    correlation_coefficient = slope

    return {
        "metric_name": "mge vs DPLL length",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")

    mge_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(mge_values) / len(mge_values)} std=0 support_fraction=1")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(mge_values) / len(mge_values)} std=0 support_fraction={conjecture_holds_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")