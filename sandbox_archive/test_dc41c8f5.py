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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
            clauses.append(f'-{variables[i]}')
        for i in range(1, n):
            clauses.append(f'{variables[i-1]} {variables[i]} -{variables[0]}')
        return ' '.join(clauses)
    
    def evaluate_formula(formula, assignment):
        stack = []
        literals = formula.split()
        for literal in literals:
            if literal.startswith('-'):
                stack.append(not eval(assignment[literal[1:]]))
            else:
                stack.append(eval(assignment[literal]))
            while len(stack) >= 3 and stack[-2] == 'and':
                b = stack.pop()
                a = stack.pop()
                op = stack.pop()
                stack.append(a and b)
            while len(stack) >= 3 and stack[-2] == 'or':
                b = stack.pop()
                a = stack.pop()
                op = stack.pop()
                stack.append(a or b)
        return stack[0]
    
    def p_adic_valuation(x):
        if x == 0:
            return float('inf')
        val = 0
        while x % 2 == 0:
            x //= 2
            val += 1
        return val
    
    def resolution_width(formula):
        clauses = formula.split()
        literals = set(clauses)
        queue = list(literals)
        seen = set(queue)
        while queue:
            literal = queue.pop(0)
            if literal.startswith('-'):
                negated_literal = literal[1:]
                if negated_literal in seen:
                    continue
                for clause in clauses:
                    if negated_literal in clause.split():
                        new_clause = ' '.join(lit for lit in clause.split() if lit != negated_literal and not lit.startswith('-'))
                        if new_clause:
                            queue.append(new_clause)
                            seen.add(new_clause)
            else:
                negated_literal = '-' + literal
                if negated_literal in seen:
                    continue
                for clause in clauses:
                    if literal in clause.split():
                        new_clause = ' '.join(lit for lit in clause.split() if lit != literal and not lit.startswith('-'))
                        if new_clause:
                            queue.append(new_clause)
                            seen.add(new_clause)
        return len(queue)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mvw_sum = 0
    w_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_tseitin_formula(n)
            assignments = {var: random.choice([True, False]) for var in variables}
            mvw = p_adic_valuation(evaluate_formula(formula, assignments))
            w = resolution_width(formula)
            if mvw < float('inf'):
                mvw_sum += mvw
                w_sum += w
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mvw = mvw_sum / instances_tested
    mean_w = w_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mvw * w for mvw, w in zip([mean_mvw] * instances_tested, [mean_w] * instances_tested)) - instances_tested * mean_mvw * mean_w) / ((instances_tested - 1) * math.sqrt(instances_tested * sum((mvw - mean_mvw) ** 2 for mvw in [mean_mvw] * instances_tested) - instances_tested * (mean_mvw ** 2)) * math.sqrt(instances_tested * sum((w - mean_w) ** 2 for w in [mean_w] * instances_tested) - instances_tested * (mean_w ** 2)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None]))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")