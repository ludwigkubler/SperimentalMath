# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def unit_propagate(clauses, assignment):
    new_clauses = []
    for clause in clauses:
        if not any(lit in assignment and assignment[lit] == val for lit, val in clause):
            new_clauses.append(clause)
    return new_clauses

def find_partial_assignment_compression_set(clauses, n):
    for k in range(1, 2*n+1):
        for subset in combinations(range(-n, 0), k):
            assignment = {lit: True if lit > 0 else False for lit in subset}
            remaining_clauses = unit_propagate(clauses, assignment)
            if not remaining_clauses:
                return k
    return n

def dpll(clauses, assignment, depth=0):
    if not clauses:
        return depth
    if any(all(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in clauses):
        return depth
    var = next(var for var in range(-n, 0) if var not in assignment)
    assignment[var] = True
    max_depth_true = dpll(unit_propagate(clauses, assignment), assignment, depth + 1)
    del assignment[var]
    assignment[var] = False
    max_depth_false = dpll(unit_propagate(clauses, assignment), assignment, depth + 1)
    return max(max_depth_true, max_depth_false)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    total_tests = len(n_values) * 50
    support_count = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(50):
            clauses = []
            for i in range(int(4*n/3)):
                clause = [(random.randint(-n, -1), random.choice([True, False]))]
                while True:
                    lit = random.randint(-n, -1)
                    val = random.choice([True, False])
                    if (lit, val) not in clause and (-lit, not val) not in clause:
                        clause.append((lit, val))
                        break
                clauses.append(clause)
            
            C_F = find_partial_assignment_compression_set(clauses, n)
            D_F = dpll(clauses, {})
            
            if D_F > 3 * C_F + math.ceil(math.log2(n)) + 2:
                counterexample = f"D(F)={D_F} > 3*C(F)+log2({n})+2"
                return {
                    "metric_name": "support_fraction",
                    "metric_value": support_count / total_tests,
                    "instances_tested": total_tests,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            if C_F <= D_F <= 3 * C_F + math.ceil(math.log2(n)):
                support_count += 1
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_count / total_tests,
        "instances_tested": total_tests,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={support_fraction} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")