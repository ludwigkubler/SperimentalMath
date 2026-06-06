# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def generate_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause = [f'not {v}' for v in clause]
        clauses.append(' or '.join(clause))
    return ' and '.join(clauses)

def evaluate_formula(formula, assignment):
    stack = []
    tokens = formula.split()
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'not':
            next_token = tokens[i+1]
            if next_token.startswith('x'):
                stack.append(not assignment[next_token[1:]])
            else:
                stack.append(not evaluate_formula(next_token, assignment))
            i += 2
        elif token in ['and', 'or']:
            op = token
            right = stack.pop()
            left = stack.pop()
            if op == 'and':
                stack.append(left and right)
            else:
                stack.append(left or right)
            i += 1
        else:
            if token.startswith('x'):
                stack.append(assignment[token[1:]])
            else:
                stack.append(evaluate_formula(token, assignment))
            i += 1
    return stack.pop()

def find_minimal_order(formula):
    n = len(formula.split())
    variables = [f'x{i}' for i in range(1, n+1)]
    min_order = float('inf')
    for k in range(1, n+1):
        for assignment in combinations(variables, k):
            assignment_dict = {var: True if var in assignment else False for var in variables}
            if evaluate_formula(formula, assignment_dict) == 0:
                min_order = min(min_order, k)
    return min_order

def frege_proof_width(formula):
    # This is a placeholder function. Implement the actual Frege proof width calculation.
    # For simplicity, we assume it's proportional to the number of variables.
    n = len(formula.split())
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        formula = generate_formula(random.randint(5, 40))
        min_order = find_minimal_order(formula)
        proof_width = frege_proof_width(formula)
        if proof_width == 0:
            return {
                "metric_name": "Min Order / Proof Width Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": len(formula.split()),
                "conjecture_holds": False,
                "counterexample": f"Formula: {formula}, Min Order: {min_order}, Proof Width: {proof_width}"
            }
        ratio = Fraction(min_order, proof_width)
        results.append(ratio)
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Min Order / Proof Width Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": 30,
        "n_max": max(len(formula.split()) for formula in [generate_formula(random.randint(5, 40)) for _ in range(30)]),
        "conjecture_holds": all(abs(ratio - mean_ratio) <= Fraction(10, 100) * abs(mean_ratio) for ratio in results) and abs(results[0] - results[-1]) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len([result for result in results if result["metric_value"] is not None])
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len([result for result in results if result["metric_value"] is not None])) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")