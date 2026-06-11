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
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables each
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literals = set(l for clause in cnf for l in clause)
        unit_clauses = [l for l in literals if any(l == lit or -l == lit for clause in cnf)]
        if unit_clauses:
            literal = unit_clauses[0]
            assignment.append(literal)
            return dpll(cnf, assignment) or dpll(cnf, extend_assignment(assignment, -literal))
        
        literal = next((l for l in literals if all(l not in a and -l not in a for a in assignment)), None)
        if literal is None:
            return False
        return dpll(cnf, extend_assignment(assignment, literal)) or dpll(cnf, extend_assignment(assignment, -literal))
    
    def extend_assignment(assignment, literal):
        new_assignment = list(assignment)
        new_assignment.append(literal)
        return new_assignment
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    height_dpll = dpll(cnf)
    
    if not isinstance(height_dpll, int) or height_dpll <= 0:
        return {
            "metric_name": "DPLL Height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_height_invalid"
        }
    
    # Placeholder for Hodge p-structure computation
    dim_H = random.randint(1, n)  # Simplified placeholder
    
    return {
        "metric_name": "DPLL Height",
        "metric_value": height_dpll,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")