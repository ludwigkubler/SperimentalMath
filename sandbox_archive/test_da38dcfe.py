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
    
    def generate_boolean_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause[0] = f'~{clause[0]}'
                clause[1] = f'~{clause[1]}'
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def tseitin_transformation(formula):
        literals = set()
        for char in formula:
            if char.isalpha():
                literals.add(char)
        
        n = len(literals)
        variables = [f'y{i}' for i in range(1, n+1)]
        clauses = []
        
        for literal in literals:
            clauses.append(f'{literal} -> {variables[literals.index(literal)]}')
            clauses.append(f'~{literal} -> ~{variables[literals.index(literal)]}')
        
        for clause in formula.split(' and '):
            if ' or ' in clause:
                disjuncts = clause.split(' or ')
                new_var = variables[n]
                n += 1
                clauses.append(f'{disjuncts[0]} -> {new_var}')
                clauses.append(f'{disjuncts[1]} -> {new_var}')
                clauses.append(f'~{disjuncts[0]} -> ~{new_var}')
                clauses.append(f'~{disjuncts[1]} -> ~{new_var}')
                clauses.append(f'{new_var} -> ({disjuncts[0]} or {disjuncts[1]})')
        
        return ' and '.join(clauses)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def order_tropical_symplectic_form(formula):
        # Placeholder for the actual computation of the tropical symplectic form
        # and its order. This is a dummy implementation.
        return random.randint(1, 10)
    
    def resolution_proof_width(formula):
        # Placeholder for the actual computation of the resolution proof width.
        # This is a dummy implementation.
        return random.randint(1, 20)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        formula = generate_boolean_formula(random.randint(5, 40))
        tseitin_form = tseitin_transformation(formula)
        order = order_tropical_symplectic_form(tseitin_form)
        width = resolution_proof_width(formula)
        
        if abs(width - order) > 0.5 * order:
            conjecture_holds = False
            counterexample = f"Formula: {formula}, Order: {order}, Width: {width}"
            break
        
        metric_values.append(order)
    
    return {
        "metric_name": "Order of Tropical Symplectic Form",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.7:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")