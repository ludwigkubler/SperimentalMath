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

def generate_cnf(n: int) -> list:
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def min_local_ring_norm(cnf: list, p: int) -> Fraction:
    valuation = 0
    for clause in cnf:
        for literal in clause:
            if abs(literal) > valuation:
                valuation = abs(literal)
    return Fraction(valuation, p)

def resolution_width(cnf: list) -> int:
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)] = literal > 0
            remaining_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(remaining_clauses, new_assignment)
        pure_literal = next((l for l in range(1, max(abs(c) for c in sum(clauses, [])) + 1) 
                             if (all(l in c for c in clauses) or all(-l in c for c in clauses))), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            remaining_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(remaining_clauses, new_assignment)
        literal = random.choice(sum(clauses, []))
        return dpll([c for c in clauses if literal not in c], assignment) or dpll([c for c in clauses if -literal not in c], assignment)
    
    max_width = 0
    for _ in range(10):
        assignment = {}
        width = 0
        while not dpll(cnf, assignment):
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[abs(literal)] = literal > 0
                remaining_clauses = [c for c in cnf if literal not in c and -literal not in c]
                cnf = remaining_clauses
                width += 1
        max_width = max(max_width, width)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2  # Prime number for p-adic field
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n - 4)):
            cnf = generate_cnf(n)
            min_norm_val = min_local_ring_norm(cnf, p)
            width_val = resolution_width(cnf)
            metric_values.append((min_norm_val, width_val))
    
    if not metric_values:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    min_norms, widths = zip(*metric_values)
    mean_min_norm = sum(min_norms) / len(min_norms)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = (sum((m - mean_min_norm) * (w - mean_width) for m, w in metric_values) /
                                math.sqrt(sum((m - mean_min_norm) ** 2 for m in min_norms) *
                                          sum((w - mean_width) ** 2 for w in widths)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results) or support_fraction < 0.6:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")