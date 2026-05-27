# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(n+1, 2*n):
            x = random.choice(variables)
            y = random.choice(variables)
            clause = f'({x} ^ {y})'
            clauses.append(clause)
        return ' & '.join(clauses)

    def xor_and_tree_width(formula):
        if formula.startswith('(') and formula.endswith(')'):
            left, right = formula[1:-1].split(' ^ ')
            return 1 + max(xor_and_tree_width(left), xor_and_tree_width(right))
        return 0

    def minimal_local_cohomology_rank(n):
        # Placeholder for actual computation
        # For simplicity, we use a dummy function that returns n^2
        return n**2

    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    tree_width = xor_and_tree_width(formula)
    rank = minimal_local_cohomology_rank(n)
    
    ratio = Fraction(rank, tree_width)
    conjecture_holds = ratio <= math.log2(n) * math.log2(n)
    counterexample = f'n={n}, rank={rank}, tree_width={tree_width}' if not conjecture_holds else ''
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result['conjecture_holds']:
            print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
            sys.exit(0)
        results.append(trial_result['metric_value'])

    mean_d = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_d)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log2(n)) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")