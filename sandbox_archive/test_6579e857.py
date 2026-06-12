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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)

    def evaluate_formula(formula, assignment):
        stack = []
        literals = formula.split()
        for literal in literals:
            if literal.startswith('x'):
                stack.append(assignment[literal])
            elif literal == 'NOT':
                stack.append(not stack.pop())
            else:
                a = stack.pop()
                b = stack.pop()
                if literal == 'OR':
                    stack.append(a or b)
                elif literal == 'AND':
                    stack.append(a and b)
        return stack[0]

    def resolution(formula):
        clauses = formula.split(' AND ')
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clause.split(' OR ') for clause in clauses[i].split(' AND '))
                    clause_j = set(clause.split(' OR ') for clause in clauses[j].split(' AND '))
                    new_clause = []
                    for literal in clause_i:
                        if 'NOT' + literal not in clause_j and literal != 'NOT' + literal:
                            new_clause.append(literal)
                    for literal in clause_j:
                        if 'NOT' + literal not in clause_i and literal != 'NOT' + literal:
                            new_clause.append(literal)
                    if len(new_clause) == 0:
                        return True
                    new_clauses.append(' AND '.join(new_clause))
            if new_clauses == clauses:
                return False
            clauses = new_clauses

    def quasi_continuous_function(formula):
        n = formula.count('x')
        order = n * math.log(n, 2)
        return order

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_formula(n)
        assignment = {f'x{i}': random.choice([True, False]) for i in range(1, n+1)}
        satisfaction_relation = evaluate_formula(formula, assignment)
        resolution_width = resolution(formula)
        quasi_order = quasi_continuous_function(formula)
        results.append((quasi_order, resolution_width))

    mean_quasi_order = sum(result[0] for result in results) / len(results)
    std_quasi_order = math.sqrt(sum((result[0] - mean_quasi_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result[0] - result[1]) <= 0.1 * result[1]) / len(results)
    
    return {
        "metric_name": "quasi_continuous_order",
        "metric_value": mean_quasi_order,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": support_fraction >= 0.8 and mean_quasi_order <= (1 + 0.2) * max(result[1] for result in results),
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_quasi_order} std={std_quasi_order} support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_value} std={std_value} support_fraction={support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")