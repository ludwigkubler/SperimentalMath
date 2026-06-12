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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} | ~{var}')
        for i in range(1, n+1):
            clause = f'~x{i}'
            for j in range(i+1, n+1):
                clause += f' | x{j}'
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def evaluate_formula(formula, assignment):
        stack = []
        literals = formula.split()
        for lit in literals:
            if lit.startswith('~'):
                stack.append(not evaluate_formula(lit[1:], assignment))
            elif lit == '&':
                b = stack.pop()
                a = stack.pop()
                stack.append(a and b)
            else:
                stack.append(assignment[lit])
        return stack[0]
    
    def find_model(formula):
        n = len(formula.split(' & ')[0].split())
        assignment = {f'x{i}': False for i in range(1, n+1)}
        queue = [assignment.copy()]
        while queue:
            current_assignment = queue.pop()
            if evaluate_formula(formula, current_assignment):
                return current_assignment
            for var in current_assignment:
                new_assignment = current_assignment.copy()
                new_assignment[var] = not new_assignment[var]
                queue.append(new_assignment)
        return None
    
    def tropical_polynomial_root_system(formula):
        model = find_model(formula)
        if model is None:
            return 0
        root_index = sum(1 for var in model if model[var])
        return root_index
    
    def resolution_proof_width(formula):
        # Simplified version of resolution proof width calculation
        clauses = formula.split(' & ')
        n = len(clauses)
        max_clause_length = max(len(clause.split(' | ')) for clause in clauses)
        return n * max_clause_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_index_values = []
    w_values = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        root_index = tropical_polynomial_root_system(formula)
        proof_width = resolution_proof_width(formula)
        m_index_values.append(root_index)
        w_values.append(proof_width)
    
    if not m_index_values or not w_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(m_index_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def calculate_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else None
    
    correlation_coefficient = calculate_correlation(m_index_values, w_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(m_index_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.6 for corr in m_index_values),
        "counterexample": "" if correlation_coefficient is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.6\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")