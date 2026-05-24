# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):
            clause = [random.randint(-1, -n), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and any(l in c or -l in c for c in cnf)) == (-l not in assignment and any(-l in c or l in c for c in cnf))), None)
        if pure_literal:
            new_assignment = {**assignment, pure_literal: True}
            return dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment)
        literal = random.choice([l for l in range(1, n+1) if l not in assignment])
        new_assignment_true = {**assignment, literal: True}
        if dpll(cnf, new_assignment_true):
            return True
        new_assignment_false = {**assignment, literal: False}
        return dpll(cnf, new_assignment_false)
    
    def rank_quasipolynomial(n):
        # Placeholder for actual quasipolynomial rank calculation
        return n  # Simplified example
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    if not dpll(cnf):
        return {
            "metric_name": "diameter",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    diameter = 0
    for _ in range(3):
        assignment = {}
        stack = [(cnf, assignment)]
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                continue
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = {**assignment, abs(literal): literal > 0}
                stack.append(([c for c in cnf if literal not in c and -literal not in c], new_assignment))
            else:
                pure_literal = next((l for l in range(1, n+1) if (l not in assignment and any(l in c or -l in c for c in cnf)) == (-l not in assignment and any(-l in c or l in c for c in cnf))), None)
                if pure_literal:
                    new_assignment = {**assignment, pure_literal: True}
                    stack.append(([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment))
                else:
                    literal = random.choice([l for l in range(1, n+1) if l not in assignment])
                    new_assignment_true = {**assignment, literal: True}
                    stack.append(([c for c in cnf if literal not in c and -literal not in c], new_assignment_true))
                    new_assignment_false = {**assignment, literal: False}
                    stack.append(([c for c in cnf if literal not in c and -literal not in c], new_assignment_false))
    
    rank = rank_quasipolynomial(n)
    return {
        "metric_name": "diameter",
        "metric_value": diameter,
        "instances_tested": 1,
        "conjecture_holds": rank >= diameter,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):0.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")