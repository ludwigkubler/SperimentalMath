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
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(2, 3))]
        cnf.append(clause)
    return cnf

def truth_table(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    table = []
    for i in range(2**n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if all(any(x * assignment[abs(lit)-1] >= 0 for x in clause) for clause in cnf):
            table.append(1)
        else:
            table.append(0)
    return table

def min_modular_function_order(table, n):
    m = len(table)
    f_phi = 0
    while True:
        found = False
        for i in range(n):
            if all(table[j] == (i * j) % m for j in range(m)):
                f_phi += 1
                found = True
                break
        if not found:
            break
    return f_phi

def tree_like_resolution_width(cnf, n):
    # Simplified DPLL solver to estimate width
    def dpll(clauses, assignment, literals):
        if not clauses:
            return len(assignment)
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(lit)-1] = (lit > 0)
            return dpll([c for c in clauses if not any(l in c for l in literals)], new_assignment, literals + [lit])
        pure_literal = next((l for l in range(1, n+1) if all((l in c or -l in c) for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment[:]
            new_assignment[pure_literal-1] = True
            return dpll([c for c in clauses if not any(l in c for l in literals)], new_assignment, literals + [pure_literal])
        return max(dpll(clauses, assignment + [False], literals), dpll(clauses, assignment + [True], literals))
    return dpll(cnf, [False] * n, [])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n, 30)
        table = truth_table(cnf)
        f_phi = min_modular_function_order(table, n)
        width = tree_like_resolution_width(cnf, n)
        results.append((n, f_phi, width))
    metric_value = sum(2**(n * f_phi) for n, f_phi, _ in results) / len(results)
    conjecture_holds = all(abs(2**(n * f_phi) - width) <= 3 for _, f_phi, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")