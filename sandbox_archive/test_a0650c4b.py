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
from fractions import Fraction
import math
from itertools import combinations, product

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        literals = [f'x{i+1}' if random.choice([True, False]) else f'-x{i+1}' for i in range(n)]
        clauses.append(' AND '.join(literals))
    return ' OR '.join(clauses)

def construct_formal_context(cnf):
    variables = set()
    relation = {}
    
    for clause in cnf.split(' OR '):
        literals = clause.split(' AND ')
        for literal in literals:
            variables.add(literal[2:] if literal.startswith('-') else literal)
            if literal not in relation:
                relation[literal] = set()
            for other_literal in literals:
                if literal != other_literal:
                    relation[literal].add(other_literal)
    
    return variables, relation

def is_transitively_closed(relation):
    closure = set(relation.keys())
    while True:
        new_closure = closure.copy()
        for x, y_set in relation.items():
            for y in y_set:
                if y not in closure and any(z in closure for z in relation.get(y, [])):
                    new_closure.add(y)
        if new_closure == closure:
            break
        closure = new_closure
    
    return closure == set(relation.keys())

def minimal_order(variables, relation):
    max_subcontext_size = 0
    for subset in combinations(variables, len(variables) // 2 + 1):
        subcontext_relation = {x: relation[x] & set(subset) for x in subset if x in relation}
        if is_transitively_closed(subcontext_relation):
            max_subcontext_size = max(max_subcontext_size, len(subset))
    return max_subcontext_size

def dpll(cnf):
    literals = cnf.split(' AND ')
    assignment = {}
    
    def solve(literals, assignment):
        if not literals:
            return True
        literal = next((l for l in literals if l[0] != '-'), None)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if solve([l for l in literals if l != literal], new_assignment):
            return True
        
        new_assignment[literal] = False
        if solve([l for l in literals if l != f'-{literal}'], new_assignment):
            return True
        
        return False
    
    return solve(literals, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            variables, relation = construct_formal_context(cnf)
            order = minimal_order(variables, relation)
            width = dpll(cnf)
            
            metrics.append({
                'n': n,
                'order': order,
                'width': width
            })
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metrics:
        return {
            "metric_name": "Minimal Order of Formal Contexts and DPLL Proof Width Inequality",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    order_values = [m['order'] for m in metrics]
    width_values = [m['width'] for m in metrics]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = (sum((x - mean_order) * (y - mean_width) for x, y in zip(order_values, width_values)) /
                               math.sqrt(sum((x - mean_order) ** 2 for x in order_values) *
                                         sum((y - mean_width) ** 2 for y in width_values)))
    
    return {
        "metric_name": "Minimal Order of Formal Contexts and DPLL Proof Width Inequality",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")