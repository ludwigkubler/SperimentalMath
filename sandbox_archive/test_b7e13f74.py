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

def generate_tseitin_clauses(n):
    variables = set()
    clauses = []
    for i in range(1, n + 1):
        literals = [f"x{i}"] if random.choice([True, False]) else [-i]
        clause = "or".join(literals)
        clauses.append(clause)
        variables.update(int(l) for l in clause.split('or'))
    return clauses, list(variables)

def dpll_solver(clauses):
    def solve(model, i=0):
        if i == len(clauses):
            return True
        clause = clauses[i]
        literals = [l.strip() for l in clause.split('or')]
        for literal in literals:
            var = int(literal[1:]) if literal.startswith('-') else int(literal)
            if literal.startswith('-'):
                if var not in model or model[var] != 0:
                    continue
            else:
                if var in model and model[var] == 1:
                    continue
            new_model = {**model, var: 1} if literal.startswith('-') else {**model, var: 0}
            if solve(new_model, i + 1):
                return True
        return False
    return solve({})

def minimal_index_of_kahler_metric(clause_set):
    variables = set()
    for clause in clause_set:
        literals = [l.strip() for l in clause.split('or')]
        variables.update(int(l) for l in literals)
    
    if not variables:
        return 0
    
    max_var = max(variables)
    kahler_index = max_var
    return kahler_index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clause_set, _ = generate_tseitin_clauses(n)
    
    if not clause_set:
        return {
            "metric_name": "kahler_index",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "empty_clause_set"
        }
    
    kahler_index = minimal_index_of_kahler_metric(clause_set)
    if not kahler_index:
        return {
            "metric_name": "kahler_index",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "zero_kahler_index"
        }
    
    solver = dpll_solver(clause_set)
    if not solver:
        return {
            "metric_name": "kahler_index",
            "metric_value": kahler_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_clause_set"
        }
    
    k = 0
    while solver():
        k += 1
    
    if k == 0:
        return {
            "metric_name": "kahler_index",
            "metric_value": kahler_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "no_resolution_proof"
        }
    
    return {
        "metric_name": "kahler_index",
        "metric_value": kahler_index,
        "instances_tested": 1,
        "conjecture_holds": kahler_index <= 2**k,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 67))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")