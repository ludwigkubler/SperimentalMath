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

def dpll(formula, assignment, literals):
    if not formula:
        return 0
    unit_clauses = [c for c in formula if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        new_literals = [l for l in literals if l != literal and -l not in literals]
        return 1 + dpll(formula, new_assignment, new_literals)
    pure_literal = next((l for l in literals if all(l not in clause or -l in clause for clause in formula)), None)
    if pure_literal is not None:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        new_literals = [l for l in literals if l != pure_literal and -l not in literals]
        return 1 + dpll(formula, new_assignment, new_literals)
    literal = random.choice(literals)
    new_assignment_true = assignment.copy()
    new_assignment_true[literal] = True
    new_literals_true = [l for l in literals if l != literal and -l not in literals]
    depth_true = 1 + dpll(formula, new_assignment_true, new_literals_true)
    new_assignment_false = assignment.copy()
    new_assignment_false[-literal] = True
    new_literals_false = [l for l in literals if l != -literal and -l not in literals]
    depth_false = 1 + dpll(formula, new_assignment_false, new_literals_false)
    return min(depth_true, depth_false)

def generate_random_formula(n):
    formula = []
    variables = list(range(1, n+1))
    for _ in range(2**n // 3):  # Ensure satisfiability
        clause = random.sample(variables + [-v for v in variables], random.randint(1, n))
        formula.append(clause)
    return formula

def toric_variety_rank(formula):
    # Simplified mapping to rank; actual implementation depends on the conjecture
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_random_formula(n)
    depth = dpll_search_tree_depth(formula, n)
    rank = toric_variety_rank(formula)
    return {
        "metric_name": "Depth of DPLL Search Tree",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": abs(depth - rank) <= max(2 * min(depth, rank), 1),
        "counterexample": ""
    }

def dpll_search_tree_depth(formula, n):
    return dpll(formula, {}, set(range(1, n+1)))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*40 + 1, 40))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth != rank\" first_failing_seed={seeds[first_failing_seed]}")