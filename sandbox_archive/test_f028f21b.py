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
        literals = [f'x{i}' for i in range(n)]
        formula = []
        for _ in range(10):  # Generate a simple formula with 10 clauses
            clause = random.sample(literals, random.randint(2, n))
            formula.append(' or '.join(clause))
        return ' and '.join(formula)
    
    def evaluate_formula(formula):
        variables = {f'x{i}': False for i in range(n)}
        stack = []
        i = 0
        while i < len(formula):
            if formula[i] == '(':
                stack.append(i)
            elif formula[i] == ')':
                start = stack.pop()
                clause = formula[start+1:i].split(' or ')
                variables[f'x{i//2}'] = any(evaluate_clause(clause, variables))
            i += 1
        return all(variables.values())
    
    def evaluate_clause(clause, variables):
        for literal in clause:
            if literal.startswith('not '):
                yield not variables[literal[4:]]
            else:
                yield variables[literal]
    
    def quasi_continuous_order(formula):
        n = len(formula)
        order = 0
        while True:
            changed = False
            for i in range(n):
                if formula[i] == ' or ':
                    formula[i] = ' and '
                    changed = True
                elif formula[i] == ' and ':
                    formula[i] = ' or '
                    changed = True
            if not changed:
                break
            order += 1
        return order
    
    def resolution_width(formula):
        n = len(formula)
        width = 0
        for i in range(n):
            if formula[i] == ' or ':
                width = max(width, sum(1 for literal in formula[i].split(' or ') if literal.startswith('not ')))
            elif formula[i] == ' and ':
                width = max(width, sum(1 for literal in formula[i].split(' and ') if not literal.startswith('not ')))
        return width
    
    n_max = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_order = 0
        total_width = 0
        
        for _ in range(30):
            formula = generate_formula(n)
            order = quasi_continuous_order(formula)
            width = resolution_width(formula)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            total_order += order
            total_width += width
        
        metric_values.append({
            "n": n,
            "order": total_order / instances_tested,
            "width": total_width / instances_tested
        })
    
    mean_order = sum(metric["order"] for metric in metric_values) / len(metric_values)
    mean_width = sum(metric["width"] for metric in metric_values) / len(metric_values)
    
    if all(0.9 * mean_width <= order <= 1.1 * mean_width for order in [metric["order"] for metric in metric_values]):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Order does not correlate with width"
    
    return {
        "metric_name": "Quasi-Continuous Order vs Resolution Width",
        "metric_value": mean_order,
        "instances_tested": instances_tested * len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(0.9 * mean_width <= order <= 1.1 * mean_width for order, width in zip([result["metric_value"] for result in results], [result["width"] for result in results])):
        print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order does not correlate with width\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")