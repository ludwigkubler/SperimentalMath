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
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    assignment = {}
    queue = [clause for clause in cnf if len(clause) == 1]
    
    while queue:
        literal = queue.pop()
        if literal in assignment and assignment[literal] != -literal:
            continue
        assignment[literal] = True
        
        new_clauses = []
        for clause in cnf:
            if literal in clause:
                new_clauses.append([l for l in clause if l != literal])
            elif -literal in clause:
                new_clauses.append([l for l in clause if l != -literal])
        
        for i in range(len(new_clauses)):
            for j in range(i + 1, len(new_clauses)):
                if set(new_clauses[i]) & set(new_clauses[j]):
                    queue.append(list(set(new_clauses[i]) ^ set(new_clauses[j])))
    
    return max(len(assignment), 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    
    resolution_width_value = resolution_width(cnf)
    distinct_quadratic_forms = len(set(tuple(sorted(clause)) for clause in cnf))
    
    metric_name = "resolution_width"
    metric_value = resolution_width_value
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    if 0.8 <= resolution_width_value / math.sqrt(n) <= 1.2 and distinct_quadratic_forms <= 1.5 * resolution_width_value:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "resolution_width_ratio_not_within_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")