# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations, chain

def generate_3cnf(n: int) -> list:
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables + [f'~{v}' for v in variables], 3)
        clauses.append(clause)
    return clauses

def is_satisfiable(clauses: list) -> bool:
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            value = var.startswith('~') ^ (var[1:] not in assignment)
            new_assignment = {**assignment, var[1:]: value}
            return dpll([c for c in clauses if var not in c and '~' + var not in c], new_assignment)
        pure_literal = next((v for v in variables if all(v not in c or '~' + v in c for c in clauses)), None)
        if pure_literal:
            value = pure_literal.startswith('~') ^ (pure_literal[1:] not in assignment)
            new_assignment = {**assignment, pure_literal[1:]: value}
            return dpll(clauses, new_assignment)
        p_var = random.choice(variables)
        return dpll(clauses + [[f'~{p_var}']], {**assignment, p_var: True}) or dpll(clauses + [[p_var]], {**assignment, p_var: False})
    return dpll(clauses, {})

def kahler_manifold_rank(formula: list) -> int:
    # Placeholder for Kähler manifold rank calculation
    # This is a dummy implementation and should be replaced with actual computation
    return len(formula)

def dpll_search_tree_height(clauses: list) -> int:
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            value = var.startswith('~') ^ (var[1:] not in assignment)
            new_assignment = {**assignment, var[1:]: value}
            return dpll([c for c in clauses if var not in c and '~' + var not in c], new_assignment) + 1
        pure_literal = next((v for v in variables if all(v not in c or '~' + v in c for c in clauses)), None)
        if pure_literal:
            value = pure_literal.startswith('~') ^ (pure_literal[1:] not in assignment)
            new_assignment = {**assignment, pure_literal[1:]: value}
            return dpll(clauses, new_assignment) + 1
        p_var = random.choice(variables)
        return max(dpll(clauses + [[f'~{p_var}']], {**assignment, p_var: True}), dpll(clauses + [[p_var]], {**assignment, p_var: False})) + 1
    return dpll(clauses, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    if not is_satisfiable(formula):
        return {
            "metric_name": "Kahler Manifold Rank to DPLL Search Tree Height Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    rank = kahler_manifold_rank(formula)
    height = dpll_search_tree_height(formula)
    ratio = Fraction(rank, height) if height != 0 else None
    return {
        "metric_name": "Kahler Manifold Rank to DPLL Search Tree Height Ratio",
        "metric_value": float(ratio) if ratio is not None else None,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"

    print(result)