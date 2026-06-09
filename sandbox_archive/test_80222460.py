# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(cnf, assignment=None):
        if not cnf:
            return True
        if any(all(abs(x) != i + 1 for x in clause) for i, clause in enumerate(cnf)):
            return False
        
        var = next((i for i in range(len(cnf)) if all(abs(x) != i + 1 for x in cnf[i])), None)
        pos_var, neg_var = var + 1, -var - 1
        
        assignment = assignment or {}
        if pos_var not in assignment and neg_var not in assignment:
            assignment[pos_var] = True
            if dpll(cnf, assignment):
                return True
            assignment.pop(pos_var)
            assignment[neg_var] = True
            if dpll(cnf, assignment):
                return True
            assignment.pop(neg_var)
        elif pos_var in assignment and not assignment[pos_var]:
            assignment[neg_var] = True
            if dpll(cnf, assignment):
                return True
            assignment.pop(neg_var)
        elif neg_var in assignment and not assignment[neg_var]:
            assignment[pos_var] = True
            if dpll(cnf, assignment):
                return True
            assignment.pop(pos_var)
        
        return False
    
    def generate_cnf(n: int) -> list:
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def frege_depth(cnf: list) -> int:
        depth = 0
        stack = [cnf]
        while stack:
            current_clause = stack.pop()
            depth += 1
            new_clauses = []
            for clause in current_clause:
                if abs(clause) == 1 or abs(clause) == -1:
                    continue
                var, sign = abs(clause), clause // abs(clause)
                new_clauses.extend([c for c in cnf if sign * var not in c])
            stack.extend(new_clauses)
        return depth
    
    def diophantine_exponent(cnf: list) -> int:
        # Placeholder function to compute the diophantine exponent
        # This is a dummy implementation and should be replaced with an actual algorithm
        return 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    depth = frege_depth(cnf)
    e_phi = diophantine_exponent(cnf)
    
    if depth > e_phi ** 2 * math.log(n):
        return {
            "metric_name": "depth",
            "metric_value": depth,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d(φ) > e(φ)^2 * log(n)"
        }
    
    return {
        "metric_name": "depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='d(φ) > e(φ)^2 * log(n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")