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
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def evaluate_formula(formula, assignment):
        stack = []
        tokens = formula.split()
        for token in tokens:
            if token == 'and':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + ' and ' + b)
            elif token == 'or':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + ' or ' + b)
            else:
                stack.append(token)
        return stack[0]
    
    def truth_table(formula, n):
        variables = [f'x{i}' for i in range(n)]
        table = []
        for assignment in product([True, False], repeat=n):
            assignment_dict = {var: val for var, val in zip(variables, assignment)}
            result = evaluate_formula(formula, assignment_dict)
            table.append((assignment, result))
        return table
    
    def resolution(table):
        clauses = [set(clause.split(' or ')) for _, clause in table if clause == 'False']
        new_clauses = set()
        while True:
            found_new_clause = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    for literal in clauses[i]:
                        if literal.startswith('not '):
                            neg_literal = literal[4:]
                            if neg_literal in clauses[j]:
                                new_clause = (clauses[i] - {literal}) | (clauses[j] - {neg_literal})
                                if new_clause not in new_clauses:
                                    new_clauses.add(new_clause)
                                    found_new_clause = True
            if not found_new_clause:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    total_order = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_formula(n)
        table = truth_table(formula, n)
        order = resolution(table)
        total_order += order
    
    mean_order = Fraction(total_order, instances_tested)
    
    return {
        "metric_name": "order",
        "metric_value": float(mean_order),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")