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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        # Generate a random Boolean formula with n variables and 2n clauses
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables + [f'~{v}' for v in variables], k=3)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    def dpll_solver(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            var = literal.strip('~')
            value = literal.startswith('~') ^ (var in assignment and assignment[var])
            if not dpll_solver([c for c in cnf if literal not in c], {**assignment, var: value}):
                return False
        pure_literals = [l for l in set(''.join(cnf)) if l != '~' and f'~{l}' not in ''.join(cnf)]
        if pure_literals:
            literal = pure_literals[0]
            var = literal.strip('~')
            value = literal.startswith('~') ^ (var in assignment and assignment[var])
            if not dpll_solver([c for c in cnf if literal not in c], {**assignment, var: value}):
                return False
        literals = [l for l in set(''.join(cnf)) if l != '~' and f'~{l}' not in ''.join(cnf)]
        literal = random.choice(literals)
        var = literal.strip('~')
        value = literal.startswith('~') ^ (var in assignment and assignment[var])
        return dpll_solver([c for c in cnf if literal not in c], {**assignment, var: value}) or \
               dpll_solver([c for c in cnf if f'~{literal}' not in c], {**assignment, var: not value})

    def resolution_proof_width(cnf):
        # Simple heuristic to estimate the width of a resolution proof
        return max(len(set(l.split(' or '))) for l in cnf)

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    cnf = [c.strip().split(' or ') for c in formula.split(' and ')]
    
    if not dpll_solver(cnf):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Formula is unsatisfiable"
        }

    width = resolution_proof_width(cnf)
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.8 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"] and r["metric_value"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")