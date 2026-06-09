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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                   for _ in range(random.randint(1, 3))]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = [None] * (max(abs(l) for l in sum(cnf, [])) + 1)

    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()
        value = 1 if literal > 0 else -1
        assignment[abs(literal)] = value
        new_clauses = []
        for clause in cnf:
            if literal in clause:
                continue
            elif any(l * assignment[abs(l)-1] <= 0 for l in clause):
                new_clauses.append(clause)
            else:
                new_clauses.append([l for l in clause if l != -literal])
        cnf = new_clauses

    pure_literals = [l for l in range(1, len(assignment)) if (assignment[l] is None and
                                                           all(l not in c or assignment[abs(c[0])-1] == 1 for c in cnf) and
                                                           all(-l not in c or assignment[abs(c[0])-1] == -1 for c in cnf))]
    while pure_literals:
        literal = pure_literals.pop()
        value = 1 if literal > 0 else -1
        assignment[abs(literal)] = value
        new_clauses = []
        for clause in cnf:
            if literal in clause:
                continue
            elif any(l * assignment[abs(l)-1] <= 0 for l in clause):
                new_clauses.append(clause)
            else:
                new_clauses.append([l for l in clause if l != -literal])
        cnf = new_clauses

    if not cnf:
        return True
    elif any(all(l * assignment[abs(l)-1] <= 0 for l in c) for c in cnf):
        return False
    else:
        literal = random.choice([l for l in range(1, len(assignment)) if assignment[l] is None])
        value = 1 if literal > 0 else -1
        assignment[abs(literal)] = value
        return dpll(cnf, assignment) or dpll(cnf, [v if i != abs(literal) else None for i, v in enumerate(assignment)])

def construct_quasi_crystal(height):
    # Simplified quasi-crystal construction (not actual encoding)
    return "Q(" + str(height) + ")"

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    m = 3 * n
    cnf = generate_cnf(n, m)
    height = dpll(cnf)
    quasi_crystal = construct_quasi_crystal(height)
    metric_value = len(quasi_crystal)
    instances_tested = 1
    n_max = n
    conjecture_holds = True if metric_value <= math.sqrt(n) else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "quasi_crystal_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")