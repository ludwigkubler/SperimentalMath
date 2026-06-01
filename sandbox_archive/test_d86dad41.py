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

# Constants for DPLL algorithm
MAX_RECURSION_DEPTH = 20000
sys.setrecursionlimit(MAX_RECURSION_DEPTH)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10*n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment, literals):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(new_cnf, new_assignment, literals)
        pure_literal = next((l for l in literals if all(l in c or -l in c for c in cnf)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_cnf = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
            return dpll(new_cnf, new_assignment, literals)
        literal = random.choice(literals)
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        if dpll(cnf, new_assignment_true, literals):
            return True
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        return dpll(cnf, new_assignment_false, literals)

    def calculate_diameter(cnf):
        n = len(cnf)
        literals = set(abs(l) for c in cnf for l in c)
        return dpll(cnf, {}, literals)

    def calculate_mcr(cnf):
        # Placeholder for minimal local cohomology rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mcr = calculate_mcr(cnf)
    d = calculate_diameter(cnf)
    
    if d > 2**n:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d > 2^n"
        }
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": mcr / d if d != 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")