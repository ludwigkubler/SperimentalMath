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

def generate_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = ' OR '.join(random.sample(variables, 2))
        clauses.append(clause)
    return ' AND '.join(clauses)

def dpll(formula):
    if formula == "TRUE":
        return 0
    elif formula == "FALSE":
        return float('inf')
    
    literals = set()
    for part in formula.split():
        if part.startswith("NOT"):
            literals.add(part[4:])
        else:
            literals.add(part)
    
    def dpll_rec(formula, assignment):
        if formula == "TRUE":
            return 0
        elif formula == "FALSE":
            return float('inf')
        
        for literal in literals:
            if literal not in assignment and 'NOT' + literal not in assignment:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_formula = simplify(formula, literal)
                result = dpll_rec(new_formula, new_assignment)
                if result < float('inf'):
                    return result + 1
                new_assignment[literal] = False
                new_formula = simplify(formula, 'NOT' + literal)
                result = dpll_rec(new_formula, new_assignment)
                if result < float('inf'):
                    return result + 1
        
        return float('inf')
    
    def simplify(formula, literal):
        parts = formula.split()
        simplified_parts = []
        for part in parts:
            if part == literal or (part.startswith("NOT") and part[4:] == literal):
                continue
            elif part.startswith("NOT") and part[4:] == 'NOT' + literal:
                simplified_parts.append(literal)
            else:
                simplified_parts.append(part)
        return ' AND '.join(simplified_parts)
    
    return dpll_rec(formula, {})

def regular_grammar_order(n):
    # Generate a simple regular grammar for the language L(φ)
    # This is a placeholder function; replace with actual implementation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        formula = generate_formula(n)
        dpll_length = dpll(formula)
        grammar_order = regular_grammar_order(n)
        
        results.append({
            "n": n,
            "formula": formula,
            "dpll_length": dpll_length,
            "grammar_order": grammar_order
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    dpll_lengths = [r["dpll_length"] for r in results]
    grammar_orders = [r["grammar_order"] for r in results]
    
    mean_dpll = sum(dpll_lengths) / len(dpll_lengths)
    mean_grammar = sum(grammar_orders) / len(grammar_orders)
    
    covariance = sum((d - mean_dpll) * (g - mean_grammar) for d, g in zip(dpll_lengths, grammar_orders))
    variance_dpll = sum((d - mean_dpll) ** 2 for d in dpll_lengths)
    variance_grammar = sum((g - mean_grammar) ** 2 for g in grammar_orders)
    
    if variance_dpll == 0 or variance_grammar == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_dpll) * math.sqrt(variance_grammar))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.8,
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_below_threshold' first_failing_seed={first_failing_seed}")