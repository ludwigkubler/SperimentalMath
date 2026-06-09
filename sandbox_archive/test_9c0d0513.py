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
    
    def generate_formula(m, n):
        formula = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            formula.append(clause)
        return formula
    
    def dpll(formula, assignment):
        if not formula:
            return True
        unit_clause = next((c for c in formula if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            if unit_clause[0] > 0:
                assignment[var] = True
            else:
                assignment[var] = False
            return dpll(formula, assignment)
        
        p = next((v for v in range(1, n + 1) if v not in assignment), None)
        new_assignment = assignment.copy()
        new_assignment[p] = True
        if dpll([c for c in formula if not any(abs(v) == abs(c[0]) for v in new_assignment)], new_assignment):
            return True
        
        new_assignment[p] = False
        new_assignment[-p] = True
        if dpll([c for c in formula if not any(abs(v) == abs(c[0]) for v in new_assignment)], new_assignment):
            return True
        
        return False
    
    def resolution_width(formula):
        queue = [frozenset(clause) for clause in formula]
        while True:
            unit_clause = next((c for c in queue if len(c) == 1), None)
            if not unit_clause:
                break
            var = abs(unit_clause.pop())
            new_clauses = set()
            for clause in queue:
                if var in clause:
                    continue
                if -var in clause:
                    queue.remove(clause)
                    continue
                new_clauses.add(frozenset(c for c in clause if c != -var))
            queue.update(new_clauses)
        return len(queue) + 1
    
    m = random.randint(5, 30)
    n = random.randint(m, 40)
    formula = generate_formula(m, n)
    
    assignment = {}
    width = resolution_width(formula)
    
    if width == 0:
        return {
            "metric_name": "msl_to_w_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    msl = len(formula)
    ratio = msl / width
    
    return {
        "metric_name": "msl_to_w_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 1 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")