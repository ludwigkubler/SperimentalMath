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

def generate_random_formula(n):
    if n == 1:
        return random.choice(['True', 'False'])
    else:
        op = random.choice(['and', 'or'])
        left = generate_random_formula(n // 2)
        right = generate_random_formula(n - n // 2 - 1)
        return f"({left} {op} {right})"

def evaluate_formula(formula):
    if formula == "True":
        return True
    elif formula == "False":
        return False
    else:
        op, left, right = formula[1:-1].split()
        if op == 'and':
            return evaluate_formula(left) and evaluate_formula(right)
        elif op == 'or':
            return evaluate_formula(left) or evaluate_formula(right)

def resolution_width(formula):
    stack = []
    for token in formula.split():
        if token in ['True', 'False']:
            stack.append(token)
        else:
            right = stack.pop()
            left = stack.pop()
            if (left == "True" and right == "False") or (left == "False" and right == "True"):
                continue
            elif left == right:
                return 1 + max(resolution_width(left), resolution_width(right))
            else:
                new_clause = f"({token} {left}) ({token} {right})"
                stack.append(new_clause)
    return len(stack)

def topological_quantum_entanglement(n):
    # Placeholder for actual TQE calculation
    return random.random() * n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_random_formula(n)
            tqe = topological_quantum_entanglement(n)
            width = resolution_width(formula)
            results.append((tqe, width))
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    tqe_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    mean_tqe = sum(tqe_values) / len(tqe_values)
    mean_width = sum(width_values) / len(width_values)
    correlation_coefficient = sum((tqe - mean_tqe) * (width - mean_width) for tqe, width in results) / (len(results) * (sum((tqe - mean_tqe) ** 2 for tqe in tqe_values)) ** 0.5 * (sum((width - mean_width) ** 2 for width in width_values)) ** 0.5)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.5 and abs(mean_tqe - mean_width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_metric_value = (sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")