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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'x'
        else:
            p = random.choice(['&', '|'])
            a, b = generate_boolean_formula(n-1), generate_boolean_formula(1)
            return f'({a} {p} {b})'

    def dpll(formula):
        if formula.startswith('True'):
            return True
        elif formula.startswith('False'):
            return False
        elif formula[0] == 'x':
            return random.choice([True, False])
        else:
            literal = formula.split()[1]
            rest = ' '.join(formula.split()[2:])
            if literal.startswith('~'):
                if dpll(rest):
                    return False
                else:
                    return True
            else:
                if dpll(f'~{rest}'):
                    return False
                else:
                    return True

    def resolution_width(formula):
        stack = [formula]
        while stack:
            current = stack.pop()
            if current.startswith('True') or current.startswith('False'):
                continue
            literal = current.split()[1]
            rest = ' '.join(current.split()[2:])
            if literal.startswith('~'):
                if literal[1:] in stack:
                    return 1 + resolution_width(rest)
                else:
                    stack.append(f'~{rest}')
            else:
                if f'~{literal}' in stack:
                    return 1 + resolution_width(rest)
                else:
                    stack.append(f'~{rest}')
        return 0

    def symplectic_embedding_size(n):
        # Simplified model for demonstration purposes
        return n * (n + 1) // 2

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_boolean_formula(n)
    mls_phi = symplectic_embedding_size(n)
    w_phi = resolution_width(formula)

    return {
        "metric_name": "mls(φ) vs. w(φ)",
        "metric_value": abs(mls_phi - w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mls_phi >= 0.8 * w_phi and abs(mls_phi - w_phi) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")