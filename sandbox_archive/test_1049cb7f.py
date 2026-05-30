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
from fractions import Fraction
import math
import sys

def generate_random_sat_instance(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + ['!' + v for v in variables], 2)
        if random.choice([True, False]):
            clause[0] = '!' + clause[0]
        if random.choice([True, False]):
            clause[1] = '!' + clause[1]
        clauses.append(clause)
    return variables, clauses

def dpll_search_tree(clauses, assignment):
    if not clauses:
        return 1
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        pure_literal = unit_clause[0]
        new_assignment = assignment.copy()
        if pure_literal.startswith('!'):
            new_assignment[pure_literal[1:]] = False
        else:
            new_assignment[pure_literal] = True
        return dpll_search_tree([c for c in clauses if pure_literal not in c], new_assignment)
    pure_literal = next((l for l in assignment if all(l not in c or (not c[0] == '!' and not c[0] == '~') for c in clauses)), None)
    if pure_literal is None:
        return 0
    new_assignment_true = assignment.copy()
    new_assignment_true[pure_literal] = True
    new_assignment_false = assignment.copy()
    new_assignment_false[pure_literal] = False
    return dpll_search_tree([c for c in clauses if pure_literal not in c], new_assignment_true) + \
           dpll_search_tree([c for c in clauses if pure_literal not in c], new_assignment_false)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 5 * n)
    variables, clauses = generate_random_sat_instance(n, m)
    result = dpll_search_tree(clauses, {})
    return {
        "metric_name": "num_trees",
        "metric_value": result,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if result == 0 else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")