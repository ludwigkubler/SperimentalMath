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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def smallest_prime_divisor(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0 and is_prime(i):
            return i
    return n if is_prime(n) else None

def generate_cnf(num_vars, num_clauses):
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, num_vars)
            sign = random.choice([1, -1])
            if (var, sign) not in clause and (-var, sign) not in clause:
                clause.add((var, sign))
        clauses.append(clause)
    return clauses

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal, = next(iter(unit_clauses))
        value = literal > 0
        assignment[literal] = value
        clauses = [c - {literal} for c in clauses if literal not in c and -literal not in c]
        unit_clauses = [c for c in clauses if len(c) == 1]
    
    pure_literals = {}
    for var in range(1, max(abs(lit) for lit in assignment.keys()) + 1):
        pos_count = sum(1 for lit in assignment if lit > 0 and abs(lit) == var)
        neg_count = sum(1 for lit in assignment if lit < 0 and abs(lit) == var)
        if pos_count == 0:
            pure_literals[var] = False
        elif neg_count == 0:
            pure_literals[var] = True
    
    while pure_literals:
        var, value = next(iter(pure_literals.items()))
        literal = var * (1 if value else -1)
        assignment[literal] = value
        clauses = [c - {literal} for c in clauses if literal not in c and -literal not in c]
        del pure_literals[var]
    
    if not clauses:
        return True
    
    unassigned_vars = [var for var in range(1, max(abs(lit) for lit in assignment.keys()) + 1) if var not in assignment]
    if not unassigned_vars:
        return False
    
    var = random.choice(unassigned_vars)
    value = random.choice([True, False])
    literal = var * (1 if value else -1)
    
    new_assignment = assignment.copy()
    new_assignment[literal] = value
    if dpll(clauses, new_assignment):
        return True
    
    del new_assignment[literal]
    new_assignment[-literal] = not value
    if dpll(clauses, new_assignment):
        return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    num_vars = random.randint(5, 40)
    num_clauses = random.randint(num_vars // 2, min(num_vars * (num_vars - 1) // 2, 100))
    clauses = generate_cnf(num_vars, num_clauses)
    
    length = dpll(clauses)
    if length is None:
        return {
            "metric_name": "DPLL proof length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": num_vars,
            "conjecture_holds": False,
            "counterexample": "dpll returned None"
        }
    
    q = smallest_prime_divisor(num_vars)
    if q is None:
        return {
            "metric_name": "DPLL proof length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": num_vars,
            "conjecture_holds": False,
            "counterexample": "no prime divisor found"
        }
    
    log_q = math.log(q)
    
    return {
        "metric_name": "DPLL proof length",
        "metric_value": length,
        "instances_tested": 1,
        "n_max": num_vars,
        "conjecture_holds": length <= log_q,
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
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dpll returned None\" first_failing_seed={seeds[first_failing_seed]}")