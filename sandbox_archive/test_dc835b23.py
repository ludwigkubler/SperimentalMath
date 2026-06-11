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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literals = set(abs(l) for l in sum(cnf, []))
        literal = next((l for l in literals if all(l not in a and -l not in a for a in assignment)), None)
        if literal is None:
            return False
        
        def extend_assignment(assignment, literal):
            new_assignment = assignment[:]
            new_assignment.append(literal)
            return new_assignment
        
        return dpll(cnf, extend_assignment(assignment, literal)) or dpll(cnf, extend_assignment(assignment, -literal))
    
    def hodge_dimension(n):
        # Placeholder for actual Hodge dimension calculation
        # This is a dummy implementation for testing purposes
        return random.randint(1, n)
    
    n = 10  # Start with a small size and increase
    cnf = generate_cnf(n)
    dim_H = hodge_dimension(n)
    height_dpll = dpll(cnf)
    
    if not height_dpll:
        return {
            "metric_name": "Hodge Dimension vs DPLL Height",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree did not find a solution"
        }
    
    return {
        "metric_name": "Hodge Dimension vs DPLL Height",
        "metric_value": dim_H / height_dpll,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")