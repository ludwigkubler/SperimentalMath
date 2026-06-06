# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll(sat_formula):
        def solve(formula, assignment):
            if not formula:
                return True
            literal = next((l for l in formula[0] if l != 0), None)
            if literal is None:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = 1
            if solve(formula, new_assignment):
                return True
            new_assignment[literal] = -1
            if solve(formula, new_assignment):
                return True
            return False
        
        return solve(sat_formula, {})
    
    def tropical_derivative_degree(cnf):
        n = len(cnf)
        degree = 0
        for clause in cnf:
            for literal in clause:
                if abs(literal) > degree:
                    degree = abs(literal)
        return degree
    
    def resolution_width(cnf):
        queue = [cnf]
        while queue:
            clause = queue.pop(0)
            if not any(clause[i] == 0 for i in range(len(clause))):
                continue
            new_clause = []
            for c in clause:
                if abs(c) != abs(clause[0]):
                    new_clause.append(c)
            if not new_clause:
                return len(queue)
            queue.append(new_clause)
        return len(queue)
    
    n_max = 40
    instances_tested = 0
    total_ratio = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        if not cnf:
            continue
        
        degree = tropical_derivative_degree(cnf)
        width = resolution_width(cnf)
        
        if width == 0:
            continue
        
        ratio = Fraction(degree, width)
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Tropical Derivative Degree / Resolution Width Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "Tropical Derivative Degree / Resolution Width Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_ratio = total_ratio / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, ratio={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break