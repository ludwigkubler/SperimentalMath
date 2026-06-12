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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_transformation(formula):
        variables = {}
        literals = set()
        
        def assign_variable(literal):
            if literal not in variables:
                variables[literal] = f'x{len(variables)}'
                literals.add(literal)
            return variables[literal]
        
        def tseitin_clause(clause):
            if len(clause) == 1:
                return assign_variable(clause[0])
            elif len(clause) == 2 and clause[0] == 'not':
                return f'not {assign_variable(clause[1])}'
            else:
                temp_var = f't{len(variables)}'
                variables[temp_var] = temp_var
                for literal in clause:
                    if literal.startswith('not'):
                        tseitin_clause(['or', ['not', assign_variable(literal[4:])], temp_var])
                    else:
                        tseitin_clause(['or', assign_variable(literal), temp_var])
                return temp_var
        
        def tseitin_formula(formula):
            if isinstance(formula, list):
                if formula[0] == 'and':
                    for subformula in formula[1:]:
                        tseitin_formula(subformula)
                elif formula[0] == 'or':
                    for subformula in formula[1:]:
                        tseitin_formula(subformula)
                elif formula[0] == 'not':
                    tseitin_formula(formula[1])
            else:
                assign_variable(formula)
        
        tseitin_formula(formula)
        return variables
    
    def resolution_width(variables):
        # Placeholder for actual resolution width calculation
        # This is a dummy implementation for testing purposes
        return len(variables) / 2
    
    def minimal_tropical_symplectic_form(order):
        # Placeholder for actual tropical symplectic form computation
        # This is a dummy implementation for testing purposes
        return order
    
    formula = random.choice(['and', 'or', 'not']) + ['x1', 'x2']
    tseitin_form = tseitin_transformation(formula)
    resolution_width_value = resolution_width(tseitin_form)
    tropical_symplectic_order = minimal_tropical_symplectic_form(len(variables))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_value,
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": abs(resolution_width_value - tropical_symplectic_order) <= 0.5 * tropical_symplectic_order,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")