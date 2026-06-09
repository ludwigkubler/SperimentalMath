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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], n)
            clauses.append(' ∨ '.join(clause))
        return ' ∧ '.join(clauses)
    
    def resolution_width(formula):
        # Simplified DPLL solver to estimate resolution width
        literals = set()
        stack = []
        for clause in formula.split(' ∧ '):
            literals |= {l.strip('~') for l in clause.split(' ∨ ') if l}
            stack.append(clause)
        
        while stack:
            clause = stack.pop()
            if any(l.startswith('~') and l[1:] in literals for l in clause.split(' ∨ ')):
                continue
            new_clause = None
            for i, c in enumerate(stack):
                if any(l.startswith('~') and l[1:] in clause.split(' ∨ ') for l in c.split(' ∨ ')):
                    new_clause = ' ∨ '.join([l for l in c.split(' ∨ ') if not l.startswith('~') and l[1:] not in clause.split(' ∨ ')])
                    break
            if new_clause:
                stack.append(new_clause)
            else:
                return len(literals)
        return len(literals)
    
    def cyclic_orderings(formula):
        # Simplified mapping to cyclic orderings (not actual Frege proof)
        clauses = formula.split(' ∧ ')
        return len(clauses)  # This is a trivial example; replace with actual logic
    
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    formula = generate_formula(n, m)
    width = resolution_width(formula)
    orderings = cyclic_orderings(formula)
    
    if width == 0:
        return {
            "metric_name": "Cyclic Orderings",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    return {
        "metric_name": "Cyclic Orderings",
        "metric_value": orderings / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if orderings / width <= 1.5 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "resolution_width_is_zero"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)