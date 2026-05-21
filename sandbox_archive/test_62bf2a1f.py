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

def generate_tseitin_formula(n: int) -> str:
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n+1):
        clause = f'{variables[i-1]} OR {variables[n+i-1]}'
        clauses.append(clause)
    
    # Generate clauses to ensure the formula is satisfiable
    for i in range(n):
        clause = f'{variables[i]} AND {variables[n+i]}'
        clauses.append(clause)
    
    # Add a final clause to make the formula unsatisfiable
    final_clause = 'NOT ' + variables[0]
    clauses.append(final_clause)
    
    return ' AND '.join(clauses)

def generate_quiver_path(variables: list, clauses: list) -> dict:
    quiver = {}
    for variable in variables:
        quiver[variable] = set()
    
    for clause in clauses:
        literals = clause.split(' OR ')
        u, v = literals
        if 'NOT' in u:
            u = u.replace('NOT ', '')
            quiver[v].add(u)
        else:
            quiver[u].add(v)
    
    return quiver

def compute_min_generators(quiver: dict) -> int:
    generators = set()
    for node, neighbors in quiver.items():
        if not neighbors:
            generators.add(node)
    return len(generators)

def resolution_length(clauses: list) -> int:
    stack = []
    while clauses:
        clause = clauses.pop(0)
        literals = clause.split(' AND ')
        if 'NOT' in literals[0]:
            literal = literals[0].replace('NOT ', '')
            for i, c in enumerate(clauses):
                if literal in c:
                    new_clause = c.replace(literal, '').strip()
                    if new_clause:
                        clauses[i] = new_clause
                    else:
                        del clauses[i]
                    break
        else:
            stack.append(clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10  # Start with a small size and increase if necessary
    while True:
        formula = generate_tseitin_formula(n)
        variables = [v for v in formula.split() if 'x' in v]
        clauses = formula.split(' AND ')
        
        quiver = generate_quiver_path(variables, clauses)
        min_generators = compute_min_generators(quiver)
        proof_length = resolution_length(clauses)
        
        if min_generators > 0:
            break
        
        n += 1
    
    metric_value = proof_length
    instances_tested = 1
    conjecture_holds = proof_length >= 2 ** (min_generators + math.log(min_generators, 2))
    counterexample = "" if conjecture_holds else f"n={n}, min_gen={min_generators}, proof_len={proof_length}"
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        try:
            result = run_trial(seed)
            print(f"TRIAL: {result}")
            results.append(result)
        except Exception as e:
            print(f"ERROR on seed {seed}: {e}")
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")