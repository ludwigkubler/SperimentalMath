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
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)]
        for _ in range(random.randint(0, n-1)):
            clause.append(random.randint(1, n) * (-1 if random.choice([True, False]) else 1))
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    unsatisfied = [c for c in cnf if not any(l in assignment and assignment[l] == (l > 0) for l in c)]
    if not unsatisfied:
        return True
    unit_clauses = [c for c in unsatisfied if len(c) == 1]
    if unit_clauses:
        literal, _ = unit_clauses[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = (literal > 0)
        return dpll(cnf, new_assignment) or dpll(cnf, new_assignment.copy())
    pure_literals = {}
    for c in unsatisfied:
        for l in c:
            if l not in pure_literals:
                pure_literals[l] = True
            elif pure_literals[l]:
                del pure_literals[l]
            else:
                pure_literals[l] = False
    if pure_literals:
        literal, polarity = next(iter(pure_literals.items()))
        new_assignment = assignment.copy()
        new_assignment[literal] = polarity
        return dpll(cnf, new_assignment) or dpll(cnf, new_assignment.copy())
    p = random.choice([l for l in range(1, len(cnf)+1)])
    return dpll(cnf, assignment.copy()) or dpll(cnf, assignment.copy())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            continue
        entropy = topological_entropy(cnf)
        results.append(entropy)
    
    mean_entropy = sum(results) / len(results)
    support_fraction = len([r for r in results if abs(r - math.log(n)) < 3]) / len(results)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_entropy} std=NA support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_entropy = sum(results) / len(results)
    support_fraction = sum(1 for r in results if abs(r - math.log(n)) < 3) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=NA support_fraction={support_fraction}")
    elif any(abs(r - math.log(n)) > 3 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result - math.log(n)) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_entropy} std=NA support_fraction={support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=0")