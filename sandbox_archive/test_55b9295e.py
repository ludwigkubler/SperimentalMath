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

def generate_3cnf(n, m):
    literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
    clauses = []
    while len(clauses) < m:
        clause = set()
        while len(clause) < 3:
            literal = random.choice(literals)
            if literal not in clause and -literal not in clause:
                clause.add(literal)
        clauses.append(tuple(sorted(clause)))
    return clauses

def dpll_solver(clauses):
    def solve(variables, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment or literal > 0 and literal not in assignment:
                return False
            assignment.add(literal)
            clauses.remove(unit_clause)
            return solve(variables, assignment)
        pure_literal = next((l for l in variables if all(l != c[0] and -l != c[1] for c in clauses)), None)
        if pure_literal is not None:
            if pure_literal < 0 and -pure_literal in assignment or pure_literal > 0 and pure_literal not in assignment:
                return False
            assignment.add(pure_literal)
            clauses = [c for c in clauses if literal not in c]
            return solve(variables, assignment)
        variable = next(iter(variables))
        if solve(variables - {variable}, assignment | {variable}):
            return True
        if solve(variables - {variable}, assignment | {-variable}):
            return True
        return False

    variables = set(l for clause in clauses for l in clause)
    assignment = set()
    return solve(variables, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Number of variables
    m = math.ceil(1.5 * n)  # Number of clauses
    clauses = generate_3cnf(n, m)
    
    if not dpll_solver(clauses):
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    t_star = len(dpll_solver(clauses))
    rank_R_F = n
    
    return {
        "metric_name": "resolution_length",
        "metric_value": t_star,
        "instances_tested": 1,
        "conjecture_holds": t_star <= m**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    total_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    mean_metric_value = total_metric_value / sum(1 for result in results if result["metric_value"] is not None)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
    
    counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, result in enumerate(results) if not result['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")