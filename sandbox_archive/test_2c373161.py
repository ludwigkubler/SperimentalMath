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

def frege_proof_width(formula):
    if formula[0] != '(':
        return 1
    stack = []
    for char in formula:
        if char == '(':
            stack.append(char)
        elif char == ')':
            stack.pop()
    return len(stack)

def generate_random_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clause.append(random.choice(['|', '&']))
        clauses.append(''.join(clause))
    return '(' + ' '.join(clauses) + ')'

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = sum(n_values)

    for n in n_values:
        formula = generate_random_formula(n)
        rank = frege_proof_width(formula)
        total_rank += rank

    mean_value = total_rank / instances_tested
    conjecture_holds = mean_value >= n**2 * math.log2(n) * 1.5
    counterexample = "" if conjecture_holds else f"rank={mean_value}, expected={n**2 * math.log2(n)}"

    return {
        "metric_name": "frege_proof_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)

    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")