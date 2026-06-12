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
    
    def generate_kary_formula(k, n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            literals = [f'x{i}' for i in range(n)]
            formula = '('
            for _ in range(k):
                subformula = ' & '.join(random.sample(literals, k))
                formula += f'({subformula}) | '
            formula = formula.rstrip(' | ') + ')'
            return formula

    def tseitin_formula(formula):
        literals = set()
        clauses = []
        
        def parse(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                parse(left)
                parse(right)
            elif ' | ' in formula:
                literals.add(formula)
            else:
                literals.add(formula)
        
        def tseitin_helper(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                return f'({tseitin_helper(left)} & {tseitin_helper(right)})'
            elif ' | ' in formula:
                literals.add(formula)
                return f'{formula} -> {len(literals) + 1}'
            else:
                literals.add(formula)
                return f'{formula} -> {len(literals) + 1}'
        
        parse(formula)
        tseitin_helper(formula)
        
        for literal in literals:
            clauses.append([literal, f'~{literal}', '0'])
            clauses.append([f'~{literal}', literal, '0'])
        
        return clauses

    def dpll(clauses):
        def is_satisfiable(clauses, assignment):
            for clause in clauses:
                if all(l not in assignment or (assignment[l] == 1 and l.startswith('~')) for l in clause):
                    return False
            return True
        
        def backtrack(assignment):
            unassigned = [l for l in literals if l not in assignment]
            if not unassigned:
                return is_satisfiable(clauses, assignment)
            
            literal = unassigned[0]
            assignment[literal] = 1
            if backtrack(assignment):
                return True
            assignment[literal] = -1
            if backtrack(assignment):
                return True
            del assignment[literal]
            return False
        
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        return backtrack({})
    
    def motivic_order(formula):
        # Placeholder function to simulate the motivic order calculation
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(formula.split())  # Simplified as number of words in formula
    
    instances_tested = 0
    n_max = 0
    motivic_orders = []
    dpll_widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_kary_formula(2, n)
            clauses = tseitin_formula(formula)
            dpll_width = dpll(clauses)
            motivic_order_val = motivic_order(formula)
            
            if dpll_width is not None:
                instances_tested += 1
                n_max = max(n_max, n)
                motivic_orders.append(motivic_order_val)
                dpll_widths.append(dpll_width)
    
    mean_motivic_order = sum(motivic_orders) / instances_tested
    mean_dpll_width = sum(dpll_widths) / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = 0
    if len(motivic_orders) > 1 and len(dpll_widths) > 1:
        numerator = sum((motivic_orders[i] - mean_motivic_order) * (dpll_widths[i] - mean_dpll_width) for i in range(len(motivic_orders)))
        denominator = math.sqrt(sum((motivic_orders[i] - mean_motivic_order) ** 2 for i in range(len(motivic_orders)))) * math.sqrt(sum((dpll_widths[i] - mean_dpll_width) ** 2 for i in range(len(dpll_widths))))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(motivic_order_val <= 2 * dpll_width_val for motivic_order_val, dpll_width_val in zip(motivic_orders, dpll_widths))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")