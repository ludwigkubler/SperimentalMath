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
                   for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = [None] * (max(abs(l) for clause in cnf for l in clause))
    
    unit_clauses = [l for clause in cnf if len(clause) == 1]
    while unit_clauses:
        l = unit_clauses.pop()
        if assignment[abs(l)-1] is None:
            assignment[abs(l)-1] = 1 if l > 0 else -1
        for clause in cnf:
            if l in clause:
                clause.remove(l)
                if not clause:
                    return False
    
    pure_literals = [l for l in range(1, len(assignment)+1) if (l not in assignment and -l not in assignment)]
    while pure_literals:
        l = pure_literals.pop()
        polarity = 1 if sum(1 for clause in cnf if l in clause) > sum(1 for clause in cnf if -l in clause) else -1
        if assignment[abs(l)-1] is None:
            assignment[abs(l)-1] = polarity
    
    unsatisfied_clauses = [clause for clause in cnf if any(l * assignment[abs(l)-1] <= 0 for l in clause)]
    if not unsatisfied_clauses:
        return True
    
    l, _ = random.choice(unsatisfied_clauses)
    new_assignment = assignment[:]
    new_assignment[abs(l)-1] = 1 if l > 0 else -1
    if dpll(cnf, new_assignment):
        return True
    
    new_assignment[abs(l)-1] = -1 if l > 0 else 1
    return dpll(cnf, new_assignment)

def quasi_crystal_pattern(height):
    pattern = []
    for i in range(1, height + 1):
        row = [i * j for j in range(1, i + 1)]
        pattern.extend(row)
    return pattern

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        height = dpll(cnf)
        if height is False:
            continue
        pattern = quasi_crystal_pattern(height)
        metric_value = len(pattern)
        results.append(metric_value)
    
    if not results:
        return {
            "metric_name": "quasi_crystal_size",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(x <= 10 * math.sqrt(n) for n, x in zip(n_values, results))
    counterexample = "" if conjecture_holds else "n_max={} failed".format(max(n_values))
    
    return {
        "metric_name": "quasi_crystal_size",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 10 * math.sqrt(max(n_values))) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean, std_dev, support_fraction))
    elif any(r > 10 * math.sqrt(max(n_values)) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 10 * math.sqrt(max(n_values)))
        print("RESULT: FALSIFIED counterexample='n_max={} failed' first_failing_seed={}".format(max(n_values), first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={}".format(len(results)))