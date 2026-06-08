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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([-variables[i], variables[i + 1]])
        clauses.append([-variables[-1]])
        return clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True
            if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
                return True
            new_assignment[var] = False
            if dpll([c for c in clauses if var not in c and -var not in c], new_assignment):
                return True
            return False
        pure_literal = next((v for v in variables if all(v not in c or -v in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        p, q = random.sample(variables, 2)
        while p == q:
            p, q = random.sample(variables, 2)
        new_assignment[p] = True
        if dpll([c for c in clauses if p not in c and -p not in c], new_assignment):
            return True
        new_assignment[p] = False
        new_assignment[q] = True
        if dpll([c for c in clauses if q not in c and -q not in c], new_assignment):
            return True
        new_assignment[q] = False
        return False
    
    def quadratic_residues_in_ap(n):
        residues = set()
        for a in range(1, n + 1):
            for d in range(1, n + 1):
                if (a % d == 0 or (n - a) % d == 0):
                    residues.add(a)
                    residues.add(n - a)
        return len(residues)
    
    def resolution_width(clauses):
        stack = clauses[:]
        while stack:
            clause1, *stack = stack
            if not clause1:
                return float('inf')
            for clause2 in stack:
                common_vars = [var for var in clause1 if -var in clause2]
                if common_vars:
                    new_clause = list(set(clause1 + clause2) - set(common_vars))
                    stack.append(new_clause)
                    break
        return len(stack)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_formula(n)
    resolution_width_value = resolution_width(clauses)
    qr_ap_count = quadratic_residues_in_ap(n)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": resolution_width_value <= qr_ap_count + 3 and resolution_width_value >= qr_ap_count - 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE reason=no_results")
        sys.exit(0)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = (sum((result["metric_value"] - mean_width) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")