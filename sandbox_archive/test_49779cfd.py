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

def generate_sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n + 1)]
        clauses.append(' | '.join(clause))
    return ' & '.join(clauses)

def clause_indicator_polynomial(phi):
    literals = set()
    for clause in phi.split(' & '):
        for literal in clause.split(' | '):
            literals.add(literal)
    polynomial = {}
    for literal in literals:
        if literal.startswith('-'):
            variable = int(literal[1:])
            polynomial[-variable] = 0
        else:
            variable = int(literal[1:])
            polynomial[variable] = 0
    return polynomial

def min_order_twisted_quiver(phi):
    polynomial = clause_indicator_polynomial(phi)
    n_max = max(abs(k) for k in polynomial.keys())
    # Simplified procedure to estimate the minimal order of twisted quiver representation
    # This is a placeholder and should be replaced with actual computation based on representation theory
    return n_max

def resolution_proof_width(phi):
    # Placeholder function to estimate the resolution proof width
    # This is a placeholder and should be replaced with actual computation based on resolution algorithms
    return len(phi.split(' & '))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_sat_instance(n)
        min_order_twq = min_order_twisted_quiver(phi)
        width = resolution_proof_width(phi)
        results.append((min_order_twq, width))
    if len(results) < 30:
        return {
            "metric_name": "MinOrder vs Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    min_orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_width = sum(widths) / len(widths)
    std_dev_min_order = math.sqrt(sum((x - mean_min_order) ** 2 for x in min_orders) / len(min_orders))
    std_dev_width = math.sqrt(sum((x - mean_width) ** 2 for x in widths) / len(widths))
    correlation_coefficient = sum((min_orders[i] - mean_min_order) * (widths[i] - mean_width) for i in range(len(results))) / (len(results) * std_dev_min_order * std_dev_width)
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(results) - 2)))
    return {
        "metric_name": "MinOrder vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(3, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")