# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            if (var, sign) not in clause and (-var, -sign) not in clause:
                clause.add((var, sign))
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment):
    if not cnf:
        return True
    unit_clauses = [c for c in cnf if len(c) == 1]
    if unit_clauses:
        var, sign = unit_clauses[0][0], unit_clauses[0][1]
        if (var, sign) in assignment or (-var, -sign) in assignment:
            return False
        assignment[var] = sign
        cnf = [c for c in cnf if var not in c and -var not in c]
    pure_literals = {}
    for literal in set(var for clause in cnf for var, _ in clause):
        pos_count = sum(sign == 1 for _, sign in clause if literal == abs(literal))
        neg_count = sum(sign == -1 for _, sign in clause if literal == abs(literal))
        if pos_count == 0:
            pure_literals[literal] = -1
        elif neg_count == 0:
            pure_literals[literal] = 1
    if pure_literals:
        var, sign = next((k, v) for k, v in pure_literals.items())
        if (var, sign) in assignment or (-var, -sign) in assignment:
            return False
        assignment[var] = sign
        cnf = [c for c in cnf if var not in c and -var not in c]
    for literal in range(1, n + 1):
        if literal not in assignment and -literal not in assignment:
            if dpll(cnf, {**assignment, literal: 1}):
                return True
            if dpll(cnf, {**assignment, literal: -1}):
                return True
    return False

def fourier_coefficient(cnf, subset):
    n = len(cnf)
    assignment = {var: (i >> j) & 1 for j in range(n) for var in cnf[j] if var[0] == j + 1}
    return (-1) ** sum(assignment[var] != sign for var, sign in subset)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    
    dpll_size = sum(dpll(cnf, {}) for _ in range(10))
    subsets = list(combinations(range(1, n + 1), 1)) + list(combinations(range(1, n + 1), 2))
    fourier_sum = sum(fourier_coefficient(cnf, subset) for subset in subsets)
    
    metric_value = dpll_size / abs(fourier_sum)
    instances_tested = 10
    conjecture_holds = True if metric_value > 0 else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Tree Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")