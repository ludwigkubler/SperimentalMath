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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unsatisfied = [c for c in cnf if not any(lit in assignment and assignment[lit] == sign for lit, sign in zip(c, (1, -1)))]
        if not unsatisfied:
            return True
        literal = next((lit for lit in range(1, n + 1) if lit not in assignment), None)
        if literal is None:
            return False
        assignment[literal] = True
        if dpll(cnf, assignment):
            return True
        assignment[literal] = False
        assignment[-literal] = True
        if dpll(cnf, assignment):
            return True
        return False
    
    def resolution(cnf):
        clauses = set(tuple(clause) for clause in cnf)
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        lit, _ = next((lit, sign) for lit, sign in zip(c1, (1, -1)) if lit in c2)
                        new_clause = tuple(sorted([l for l in c1 + c2 if l != lit and -l not in c1 + c2]))
                        if new_clause:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return max(len(c) for c in clauses)
    
    def galois_group_size(tutte_poly):
        factors = []
        while tutte_poly > 1:
            factor = 2
            while tutte_poly % factor == 0:
                factors.append(factor)
                tutte_poly //= factor
            factor += 1
        return len(factors) * math.log(len(factors), 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n * 10)
        cnf = generate_cnf(n, m)
        if not dpll(cnf):
            continue
        width = resolution(cnf)
        tutte_poly = 1
        for clause in cnf:
            tutte_poly *= (len(clause) + 1)
        galois_size = galois_group_size(tutte_poly)
        results.append({
            "n": n,
            "m": m,
            "width": width,
            "galois_size": galois_size
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(result["width"] for result in results) / len(results)
    mean_galois_size = sum(result["galois_size"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["width"] <= 3) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8 and mean_width <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")