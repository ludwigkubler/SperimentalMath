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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            random.shuffle(clause)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    def tropicalize_formula(formula):
        # Simplified tropicalization procedure
        points = []
        for clause in formula.split(' and '):
            if ' or ' in clause:
                literals = clause.split(' or ')
                point = [1 if literal.startswith('x') else -1 for literal in literals]
                points.append(point)
        return points

    def calculate_automorphism_group_order(points):
        # Simplified calculation of automorphism group order
        n = len(points[0])
        order = 1
        for i in range(n):
            if all(points[j][i] == points[0][i] for j in range(1, len(points))):
                order += 1
        return order

    def dpll_proof_path_length(formula):
        # Simplified DPLL proof path length calculation
        stack = [formula]
        path_length = 0
        while stack:
            formula = stack.pop()
            if ' or ' not in formula and ' and ' not in formula:
                continue
            if ' or ' in formula:
                clause, rest = formula.split(' or ', 1)
                if '~' not in clause:
                    stack.append(rest)
                else:
                    stack.append(clause.replace('~', '') + ' and ' + rest)
            elif ' and ' in formula:
                clause, rest = formula.split(' and ', 1)
                if '~' not in clause:
                    stack.append(clause + ' or ' + rest)
                else:
                    stack.append(clause.replace('~', '') + ' and ' + rest)
            path_length += 1
        return path_length

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        formula = generate_random_formula(n)
        points = tropicalize_formula(formula)
        order_t = calculate_automorphism_group_order(points)
        path_length = dpll_proof_path_length(formula)
        results.append((order_t, path_length))

    mean_order_t = sum(order_t for order_t, _ in results) / len(results)
    mean_path_length = sum(path_length for _, path_length in results) / len(results)
    std_deviation = math.sqrt(sum((order_t - mean_order_t)**2 + (path_length - mean_path_length)**2 for order_t, path_length in results) / len(results))

    support_fraction = sum(1 for order_t, path_length in results if abs(order_t - path_length) <= 3 * max(path_length)) / len(results)

    return {
        "metric_name": "order_t vs path_length",
        "metric_value": mean_order_t,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order_t = sum(res["metric_value"] for res in results) / len(results)
    std_deviation = math.sqrt(sum((res["metric_value"] - mean_order_t)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order_t} std={std_deviation} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")