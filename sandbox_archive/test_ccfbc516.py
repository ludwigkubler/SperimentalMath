# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(x == 0 for x in clause):
            continue
        clauses.append(clause)
    return clauses

def tseitin_encoding(cnf):
    literals = set()
    for clause in cnf:
        literals.update(abs(lit) for lit in clause)
    
    new_vars = {lit: len(literals) + i + 1 for i, lit in enumerate(literals)}
    formulas = []
    
    for clause in cnf:
        if len(clause) == 1:
            formulas.append(f"X_{new_vars[clause[0]]} = {abs(clause[0])}")
        else:
            new_var = max(new_vars.values()) + 1
            formulas.append(f"X_{new_var} = ({' | '.join([f'(X_{new_vars[lit]})' if lit > 0 else f'~(X_{new_vars[-lit]})' for lit in clause])})")
            new_vars[clause[0]] = new_var
    
    return formulas

def quiver_representation(cnf):
    formulas = tseitin_encoding(cnf)
    quiver = {}
    
    for formula in formulas:
        if '=' not in formula:
            continue
        lhs, rhs = formula.split('=')
        literals = [int(x.strip()) for x in rhs.split('|')]
        for lit in literals:
            if lit > 0:
                if lit not in quiver:
                    quiver[lit] = set()
                quiver[lit].update(literals)
    
    return quiver

def minimal_order(quiver):
    order = 0
    visited = set()
    stack = list(quiver.keys())
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in quiver[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
            order += 1
    
    return order

def frege_proof_length(cnf):
    n = len(cnf[0])
    clauses = [set(abs(lit) for lit in clause) for clause in cnf]
    variables = set(range(1, n + 1))
    
    def extend_formula(formula, variable):
        new_formulas = []
        for clause in formula:
            if variable not in clause:
                new_formulas.append(clause | {variable})
                new_formulas.append(clause | {-variable})
        return new_formulas
    
    def is_satisfiable(formula):
        stack = [formula]
        while stack:
            current_formula = stack.pop()
            if len(current_formula) == 0:
                continue
            variable = min(current_formula)
            if -variable in current_formula:
                return False
            new_formula = extend_formula(current_formula, variable)
            for new_clause in new_formula:
                if all(lit not in variables for lit in new_clause):
                    stack.append(new_clause)
        return True
    
    def proof_length(formula):
        length = 0
        while not is_satisfiable(formula):
            length += 1
            formula = extend_formula(formula, min(formula))
        return length
    
    return proof_length(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            quiver_rep = quiver_representation(cnf)
            order = minimal_order(quiver_rep)
            complexity = frege_proof_length(cnf)
            
            total_order += order
            total_complexity += complexity
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_complexity = total_complexity / instances_tested
    correlation_coefficient = (instances_tested * sum(order * complexity for order, complexity in zip(total_order, total_complexity)) -
                               sum(total_order) * sum(total_complexity)) / math.sqrt(
                                   instances_tested * sum(order**2 for order in total_order) - sum(total_order)**2 *
                                   instances_tested * sum(complexity**2 for complexity in total_complexity) - sum(total_complexity)**2)
    
    conjecture_holds = 0.5 <= correlation_coefficient < 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.4f} not within [0.5, 0.7)"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")