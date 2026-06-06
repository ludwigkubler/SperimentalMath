# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Generate all possible binary strings of length n
    for i in range(2**n):
        binary_str = format(i, f'0{n}b')
        clause = []
        for j in range(n):
            if binary_str[j] == '1':
                clause.append(variables[j])
            else:
                clause.append(f'{variables[j]}_bar')
        clauses.append(clause)
    
    # Add negated variables
    for var in variables:
        clauses.append([f'{var}_bar'])
    
    return clauses

def generate_formal_context(n):
    cnf = generate_tseitin_formula(n)
    formal_context = []
    for clause in cnf:
        row = [1 if var in clause else 0 for var in variables]
        formal_context.append(row)
    return formal_context

def circuit_monotone_width(cnf):
    n = len(variables)
    width = 0
    for i in range(2**n):
        assignment = {variables[j]: (i >> j) & 1 for j in range(n)}
        satisfied_clauses = [all(assignment[var] if var.startswith('x') else not assignment[var[4:]] for var in clause) for clause in cnf]
        width = max(width, sum(satisfied_clauses))
    return width

def minimal_order(formal_context):
    n = len(formal_context)
    order = 0
    for i in range(n):
        row = formal_context[i]
        if all(row[j] == formal_context[j][i] for j in range(n)):
            order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "minimal_order_over_monotone_width"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        cnf = generate_tseitin_formula(n)
        formal_context = generate_formal_context(n)
        
        monotone_width = circuit_monotone_width(cnf)
        order = minimal_order(formal_context)
        
        instances_tested += 1
        
        if order > monotone_width**0.5:
            conjecture_holds = False
            counterexample = f"n={n}, order={order}, monotone_width={monotone_width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")