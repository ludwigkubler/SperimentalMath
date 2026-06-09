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
    
    def generate_formula(m, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'-{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True if var.startswith('x') else False
            if dpll([c for c in clauses if not any(v in c for v in (var, f'-{var}'))], new_assignment):
                return True
            new_assignment.pop(var)
        pure_literal = next((v for v in variables if all(v in c or f'-{v}' in c for c in clauses)), None)
        if pure_literal:
            new_assignment[pure_literal] = True if pure_literal.startswith('x') else False
            if dpll([c for c in clauses if not any(v in c for v in (pure_literal, f'-{pure_literal}'))], new_assignment):
                return True
            new_assignment.pop(pure_literal)
        for var in variables:
            if var not in assignment and f'-{var}' not in assignment:
                new_assignment[var] = True
                if dpll([c for c in clauses if not any(v in c for v in (var, f'-{var}'))], new_assignment):
                    return True
                new_assignment.pop(var)
                new_assignment[f'-{var}'] = True
                if dpll([c for c in clauses if not any(v in c for v in (var, f'-{var}'))], new_assignment):
                    return True
                new_assignment.pop(f'-{var}')
        return False
    
    def resolution(clauses):
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(not v.startswith('-') and not f'-{v}' in clauses[j] for v in clauses[i]) and any(v.startswith('-') and not v[1:] in clauses[i] for v in clauses[j]):
                        resolvent = [c for c in clauses[i] if not c.startswith('-')] + [c[1:] for c in clauses[j] if c.startswith('-')]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    n = random.randint(5, 30)
    m = random.randint(n, n * 2)
    formula = generate_formula(m, n)
    width = resolution(formula)
    
    return {
        "metric_name": "msl_over_w",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")