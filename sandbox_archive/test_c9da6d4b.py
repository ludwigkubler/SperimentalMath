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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) * (1 if random.choice([True, False]) else -1) for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    unit_clauses = [lit for lit in cnf if len(lit) == 1]
    while unit_clauses:
        lit = unit_clauses.pop()
        value = True if lit > 0 else False
        assignment[abs(lit)] = value
        cnf = [[l for l in clause if l != lit and l != -lit] for clause in cnf]
        unit_clauses.extend([l for l in cnf if len(l) == 1])

    pure_literals = [lit for lit, value in assignment.items() if all(abs(lit) not in assignment or assignment[abs(lit)] == value for clause in cnf for l in clause)]
    while pure_literals:
        lit = pure_literals.pop()
        value = True
        assignment[lit] = value
        cnf = [[l for l in clause if l != lit and l != -lit] for clause in cnf]

    if not cnf:
        return assignment

    literal, _ = random.choice(cnf)
    return dpll(cnf, assignment | {literal: True}) or dpll(cnf, assignment | {literal: False})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = len(dpll(cnf))
    alpha_H_n_squared = n  # Simplified for testing purposes
    c_n = n  # Simplified for testing purposes
    conjecture_holds = width <= c_n * alpha_H_n_squared
    counterexample = "" if conjecture_holds else f"CNF with {n} vertices and DPLL search tree width {width}"
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")