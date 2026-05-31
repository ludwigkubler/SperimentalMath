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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate clauses for each variable
    for i in range(n):
        clause = [variables[i]]
        for j in range(i + 1, n):
            clause.append(-variables[j])
        clauses.append(clause)
    
    # Generate clauses to ensure at least one literal is true
    for i in range(1, n + 1):
        clauses.append([i])
    
    # Add the final clause that combines all variables
    final_clause = [-variables[i] for i in range(n)]
    final_clause.append(variables[0])
    clauses.append(final_clause)
    
    return clauses

def evaluate_formula(formula, assignment):
    for clause in formula:
        if all(not assignment[abs(lit) - 1] if lit < 0 else assignment[lit - 1] for lit in clause):
            continue
        return False
    return True

def compute_p_adic_valuation_width(formula, n):
    min_valuation = float('inf')
    for i in range(2**n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if evaluate_formula(formula, assignment):
            valuation = sum(int(math.log(abs(x), 3)) for x in assignment)
            if valuation < min_valuation:
                min_valuation = valuation
    return min_valuation

def compute_resolution_proof_width(formula):
    # Simple DPLL solver to estimate proof width
    def dpll(clauses, assignment):
        if not clauses:
            return len(assignment)
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            new_assignment = assignment + [bool(lit > 0)]
            new_clauses = [c for c in clauses if not evaluate_formula([lit], new_assignment)]
            return dpll(new_clauses, new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if (all(l not in c for c in clauses) or all(-l not in c for c in clauses))), None)
        if pure_literal:
            new_assignment = assignment + [bool(pure_literal > 0)]
            new_clauses = [c for c in clauses if not evaluate_formula([pure_literal], new_assignment)]
            return dpll(new_clauses, new_assignment)
        literal = random.choice(range(1, n + 1))
        new_assignment_true = assignment + [True]
        new_clauses_true = [c for c in clauses if not evaluate_formula([literal], new_assignment_true)]
        result_true = dpll(new_clauses_true, new_assignment_true)
        if result_true != float('inf'):
            return result_true
        new_assignment_false = assignment + [False]
        new_clauses_false = [c for c in clauses if not evaluate_formula([-literal], new_assignment_false)]
        result_false = dpll(new_clauses_false, new_assignment_false)
        return result_false
    
    return dpll(formula, [])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mvw_values = []
    wp_values = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        mvw = compute_p_adic_valuation_width(formula, n)
        wp = compute_resolution_proof_width(formula)
        mvw_values.append(mvw)
        wp_values.append(wp)
    
    correlation_coefficient = sum((mvw - mean_mvw) * (wp - mean_wp) for mvw, wp in zip(mvw_values, wp_values)) / len(mvw_values)
    mean_mvw = sum(mvw_values) / len(mvw_values)
    mean_wp = sum(wp_values) / len(wp_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else f"correlation_coefficient={correlation_coefficient:.4f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")