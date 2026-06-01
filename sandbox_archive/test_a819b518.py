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
    cnf = []
    for _ in range(10 * n):  # Each variable appears in about 10 clauses
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        cnf.append(clause)
    return cnf

def min_local_ring_norm(cnf):
    p = 2  # Using a fixed p-adic field
    norm = 0
    for clause in cnf:
        val = sum(abs(lit) for lit in clause)
        if val > norm:
            norm = val
    return Fraction(norm, p**len(cnf))

def dpll_solve(cnf):
    def solve(variables, assignment):
        if not variables:
            return True
        var = variables[0]
        pos_var, neg_var = abs(var), -var
        if pos_var in assignment and assignment[pos_var] == False:
            return False
        if neg_var in assignment and assignment[neg_var] == True:
            return False
        assignment[var] = True
        if solve(variables[1:], assignment):
            return True
        assignment[var] = False
        assignment[-var] = True
        if solve(variables[1:], assignment):
            return True
        del assignment[var]
        del assignment[-var]
        return False

    variables = list(range(1, max(abs(lit) for lit in cnf) + 1))
    assignment = {}
    return solve(variables, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlations = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_norm_val = min_local_ring_norm(cnf)
        width = dpll_solve(cnf)
        
        if width is None or min_norm_val is None:
            return {
                "metric_name": "correlation",
                "metric_value": 0.0,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        correlation = min_norm_val * width
        correlations.append(correlation)
    
    mean_corr = sum(correlations) / len(correlations)
    std_corr = math.sqrt(sum((x - mean_corr) ** 2 for x in correlations) / len(correlations))
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": all(0.7 <= corr >= 0.5 for corr in correlations) and mean_corr >= 0.8,
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
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results) or support_fraction < 0.6:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=seeds[0]) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")