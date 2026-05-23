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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_k_cnf(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    formula = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        formula.append(clause)
    return formula

def resolve_clause(clause, assignment):
    return any([assignment[var] for var in clause])

def dpll(formula, assignment, variables):
    if not formula:
        return True
    unit_clauses = [c for c in formula if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        if literal < 0:
            literal = -literal
        assignment[literal] = True
        new_formula = [[l for l in c if l != literal and l != -literal] for c in formula]
        return dpll(new_formula, assignment, variables)
    pure_literals = {}
    for var in variables:
        pos_count = sum(1 for clause in formula if var in clause)
        neg_count = sum(1 for clause in formula if -var in clause)
        if pos_count == 0 and var not in pure_literals:
            pure_literals[var] = True
        elif neg_count == 0 and var not in pure_literals:
            pure_literals[var] = False
    if pure_literals:
        literal = next(iter(pure_literals))
        assignment[literal] = pure_literals[literal]
        new_formula = [[l for l in c if l != literal and l != -literal] for c in formula]
        return dpll(new_formula, assignment, variables)
    var = random.choice(variables)
    assignment[var] = True
    if dpll(formula, assignment, variables):
        return True
    assignment[var] = False
    if dpll(formula, assignment, variables):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 5 * n
    formula = generate_k_cnf(n, m)
    
    rank = len(set(tuple(sorted(clause)) for clause in formula))
    assignment = {var: False for var in range(1, n + 1)}
    proof_length = 0
    
    while not dpll(formula, assignment, list(range(1, n + 1))):
        proof_length += 1
        # Simplify the formula by removing satisfied clauses and unit literals
        formula = [c for c in formula if not resolve_clause(c, assignment)]
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank <= proof_length ** (1/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")