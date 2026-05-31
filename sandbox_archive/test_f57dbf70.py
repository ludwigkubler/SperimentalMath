# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        clause = [var]
        neg_clause = [-var]
        clauses.append(clause)
        clauses.append(neg_clause)
    
    # Generate clauses for implications
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clause = [-i, -j, i + j]
            neg_clause = [i, j, -(i + j)]
            clauses.append(clause)
            clauses.append(neg_clause)
    
    # Generate the final clause
    final_clause = []
    for var in variables:
        final_clause.append(-var)
    clauses.append(final_clause)
    
    return clauses

def evaluate_formula(formula, assignment):
    stack = []
    for literal in formula:
        if isinstance(literal, list):
            sub_result = True
            for lit in literal:
                if lit > 0 and not assignment[lit - 1]:
                    sub_result = False
                    break
                elif lit < 0 and assignment[-lit - 1]:
                    sub_result = False
                    break
            stack.append(sub_result)
        else:
            if literal > 0 and not assignment[literal - 1]:
                stack.append(False)
            elif literal < 0 and assignment[-literal - 1]:
                stack.append(True)
    
    result = True
    for res in stack:
        result &= res
    
    return result

def p_adic_valuation(n):
    if n == 0:
        return 0
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def resolution_width(formula):
    clauses = formula[:]
    learned_clauses = []
    
    def resolve(clause1, clause2):
        new_clause = [lit for lit in clause1 if lit not in clause2 and -lit not in clause2]
        return new_clause
    
    while True:
        found_resolvent = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                common_lits = [lit for lit in clauses[i] if -lit in clauses[j]]
                if common_lits:
                    resolvent = resolve(clauses[i], clauses[j])
                    learned_clauses.append(resolvent)
                    found_resolvent = True
                    break
            if found_resolvent:
                break
        
        if not found_resolvent:
            break
        
        clauses.extend(learned_clauses)
        learned_clauses.clear()
    
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        variables = list(range(1, n + 1))
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            assignment = {var: random.choice([True, False]) for var in variables}
            if evaluate_formula(formula, assignment):
                mvw = p_adic_valuation(sum(1 for lit in formula if evaluate_formula([lit], assignment)))
                resolution_w = resolution_width(formula)
                results.append((mvw, resolution_w))
    
    if len(results) < 30:
        return {
            "metric_name": "MVW vs Resolution Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mvw_values = [mvw for mvw, _ in results]
    resolution_w_values = [w for _, w in results]
    
    mean_mvw = sum(mvw_values) / len(mvw_values)
    mean_resolution_w = sum(resolution_w_values) / len(resolution_w_values)
    
    if abs(mean_mvw - mean_resolution_w) < 0.1:
        return {
            "metric_name": "MVW vs Resolution Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_correlation"
        }
    
    correlation_coefficient = sum((mvw - mean_mvw) * (w - mean_resolution_w) for mvw, w in results) / len(results)
    
    return {
        "metric_name": "MVW vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _, w in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value'] if result['metric_value'] is not None else 'None'}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None]))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['metric_value'] < 0.5 for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'] and r['metric_value'] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")