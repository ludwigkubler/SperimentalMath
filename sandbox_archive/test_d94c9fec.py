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

def generate_formula(n):
    if n == 1:
        return random.choice(['P', '¬P'])
    else:
        var = f'X{n}'
        op = random.choice(['∧', '∨'])
        subformula1 = generate_formula(n - 1)
        subformula2 = generate_formula(n - 1)
        return f'{var} {op} ({subformula1}) ({subformula2})'

def dpll(formula):
    if formula == 'P':
        return True
    elif formula == '¬P':
        return False
    else:
        var, op, subformula = formula.split()
        if var[0] == 'X':
            n = int(var[1:])
            if op == '∧':
                return dpll(subformula) and dpll(formula.replace(f'({subformula})', '', 1))
            elif op == '∨':
                return dpll(subformula) or dpll(formula.replace(f'({subformula})', '', 1))
        else:
            raise ValueError("Invalid formula format")

def p_adic_order(n, p):
    if n == 0:
        return 0
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        path_length = dpll(formula)
        p_adic_val = p_adic_order(path_length, 2)  # Using base 2 for simplicity
        results.append((p_adic_val, path_length))
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    p_adic_vals = [r[0] for r in results]
    path_lengths = [r[1] for r in results]
    mean_p_adic = sum(p_adic_vals) / len(p_adic_vals)
    mean_path_length = sum(path_lengths) / len(path_lengths)
    correlation = (sum((p_adic - mean_p_adic) * (path - mean_path_length) for p_adic, path in results) /
                   math.sqrt(sum((p_adic - mean_p_adic)**2 for p_adic in p_adic_vals) *
                             sum((path - mean_path_length)**2 for path in path_lengths)))
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    if all(r is not None and abs(r) >= 0.7 for r in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((r - mean)**2 for r in results) / len(results))
        support_fraction = len([r for r in results if abs(r) >= 0.7]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is None or abs(result) < 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")