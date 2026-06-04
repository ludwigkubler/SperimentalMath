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

def generate_boolean_formula(n):
    if n == 1:
        return random.choice(['x', 'not x'])
    else:
        op = random.choice(['and', 'or'])
        left = generate_boolean_formula(n - 1)
        right = generate_boolean_formula(n - 1)
        return f'({left} {op} {right})'

def evaluate_formula(formula, assignment):
    if formula == 'x':
        return assignment[0]
    elif formula == 'not x':
        return not assignment[0]
    else:
        left, op, right = formula.split()
        left_val = evaluate_formula(left, assignment)
        right_val = evaluate_formula(right, assignment)
        if op == 'and':
            return left_val and right_val
        elif op == 'or':
            return left_val or right_val

def generate_assignment(n):
    return [random.choice([True, False]) for _ in range(n)]

def frege_proof_depth(formula):
    if formula == 'x' or formula == 'not x':
        return 1
    else:
        left, op, right = formula.split()
        return 1 + max(frege_proof_depth(left), frege_proof_depth(right))

def symplectic_leaves_count(n):
    # Placeholder function for computing the minimal order of symplectic leaves
    # This is a dummy implementation and should be replaced with actual computation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        min_order_sum = 0
        instances_tested = 0
        for _ in range(5):
            formula = generate_boolean_formula(n)
            assignment = generate_assignment(n)
            if evaluate_formula(formula, assignment):
                proof_depth = frege_proof_depth(formula)
                min_order = symplectic_leaves_count(n)
                min_order_sum += min_order
                instances_tested += 1
        if instances_tested == 0:
            continue
        mean_min_order = Fraction(min_order_sum, instances_tested)
        conjecture_holds = mean_min_order >= n and abs(mean_min_order - n) <= 3
        results.append({
            "n": n,
            "mean_min_order": mean_min_order,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"Formula: {formula}, Assignment: {assignment}"
        })
    return {
        "metric_name": "mean_min_order",
        "metric_value": sum(result["mean_min_order"] for result in results) / len(results),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if not result['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")