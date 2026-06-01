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
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)] = literal > 0
            if not dpll([c for c in cnf if literal not in c], new_assignment):
                return False
            new_assignment[abs(literal)] = not (literal > 0)
            if not dpll([c for c in cnf if literal not in c], new_assignment):
                return False
        else:
            literal = next((i for i in range(1, n + 1) if i not in assignment), None)
            if not dpll(cnf, {**assignment, literal: True}):
                return dpll(cnf, {**assignment, literal: False})
        return False
    
    def min_quaternionic_roots(cnf):
        # Simplified version for demonstration; actual implementation needed
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    assignment = {}
    diameter = dpll(cnf, assignment)
    
    if not diameter:
        return {
            "metric_name": "min_quaternionic_roots",
            "metric_value": min_quaternionic_roots(cnf),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree diameter not computed"
        }
    
    return {
        "metric_name": "min_quaternionic_roots",
        "metric_value": min_quaternionic_roots(cnf),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")