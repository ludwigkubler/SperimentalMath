# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_formula(n):
    if n == 1:
        return random.choice(['0', '1'])
    else:
        left = generate_formula(n // 2)
        right = generate_formula(n - n // 2)
        op = random.choice(['&', '|'])
        return f"({left}{op}{right})"

def evaluate_formula(formula):
    if formula in ['0', '1']:
        return int(formula)
    elif formula[0] == '(' and formula[-1] == ')':
        left, op, right = formula[1:-1].split()
        left_val = evaluate_formula(left)
        right_val = evaluate_formula(right)
        if op == '&':
            return left_val & right_val
        elif op == '|':
            return left_val | right_val
    raise ValueError("Invalid formula")

def ramanujan_q(formula):
    if formula in ['0', '1']:
        return Fraction(1, 2) ** len(formula)
    elif formula[0] == '(' and formula[-1] == ')':
        left, op, right = formula[1:-1].split()
        left_val = evaluate_formula(left)
        right_val = evaluate_formula(right)
        if op == '&':
            return ramanujan_q(left) * ramanujan_q(right)
        elif op == '|':
            return 1 - (1 - ramanujan_q(left)) * (1 - ramanujan_q(right))
    raise ValueError("Invalid formula")

def resolution_width(formula):
    if formula in ['0', '1']:
        return 0
    elif formula[0] == '(' and formula[-1] == ')':
        left, op, right = formula[1:-1].split()
        left_val = evaluate_formula(left)
        right_val = evaluate_formula(right)
        if op == '&':
            return max(resolution_width(left), resolution_width(right))
        elif op == '|':
            return 1 + max(resolution_width(left), resolution_width(right))
    raise ValueError("Invalid formula")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    Q_min_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            Q_min = ramanujan_q(formula)
            w = resolution_width(formula)
            Q_min_sum += Q_min
            w_sum += w
            instances_tested += 1
            n_max = max(n_max, n)

    mean_Q_min = Fraction(Q_min_sum, instances_tested)
    mean_w = Fraction(w_sum, instances_tested)
    correlation_coefficient = (instances_tested * Q_min_sum * w_sum - Q_min_sum * Q_min_sum - w_sum * w_sum) / (
        math.sqrt((instances_tested * Q_min_sum * Q_min_sum - Q_min_sum * Q_min_sum) * (instances_tested * w_sum * w_sum - w_sum * w_sum))
    )
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * instances_tested - 3)))

    conjecture_holds = correlation_coefficient >= Fraction(7, 10) and p_value < Fraction(5, 100)
    counterexample = "" if conjecture_holds else "correlation_coefficient={:.4f}, p_value={:.4f}".format(correlation_coefficient, p_value)

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={}".format(len(results)))