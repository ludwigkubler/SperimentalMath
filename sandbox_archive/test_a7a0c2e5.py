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

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(x == 0 for x in clause):
            continue
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len([x for x in c if x != 0]) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        var = abs(literal) - 1
        new_assignment[var] = literal > 0
        return dpll(cnf, new_assignment)
    
    var = next((i for i in range(len(cnf)) if all(abs(x) != i + 1 for x in cnf[i])), None)
    if var is None:
        return False
    
    assignment[var] = True
    if dpll(cnf, assignment):
        return True
    assignment[var] = False
    if dpll(cnf, assignment):
        return True
    return False

def compute_diophantine_exponent(phi):
    # Placeholder for actual computation of diophantine exponent
    # This is a dummy function that should be replaced with the actual implementation
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            return {
                "metric_name": "diophantine_exponent",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable_cnf"
            }
        
        diophantine_exponent = compute_diophantine_exponent(cnf)
        depth = len(dpll(cnf, {}))  # Simplified for demonstration
        
        results.append({
            "n": n,
            "diophantine_exponent": diophantine_exponent,
            "depth": depth
        })
    
    if not results:
        return {
            "metric_name": "diophantine_exponent",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    diophantine_values = [r["diophantine_exponent"] ** 2 * math.log(r["n"]) for r in results]
    depth_values = [r["depth"] for r in results]
    
    correlation_coefficient = sum((d1 - mean(diophantine_values)) * (d2 - mean(depth_values))
                                  for d1, d2 in zip(diophantine_values, depth_values)) / (
        len(diophantine_values) * std(diophantine_values) * std(depth_values)
    )
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(d <= e ** 2 * math.log(n) for n, d, e in zip(results["n"], results["depth"], results["diophantine_exponent"]))
    
    return {
        "metric_name": "diophantine_exponent",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation_coefficient < 0.8 or d > e^2 * log(n)"
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample=\"correlation_coefficient < 0.8 or d > e^2 * log(n)\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(f"RESULT: {RESULT} mean={mean([r['metric_value'] for r in results if r['metric_value'] is not None])} std={std([r['metric_value'] for r in results if r['metric_value'] is not None])} support_fraction={sum(r['conjecture_holds'] for r in results) / len(results)}")