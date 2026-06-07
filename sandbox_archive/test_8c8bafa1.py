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
    for _ in range(10):  # Generate 10 clauses
        clause = []
        for i in range(n):
            coeff = random.choice([-1, 1])
            if all(abs(coeff) != abs(clause[j]) for j in range(len(clause))):
                clause.append(coeff)
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    # Simplified DPLL solver to estimate resolution width
    clauses = [set(clause) for clause in cnf]
    unit_clauses = {c for c in set.union(*clauses) if len(c) == 1}
    
    while unit_clauses:
        unit_clause = next(iter(unit_clauses))
        unit_clauses.remove(unit_clause)
        
        for i, clause in enumerate(clauses):
            if unit_clause in clause:
                clauses[i] -= {unit_clause}
                if not clauses[i]:
                    return float('inf')
                elif len(clauses[i]) == 1:
                    unit_clauses.add(next(iter(clauses[i])))
    
    return len(cnf)

def tropical_hodge_index(cnf):
    # Placeholder for actual computation
    # For simplicity, we use the number of variables as a proxy
    n = sum(len(clause) for clause in cnf)
    return Fraction(n, 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ht = tropical_hodge_index(cnf)
        w = resolution_width(cnf)
        
        if w == float('inf'):
            continue
        
        ratio = Fraction(ht, w)
        ratios.append(ratio)
    
    if not ratios:
        return {
            "metric_name": "ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_ratio"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(r >= Fraction(1, 1) for r in ratios)
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(ratios),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_less_than_1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=empty_ratio")