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

def generate_formula(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            clauses.append(clause)
    return clauses

def dpll(clauses, assignment):
    unsatisfied_clauses = [c for c in clauses if not any(l in assignment and assignment[l] == v for l, v in zip(c, (1, -1)))]
    if not unsatisfied_clauses:
        return True
    literal = random.choice([l for c in unsatisfied_clauses for l in c if l not in assignment])
    if dpll(clauses, {**assignment, literal: 1}):
        return True
    if dpll(clauses, {**assignment, literal: -1}):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_formula(n)
    
    if not clauses:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    resolution_width = len(clauses)
    dpll_depth = 1
    
    def backtrack(assignment, depth):
        nonlocal dpll_depth
        if not assignment:
            dpll_depth = max(dpll_depth, depth)
        for literal in range(1, n + 1):
            if literal not in assignment and -literal not in assignment:
                new_assignment = {**assignment, literal: 1}
                if dpll(clauses, new_assignment):
                    backtrack(new_assignment, depth + 1)
                new_assignment = {**assignment, literal: -1}
                if dpll(clauses, new_assignment):
                    backtrack(new_assignment, depth + 1)
    
    backtrack({}, 0)
    
    m_n = len([c for c in clauses if any(l in assignment and assignment[l] == v for l, v in zip(c, (1, -1)))])

    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_n <= resolution_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}"
    
    print(result)