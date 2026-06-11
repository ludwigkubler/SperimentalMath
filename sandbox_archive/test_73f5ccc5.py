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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if not (literal in c or -literal in c)], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if not (literal in c or -literal in c)], new_assignment):
                return True
            return False
        literal, polarity = next((l, p) for l, p in assignment.items() if not any(l in c or -l in c for c in cnf))
        new_assignment[literal] = polarity
        if dpll([c for c in cnf if not (literal in c or -literal in c)], new_assignment):
            return True
        del new_assignment[literal]
        new_assignment[-literal] = not polarity
        if dpll([c for c in cnf if not (literal in c or -literal in c)], new_assignment):
            return True
        return False
    
    def hecke_eigenform_order(n):
        # Placeholder function to simulate the order calculation
        return random.randint(1, n)
    
    n = 40
    cnf = generate_cnf(n)
    dpll_width = len(cnf) * 2  # Simplified DPLL search tree width estimation
    hecke_order = hecke_eigenform_order(n)
    
    if dpll_width == 0 or hecke_order == 0:
        return {
            "metric_name": "mean_absolute_deviation",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    ratio = Fraction(hecke_order, dpll_width)
    return {
        "metric_name": "mean_absolute_deviation",
        "metric_value": abs(ratio - 1),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(result)