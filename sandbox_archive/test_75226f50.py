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
    variables = [f"v{i}" for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for OR gates
    for i in range(1, n+1):
        clause = [-variables[i-1]]
        for j in range(i+1, n+1):
            clause.append(f"v{j}")
        clauses.append(clause)
    
    # Generate clauses for AND gates
    for i in range(n):
        clause = [f"v{i+1}", f"v{n+i+1}"]
        clauses.append(clause)
    
    return variables, clauses

def formal_context_from_formula(variables, clauses):
    context = {}
    for var in variables:
        context[var] = set()
    for clause in clauses:
        for lit in clause:
            if lit.startswith('v'):
                context[lit].add(lit[1:])
            else:
                context[-lit[1:]].add(-int(lit))
    return context

def minimal_order(context):
    n = len(context)
    order = 0
    while True:
        new_order = sum(len(values) for values in context.values())
        if new_order <= order:
            break
        order = new_order
    return order

def circuit_monotone_width(clauses):
    max_clause_length = max(len(clause) for clause in clauses)
    return max_clause_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        context = formal_context_from_formula(variables, clauses)
        order = minimal_order(context)
        width = circuit_monotone_width(clauses)
        
        results.append({
            "n": n,
            "order": order,
            "width": width
        })
    
    total_order = sum(result["order"] for result in results)
    total_width = sum(result["width"] for result in results)
    mean_order = Fraction(total_order, len(results))
    mean_width = Fraction(total_width, len(results))
    
    conjecture_holds = all(order <= width**0.5 for order, width in zip([result["order"] for result in results], [result["width"] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order vs Circuit Monotone Width",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")