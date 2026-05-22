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

def is_quadratic_residue(a, n):
    return pow(a, (n - 1) // 2, n) == 1

def count_quadratic_residues(n):
    count = 0
    for a in range(1, n):
        if is_quadratic_residue(a, n):
            count += 1
    return count

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append(f'{variables[i]}')
        clauses.append(f'-{variables[i]}')
    for i in range(1, n):
        clauses.append(f'{variables[i-1]} {variables[i]}')
        clauses.append(f'-{variables[i-1]} -{variables[i]}')
    return ' '.join(clauses)

def resolution_length(formula):
    clauses = formula.split()
    literals = set()
    while True:
        new_literals = set()
        for clause in clauses:
            if not clause:
                continue
            literal, *rest = clause.split()
            if literal.startswith('-'):
                literal = literal[1:]
                if literal in literals:
                    literals.remove(literal)
                else:
                    new_literals.add(literal)
            else:
                if literal in literals:
                    return len(clauses) + 1
                else:
                    literals.add(literal)
        if not new_literals:
            break
        clauses.extend([f'-{l}' for l in new_literals])
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            formula = generate_tseitin_formula(n)
            length = resolution_length(formula)
            total_length += length
            instances_tested += 1

    average_length = Fraction(total_length, instances_tested)

    expected_length = n_values[-1]**2 * math.log(n_values[-1], count_quadratic_residues(n_values[-1])) / math.log(math.log(n_values[-1], count_quadratic_residues(n_values[-1])))
    
    conjecture_holds = abs(average_length - expected_length) <= 0.1 * expected_length
    counterexample = "" if conjecture_holds else f"n={n_values[-1]}, avg_length={average_length}, expected_length={expected_length}"

    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": float(average_length),
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

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_values[-1], avg_length, expected_length\" first_failing_seed={first_failing_seed}")