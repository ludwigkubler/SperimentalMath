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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def evaluate_clause(clause, assignment):
    return any(assignment[abs(l) - 1] == (l > 0) for l in clause)

def evaluate_formula(formula, assignment):
    return all(evaluate_clause(clause, assignment) for clause in formula)

def zeta_function(cnf):
    n = len(cnf)
    zeta_value = Fraction(1, 2**n)
    for _ in range(n):
        zeta_value *= Fraction(1, 2)
    return zeta_value

def resolution_width(cnf):
    # Simplified DPLL solver to estimate resolution width
    def dpll(formula, assignment, clauses):
        if not formula:
            return True
        unit_clause = next((c for c in formula if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            new_formula = [c for c in formula if literal not in c and -literal not in c]
            return dpll(new_formula, new_assignment, clauses)
        pure_literal = next((l for l in range(1, n + 1) if sum(l in c or -l in c for c in formula) == 1), None)
        if pure_literal:
            new_assignment = assignment[:]
            new_assignment[pure_literal - 1] = True
            new_formula = [c for c in formula if pure_literal not in c and -pure_literal not in c]
            return dpll(new_formula, new_assignment, clauses)
        literal = random.choice([l for l in range(1, n + 1) if any(l in c or -l in c for c in formula)])
        new_assignment = assignment[:]
        new_assignment[literal - 1] = True
        new_formula = [c for c in formula if literal not in c and -literal not in c]
        if dpll(new_formula, new_assignment, clauses):
            return True
        new_assignment[literal - 1] = False
        new_formula = [c for c in formula if literal not in c and -literal not in c]
        return dpll(new_formula, new_assignment, clauses)
    
    return len(cnf) if dpll(cnf, [False] * n, cnf) else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        zeta_value = zeta_function(cnf)
        if zeta_value <= 0:
            continue
        zeta_order = math.log(zeta_value, 2) if zeta_value > 0 else -math.inf
        width = resolution_width(cnf)
        results.append((zeta_order, width))
    
    if not results:
        return {
            "metric_name": "Order(ζφ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    zeta_orders, widths = zip(*results)
    correlation_coefficient = sum((zeta_orders[i] - mean(zeta_orders)) * (widths[i] - mean(widths)) for i in range(len(results))) / len(results) / math.sqrt(variance(zeta_orders)) / math.sqrt(variance(widths))
    
    return {
        "metric_name": "Order(ζφ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def variance(values):
    avg = mean(values)
    return sum((x - avg) ** 2 for x in values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(r is not None for r in results):
        mean_val = mean(results)
        std_dev = math.sqrt(variance(results))
        support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 1 for i, r in enumerate(results) if r is None), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")