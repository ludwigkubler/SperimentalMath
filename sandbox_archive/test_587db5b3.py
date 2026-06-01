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
from itertools import combinations

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([f"x{i}", f"~x{i}"]) for i in range(1, n + 1)]
        random.shuffle(clause)
        clauses.append(" ".join(clause))
    return " ".join(clauses)

def p_adic_valuation(clause, p):
    valuation = float('inf')
    for literal in clause.split():
        if literal.startswith('~'):
            var = int(literal[2:])
        else:
            var = int(literal[1:])
        valuation = min(valuation, Fraction(1, 2 ** (var - 1)))
    return valuation

def compute_min_norm(cnf, p):
    clauses = cnf.split()
    min_norm = float('inf')
    for clause in clauses:
        val = p_adic_valuation(clause, p)
        if val < min_norm:
            min_norm = val
    return min_norm

def dpll_solve(cnf):
    def solve(variables, assignment):
        if not variables:
            return True
        var = variables[0]
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if all(new_assignment[var] == (value if literal.startswith('~') else not value) for literal in clause.split()):
                continue
            new_variables = [v for v in variables[1:] if v != var]
            if solve(new_variables, new_assignment):
                return True
        return False

    cnf_lines = cnf.split()
    literals = set(literal.strip('~') for line in cnf_lines for literal in line.split())
    variables = list(range(1, max(int(lit) for lit in literals) + 1))
    if solve(variables, {}):
        return len(cnf_lines)
    else:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            min_norm = compute_min_norm(cnf, p)
            width = dpll_solve(cnf)
            if min_norm == float('inf') or width == float('inf'):
                continue
            metric_values.append((min_norm, width))
    
    if not metric_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_min_norm = sum(m for m, _ in metric_values) / len(metric_values)
    mean_width = sum(w for _, w in metric_values) / len(metric_values)
    correlation_coefficient = (sum((m - mean_min_norm) * (w - mean_width) for m, w in metric_values) /
                               math.sqrt(sum((m - mean_min_norm) ** 2 for m, _ in metric_values) *
                                         sum((w - mean_width) ** 2 for _, w in metric_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(c >= 0.7 for c in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results) or support_fraction < 0.6:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")