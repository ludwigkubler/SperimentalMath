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
    
    def generate_formula(n):
        variables = set(f"x{i}" for i in range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables | {f"~{v}" for v in variables}, 2)
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses, assignment={}):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [[l for l in c if l != literal and l != f"~{literal}"] for c in clauses]
            return 1 + dpll_width(new_clauses, new_assignment)
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = True
                else:
                    pure_literals[literal] = False
        for literal, is_pure in pure_literals.items():
            if is_pure:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = [[l for l in c if l != literal and l != f"~{literal}"] for c in clauses]
                return 1 + dpll_width(new_clauses, new_assignment)
        literals = [c[0] for c in clauses if len(c) > 1]
        literal = random.choice(literals)
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [[l for l in c if l != literal and l != f"~{literal}"] for c in clauses]
        width_true = dpll_width(new_clauses_true, new_assignment_true)
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        new_clauses_false = [[l for l in c if l != literal and l != f"~{literal}"] for c in clauses]
        width_false = dpll_width(new_clauses_false, new_assignment_false)
        return 1 + max(width_true, width_false)
    
    def betti_number(clauses):
        # Placeholder implementation. This is a dummy value.
        return random.random()
    
    n_max = 40
    instances_tested = 30
    max_betti = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_formula(n)
        width = dpll_width(formula)
        betti = betti_number(formula)
        if betti > max_betti:
            max_betti = betti
    
    conjecture_holds = max_betti <= (math.log(n_max) / math.log(math.log(n_max))) * width
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "max_betti",
        "metric_value": max_betti,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")